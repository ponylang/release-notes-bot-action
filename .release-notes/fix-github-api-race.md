## Fix GitHub API race condition when finding PR for a commit

The bot could fail to find a PR associated with a commit if the GitHub search API hadn't finished indexing the merge yet. The bot now retries up to 5 times with a 10-second delay before concluding there's no associated PR.
