## Improve resilience to GitHub API failures

When multiple repositories merge PRs at the same time, the bot could crash because GitHub drops connections instead of returning an error response. The bot now catches connection errors, staggers its start with a random delay to spread out concurrent runs, and uses exponential backoff between retries.
