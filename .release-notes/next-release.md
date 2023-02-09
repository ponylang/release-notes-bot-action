## Handle GitHub secondary rate limit failure

The release-notes-bot-action makes extensive use of the GitHub API. As such, it can trigger rate limits that cause a failure. We've found that it is rather easy when using the bot across a number of repositories to hit a "secondary rate limit failure". Basically that is "you are doing too many API calls at once".

The error is transient. If someone was to notice, they could restart the failed release-notes-bot run and it would work. However, that requires someone to notice.

With this release, we've added a retry for the one time we know that the limit can be triggered. If the rate limit is triggered, the bot will wait for 30 seconds before trying again. If it encounters 5 failures, it will give up and quit.

It is possible that we'll need to add similar returns around other GitHub API calls. If we do, additional updates will be made.

