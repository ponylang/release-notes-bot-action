#!/usr/bin/python3

import git,json,os,sys
from github import Github

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
print(INFO + "PR found " + str(pr_id) + ENDC)

# find associated release notes file
release_notes_files = []
repo = github.get_repo(repo_name)
for commit in event_data['commits']:
  print(INFO + "Examining files in commit " + str(commit['id']) + ENDC)
  c = repo.get_commit(sha=commit['id'])
  for f in c.files:
    if f.status != "added":
      continue
    print(INFO + "Found file " + f.filename + ENDC)
    if f.filename.startswith('.release-notes/'):
      if not f.filename.endswith('next-release.md'):
        release_notes_files.append(f.filename)

# if no release notes files, exit
if not release_notes_files:
  print(NOTICE + "No release notes file found in commits. Exiting." + ENDC)
  sys.exit(0)

print(INFO + "Cloning repo." + ENDC)
clone_from = "https://" + os.environ['GITHUB_ACTOR'] + ":" + os.environ['API_CREDENTIALS'] + "@github.com/" + repo_name
git = git.Repo.clone_from(clone_from, '.').git

print(INFO + "Setting up git configuration." + ENDC)
git.config('--global', 'user.name', os.environ['INPUT_GIT_USER_NAME'])
git.config('--global', 'user.email', os.environ['INPUT_GIT_USER_EMAIL'])

release_notes = ""
for rnf in release_notes_files:
  release_notes += open(rnf, 'r').read().rstrip() + '\n\n'
next_release_notes = open('.release-notes/next-release.md', 'a+')
next_release_notes.write(release_notes)
next_release_notes.close()

print(INFO + "Adding git changes." + ENDC)
for rnf in release_notes_files:
  git.rm(rnf)
git.add('.release-notes/next-release.md')
git.commit('-m', "Updating release notes for PR #" + str(pr_id)+ " [skip-ci]")

print(INFO + "Pushing updated release notes." + ENDC)
git.push()
