# Release-notes-bot action

Automatically adds a new release notes entry to once a PR is merged. Two conditions must be met for the action to trigger.

* One of 3 labels must be applied to the PR in order for a release entry to be added:
  - changelog - added
  - changelog - fixed
  - changelog - changed
* A release notes addition file must be part a commit for the PR.


## Example workflow

```yml
name: Release Notes Bot

on:
  push:
    paths-ignore:
      - .release-notes/next-release.md

jobs:
  release-notes-bot:
    runs-on: ubuntu-latest
    name: Update release notes
    steps:
      - name: Update
        uses: ponylang/release-notes-bot-action@initial
        with:
          git_user_name: "Ponylang Main Bot"
          git_user_email: "ponylang.main@gmail.com"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Note, you do not need to create `GITHUB_TOKEN`. It is already provided by GitHub. You merely need to make it available to the release-notes-bot action.
