## Retry on connection errors for all GitHub API calls

API calls outside the search loop (fetching the repo, commits, and pull request) could still crash on connection errors or rate limits. All GitHub API calls now retry with exponential backoff.
