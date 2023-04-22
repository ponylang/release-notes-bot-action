## Fix a failure when release notes appear in more than one commit

If more than 1 commit was associated with a PR and more than one commit included the same release notes file, this actual would previously fail.

We've updated to make sure it only processes each file once as compared to before when it would attempt to process each release notes file for every occurrence across all commits.

You can also call this fix: "use set, not list".

