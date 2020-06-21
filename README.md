# Release-notes-bot action

Automatically adds a new release notes entry to the upcoming release notes file once a PR is merged if a corresponding release notes addition file is present.

A repo must have a `.release-notes` directory and a `.release-notes/next-release.md` file for the action to work properly.

## Example workflow

```yml
name: Release Notes Bot

on:
  push:
    branches:
      - master
    paths-ignore:
      - .release-notes/next-release.md

jobs:
  release-notes-bot:
    runs-on: ubuntu-latest
    name: Update release notes
    steps:
      - name: Update
        uses: ponylang/release-notes-bot-action@0.1.0
        with:
          git_user_name: "Ponylang Main Bot"
          git_user_email: "ponylang.main@gmail.com"
        env:
          API_CREDENTIALS: ${{ secrets.GITHUB_TOKEN }}
```

Note, you do not need to create `GITHUB_TOKEN`. It is already provided by GitHub. You merely need to make it available to the release-notes-bot action.
