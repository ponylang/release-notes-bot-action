#!/usr/bin/python3

import git,json,os,sys
from github import Github

# x FLOW WE NEED --> on push to master...
# x CHECK TO SEE IF THERE IS AN ASSOCIATED PR (via search)
# x EXIT IF NO
# GITHUB_EVENT_PATH get commits
# FOREACH get sha, look up commit from commits url
# check files for release notes file
# IF/WHEN FOUND...
# get release notes content from `raw_url`
# add release notes to end of `next-release.md`
# delete release notes addition from PR
# git add .release-notes/next-release.md

ENDC   = '\033[0m'
ERROR  = '\033[31m'
INFO   = '\033[34m'
NOTICE = '\033[33m'

if not 'API_CREDENTIALS' in os.environ:
  print(ERROR + "API_CREDENTIALS needs to be set in env. Exiting." + ENDC)
  sys.exit(1)

# login
github = Github(os.environ['API_CREDENTIALS'])

# get json data for our event
event_data = json.load(open(os.environ['GITHUB_EVENT_PATH'], 'r'))

# grab info needed to find PR
sha = event_data['head_commit']['id']
repo_name = event_data['repository']['full_name']

# find associated PR (if any)
print(INFO + "Finding PR associated with " + sha + " in " + repo_name + ENDC)
query = "q=is:merged+sha:" + sha + "+repo:" + repo_name
print(INFO + "Query: " + query + ENDC)
results = github.search_issues(query='is:merged', sha=sha, repo=repo_name)

if results.totalCount == 0:
  print(NOTICE + "No merged PR associated with " + sha + ". Exiting.")
  sys.exit(0)

pr_id = results[0].number

# find associated release notes file
release_notes_file = None
repo = github.get_repo(repo_name)
for commit in event_data['commits']:
    c = repo.get_commit(sha=commit['id'])
    for f in c.files:
      if f.filename.startswith('.release-notes/'):
        if not f.filename.endswith('next-release.md'):
          release_notes_file = f.filename

# if no release notes file, exit
if release_notes_file is None:
  print(NOTICE + "No release notes fie found in commits. Exiting." + ENDC)
  sys.exit(0)

print(INFO + "Setting up git configuration." + ENDC)
git = git.Repo('.').git
git.config('--global', 'user.name', os.environ['INPUT_GIT_USER_NAME'])
git.config('--global', 'user.email', os.environ['INPUT_GIT_USER_EMAIL'])

print(INFO + "Making sure repo is up to date." + ENDC)
git.checkout('master')
git.pull()

release_notes = open(release_notes_file, 'r').read().rstrip() + '\n'
next_release_notes = open('.release-notes/next-release.md', 'a+')
next_release_notes.write(release_notes)
next_release_notes.close()

print(INFO + "Adding git changes." + ENDC)
git.rm(release_notes_file)
git.add('.release-notes/next-release.md')
git.commit('-m', "Updating release notes for PR #" + str(pr_id)+ " [skip-ci]")

print(INFO + "Pushing updated release notes." + ENDC)
push_to = "https://" + os.environ['API_CREDENTIALS'] + "@github.com/" + repo_name + ".git"
# git.push(push_to, 'master')
os.system("/usr/bin/git push " + push_to + " master")
