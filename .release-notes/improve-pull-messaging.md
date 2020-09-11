## Improve logging around multiple push attempts

Previously, if the bot failed to push its updates, it would create a log message for each pull that it attempted but only for the first push. This could be confusing to the user.

Now each push and pull attempt will be logged.
