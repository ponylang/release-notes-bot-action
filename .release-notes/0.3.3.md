## Rebase on pull

Prior to this change, the release-notes-bot would sometimes create a merge commit when pushing changes if it had to pull down other changes first. We now set `--rebase` when doing pulls to avoid muddying up the history.

