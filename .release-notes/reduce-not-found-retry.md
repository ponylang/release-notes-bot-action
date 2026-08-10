## Reduce retry delay when PR isn't immediately available

The bot previously used exponential backoff when a merged PR wasn't immediately available in the GitHub search API, waiting up to 5 minutes across 5 retries. The delay is now two retries at 15 and 30 seconds. The longer exponential backoff still applies to rate limit and connection errors.
