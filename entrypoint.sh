#!/bin/bash


// FLOW WE NEED --> on push to master...
// CHECK TO SEE IF THERE IS AN ASSOCIATED PR (via search)
// EXIT IF NO
// CHECK TO SEE IF PR HAS CHANGELOG label
// EXIT IF NO
// GITHUB_EVENT_PATH get commits
// FOREACH get sha, look up commit from commits url
// check files for release notes file
// IF/WHEN FOUND...
// get release notes content from `raw_url`
// add release notes to end of `next-release-notes.md`
// delete release notes addition from PR
// git add .release-notes/next-release.md

set -e

if [[ -z "${GITHUB_TOKEN}" ]]; then
  echo -e "\e[31mGITHUB_TOKEN needs to be set in env. Exiting."
  exit 1
fi

# Get commit SHA from PushEvent
SHA=$(jq -r '.head_commit.id' "${GITHUB_EVENT_PATH}")
REPO=$(jq -r '.repository.full_name' "${GITHUB_EVENT_PATH}")

# Search for merged PR featuring our SHA in our REPO
echo -e "\e[34mRunning changelog-bot for ${SHA} in ${REPO}"
PR_URL=$(curl -s "https://api.github.com/search/issues?q=is:merged+sha:${SHA}+repo:${REPO}" | jq -r '.items[].pull_request.url')

if [[ -z "${PR_URL}" ]]; then
  echo -e "\e[33mNo merged PR associated with ${SHA}. Exiting."
  exit 0
fi

# We have a PR url, let's fetch it.
echo -e "\e[34mFetching ${PR_URL}"
curl -s "${PR_URL}" >> pr.json

# Extract information from pull request
echo -e "\e[34mExtracting information from PR"
BASE_BRANCH=$(jq -r '.base.ref' pr.json)
PULL_REQUEST_TITLE=$(jq -r '.title' pr.json)
PULL_REQUEST_NUMBER=$(jq -r '.number' pr.json)
PR_HTML_URL=$(jq -r '.html_url' pr.json)
COMMIT_MESSAGE="Update CHANGELOG for PR #${PULL_REQUEST_NUMBER} [skip ci]"
CHANGELOG_ENTRY="${PULL_REQUEST_TITLE} ([PR #${PULL_REQUEST_NUMBER}](${PR_HTML_URL}))"

CHANGELOG_TYPES=$(
  jq -r '.labels | map(.name) | join("'"$IFS"'")' pr.json |
  grep 'changelog - ' |
  grep -o -E 'added|changed|fixed' ||
  true
)
# git setup
echo -e "\e[34mSetting up git configuration"
git config --global user.name "${INPUT_GIT_USER_NAME}"
git config --global user.email "${INPUT_GIT_USER_EMAIL}"

# create work directory
echo -e "\e[34mCreating temporary work directory in /tmp"
WORK_DIR=$(mktemp -d -p /tmp)
pushd "${WORK_DIR}" || exit 1

# clone repository
echo -e "\e[34mCloning ${BASE_BRANCH} of ${REPO} into ${WORK_DIR}"
git clone --depth=1 --branch="${BASE_BRANCH}" "https://${GITHUB_ACTOR}:${GITHUB_TOKEN}@github.com/${REPO}" .

# make sure we are up to date
echo -e "\e[34mPulling latest changes"
git pull

echo -e "\e[34mUpdating CHANGELOG.md"
for CHANGELOG_TYPE in $CHANGELOG_TYPES; do
  changelog-tool add "${CHANGELOG_TYPE}" "${CHANGELOG_ENTRY}" -e
done

# Checking to see if we need to commit
DIRTY=$(git status -s)

if [[ ${DIRTY} == "" ]]; then
  echo -e "\e[33mNo changes to CHANGELOG.md. Exiting."
  exit 0
fi

# Add CHANGELOG changes and commit
echo -e "\e[34mCommiting CHANGELOG.md changes"
git add CHANGELOG.md
git commit -m "$COMMIT_MESSAGE"

# push those changes son
echo -e "\e[34mPushing changes"
git push
