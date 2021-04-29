# Release-notes-bot action

Automatically adds a new release notes entry to the upcoming release notes file once a PR is merged if a corresponding release notes addition file is present and a changelog label was applied to the PR.

Valid changelog labels are:

- changelog - added
- changelog - changed
- changelog - fixed

If no changelog label was applied to the PR, any release notes files in the PR will be deleted.

A repo must have a `.release-notes` directory and a `.release-notes/next-release.md` file for the action to work properly.

To prompt contributors to add release notes, see the [release-notes-reminder-bot-action](https://github.com/ponylang/release-notes-reminder-bot-action).

## Example workflow

```yml
name: Release Notes Bot

on:
  push:
    branches:
      - '**'
    tags-ignore:
      - '**'
    paths-ignore:
      - .release-notes/next-release.md
      - .release-notes/\d+.\d+.\d+.md

jobs:
  release-notes-bot:
    runs-on: ubuntu-latest
    name: Update release notes
    steps:
      - name: Update
        uses: docker://ponylang/release-notes-bot-action:0.3.4
        with:
          git_user_name: "Ponylang Main Bot"
          git_user_email: "ponylang.main@gmail.com"
        env:
          API_CREDENTIALS: ${{ secrets.GITHUB_TOKEN }}
```

Note, you do not need to create `GITHUB_TOKEN`. It is already provided by GitHub. You merely need to make it available to the release-notes-bot action.
