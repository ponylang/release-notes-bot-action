## Improve logging around multiple push attempts

Previously, if the bot failed to push its updates, it would create a log message for each pull that it attempted but only for the first push. This could be confusing to the user.

Now each push and pull attempt will be logged.

## Fix build error coming from PyGitHub dependency

With the release of a new version of PyGitHub, the pynacl dependency changed and no longer builds. We are fine using the previous version of PyGitHub so this update pins us to that version. If we need to upgrade in the future, we'll need to fix the "can't build pynacl" issue.
