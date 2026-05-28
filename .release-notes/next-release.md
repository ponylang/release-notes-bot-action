## Fix intermittent crash when looking up the PR for a commit

The bot could fail with an internal error while searching for the pull request associated with a commit when the GitHub API returned an unexpected response. The lookup now handles those response cases gracefully and the bot retries instead of crashing.

