#!/usr/bin/python3
# pylint: disable=C0103
# pylint: disable=C0114

import time
import json
import os
import sys
import git
from git.exc import GitCommandError
from github import Github
from github.GithubException import RateLimitExceededException
from github.GithubException import GithubException
import requests.exceptions

CHANGELOG_LABELS = ['changelog - added',
                    'changelog - changed',
                    'changelog - fixed']

ENDC = '\033[0m'
ERROR = '\033[31m'
INFO = '\033[34m'
NOTICE = '\033[33m'

def github_api_call(fn, description):
    """Call fn() with retry and exponential backoff on rate limits and connection errors."""
    api_failures = 0
    while True:
        try:
            return fn()
        except (RateLimitExceededException,
                requests.exceptions.ConnectionError):
            api_failures += 1
            if api_failures <= 5:
                backoff = 60 * (2 ** (api_failures - 1))
                print(NOTICE
                      + description + " failed. "
                      + "Sleeping " + str(backoff) + "s and trying again."
                      + ENDC)
                time.sleep(backoff)
            else:
                print(ERROR + description + " failed again. Giving up." + ENDC)
                raise
        except GithubException as e:
            err_msg = e.data.get('message', '') if isinstance(e.data, dict) else ''
            if "You have exceeded a secondary rate limit" in err_msg:
                api_failures += 1
                if api_failures <= 5:
                    backoff = 60 * (2 ** (api_failures - 1))
                    print(NOTICE
                          + description + " failed due to secondary rate limit. "
                          + "Sleeping " + str(backoff) + "s and trying again."
                          + ENDC)
                    time.sleep(backoff)
                else:
                    print(ERROR
                          + description + " failed again. Giving up."
                          + ENDC)
                    raise
            else:
                raise


if 'API_CREDENTIALS' not in os.environ:
    print(ERROR + "API_CREDENTIALS needs to be set in env. Exiting." + ENDC)
    sys.exit(1)

# login
github = Github(os.environ['API_CREDENTIALS'])

# get json data for our event
with open(os.environ['GITHUB_EVENT_PATH'], 'r', encoding='utf-8') as f:
    event_data = json.load(f)

# grab info needed to find PR
sha = event_data['head_commit']['id']
repo_name = event_data['repository']['full_name']

# find associated PR (if any)
print(INFO + "Finding PR associated with " + sha + " in " + repo_name + ENDC)
query = "q=is:merged+sha:" + sha + "+repo:" + repo_name
print(INFO + "Query: " + query + ENDC)
pr_id = 0
no_pr_failures = 0
search_failures = 0
while True:
    try:
        results = github.search_issues(query='is:merged', sha=sha,
                                       repo=repo_name)

        # something really weird has started happening after years where
        # totalCount gives us 0 when the API call from the command line does
        # not. The PyGithub people. So now we just try to get the first result.
        # *****do not use `totalCount`****
        try:
            pr_id = results[0].number
            print(INFO + "PR found " + str(pr_id) + ENDC)
            break
        except IndexError:
            no_pr_failures += 1
            if no_pr_failures <= 2:
                delay = 15 * no_pr_failures
                print(NOTICE
                      + "No merged PR associated with " + sha + " yet. "
                      + "Sleeping " + str(delay) + "s and trying again."
                      + ENDC)
                time.sleep(delay)
            else:
                print(NOTICE
                      + "No merged PR associated with " + sha
                      + ". Exiting."
                      + ENDC)
                sys.exit(0)
    except RateLimitExceededException:
        search_failures += 1
        if search_failures <= 5:
            delay = 60 * (2 ** (search_failures - 1))
            print(NOTICE
                  + "Search failed due to rate limit exceeded. "
                  + "Sleeping " + str(delay) + "s and trying again."
                  + ENDC)
            time.sleep(delay)
        else:
            print(ERROR + "Search failed again. Giving up." + ENDC)
            raise
    except GithubException as e:
        msg = e.data.get('message', '') if isinstance(e.data, dict) else ''
        if "You have exceeded a secondary rate limit" in msg:
            search_failures += 1
            if search_failures <= 5:
                delay = 60 * (2 ** (search_failures - 1))
                print(NOTICE
                    + "Search failed due to secondary rate limit exceeded. "
                    + "Sleeping " + str(delay) + "s and trying again."
                    + ENDC)
                time.sleep(delay)
            else:
                print(ERROR + "Search failed again. Giving up." + ENDC)
                raise
        else:
            raise
    except requests.exceptions.ConnectionError:
        search_failures += 1
        if search_failures <= 5:
            delay = 60 * (2 ** (search_failures - 1))
            print(NOTICE
                  + "Search failed due to connection error. "
                  + "Sleeping " + str(delay) + "s and trying again."
                  + ENDC)
            time.sleep(delay)
        else:
            print(ERROR + "Search failed again. Giving up." + ENDC)
            raise

# find associated release notes file
release_notes_files = set()
repo = github_api_call(lambda: github.get_repo(repo_name), "Get repo")
for commit in event_data['commits']:
    print(INFO + "Examining files in commit " + str(commit['id']) + ENDC)
    c = github_api_call(lambda c=commit: repo.get_commit(sha=c['id']),
                        "Get commit")
    for f in c.files:
        if f.status != "added":
            continue
        print(INFO + "Found file " + f.filename + ENDC)
        if f.filename.startswith('.release-notes/'):
            if not f.filename.endswith('next-release.md'):
                release_notes_files.add(f.filename)

# if no release notes files, exit
if not release_notes_files:
    print(NOTICE + "No release notes file found in commits. Exiting." + ENDC)
    sys.exit(0)

print(INFO + "Cloning repo." + ENDC)
pull_request = github_api_call(lambda: repo.get_pull(pr_id), "Get pull request")
clone_from = "https://" + os.environ['GITHUB_ACTOR'] \
              + ":" \
              + os.environ['API_CREDENTIALS'] \
              + "@github.com/" \
              + repo_name
pr_base_branch = pull_request.base.ref
clone_options = ["--branch=" + pr_base_branch]
git = git.Repo.clone_from(clone_from, '.', multi_options=clone_options).git

print(INFO + "Setting up git configuration." + ENDC)
git.config('--global', 'user.name', os.environ['INPUT_GIT_USER_NAME'])
git.config('--global', 'user.email', os.environ['INPUT_GIT_USER_EMAIL'])
git.config('--global', 'branch.autosetuprebase', 'always')
git.config('--global', '--add', 'safe.directory', os.environ['GITHUB_WORKSPACE'])

# check to make sure that the PR had a changelog label
# if it didn't delete the release notes file(s) and exit.
found_changelog_label = False
for prl in pull_request.labels:
    print(INFO + "PR had label: " + prl.name + ENDC)
    if prl.name in CHANGELOG_LABELS:
        found_changelog_label = True
        break

if found_changelog_label:
    print(NOTICE + "Processing release notes." + ENDC)
    release_notes = ""
    for rnf in release_notes_files:
        with open(rnf, 'r', encoding='utf-8') as f:
            release_notes += f.read().rstrip() + '\n\n'
    with open('.release-notes/next-release.md', 'a+', encoding='utf-8') as next_release_notes:
        next_release_notes.write(release_notes)

    print(INFO + "Adding git changes." + ENDC)
    for rnf in release_notes_files:
        git.rm(rnf)
    git.add('.release-notes/next-release.md')
    git.commit('-m', "Update release notes for PR #" + str(pr_id))
else:
    print(NOTICE + "Found release notes but no changelog label." + ENDC)
    for rnf in release_notes_files:
        git.rm(rnf)
    git.commit('-m',
               "Remove release notes from changelog labelless PR #"
               + str(pr_id))

push_failures = 0
while True:
    try:
        print(INFO + "Pushing changes." + ENDC)
        git.push()
        break
    except GitCommandError:
        push_failures += 1
        if push_failures <= 5:
            delay = 10 * (2 ** (push_failures - 1))
            print(NOTICE
                  + "Failed to push. Sleeping " + str(delay)
                  + "s, then pulling and trying again."
                  + ENDC)
            time.sleep(delay)
            git.pull(rebase=True)
        else:
            print(ERROR + "Failed to push again. Giving up." + ENDC)
            raise
