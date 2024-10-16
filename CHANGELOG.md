# Change Log

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a CHANGELOG](http://keepachangelog.com/).

## [unreleased] - unreleased

### Fixed


### Added


### Changed


## [0.3.8] - 2024-10-16

### Fixed

- Handle Additional GitHub secondary rate limit failure ([PR #60](https://github.com/ponylang/release-notes-bot-action/pull/60))

### Changed

- Update base image to Alpine 3.18 ([PR #50](https://github.com/ponylang/release-notes-bot-action/pull/50))

## [0.3.7] - 2023-04-22

### Fixed

- Fix bug when release notes files appeared in more than one commit ([PR #40](https://github.com/ponylang/release-notes-bot-action/pull/40))

## [0.3.6] - 2023-02-09

### Added

- Add sleep and retry when secondary rate limit impacts on PR search ([PR #38](https://github.com/ponylang/release-notes-bot-action/pull/38))

## [0.3.5] - 2022-07-12

### Fixed

- Update to work with newer versions of git ([PR #33](https://github.com/ponylang/release-notes-bot-action/pull/33))

### Changed

- Update base image ([PR #35](https://github.com/ponylang/release-notes-bot-action/pull/35))

## [0.3.4] - 2021-04-29

### Fixed

- Improve logging around multiple push attempts ([PR #27](https://github.com/ponylang/release-notes-bot-action/pull/27))
- Fix build error caused by PyGitHub version dependencies changing ([PR #28](https://github.com/ponylang/changelog-bot-action/pull/28))

### Added

- Create images on release ([PR #29](https://github.com/ponylang/release-notes-bot-action/pull/29))

## [0.3.3] - 2020-09-10

### Changed

- Rebase on pull ([PR #26](https://github.com/ponylang/release-notes-bot-action/pull/26))

## [0.3.2] - 2020-08-31

### Fixed

- Fix broken push retries ([PR #25](https://github.com/ponylang/release-notes-bot-action/pull/25))

## [0.3.1] - 2020-08-30

### Fixed

- Fix broken push retries ([PR #24](https://github.com/ponylang/release-notes-bot-action/pull/24))

## [0.3.0] - 2020-08-26

### Changed

- Turn on branch.autorebasesetup when pushing/pulling ([PR #22](https://github.com/ponylang/release-notes-bot-action/pull/22))

## [0.2.0] - 2020-08-15

### Fixed

- Only get release notes from added files ([PR #8](https://github.com/ponylang/release-notes-bot-action/pull/8))
- Support multiple release-notes entry files in a single PR ([PR #9](https://github.com/ponylang/release-notes-bot-action/pull/9))

### Added

- Retry if an error is encountered while pushing updating release notes ([PR #12](https://github.com/ponylang/release-notes-bot-action/pull/12))
- Add ability to work with branches other than the default branch ([PR #18](https://github.com/ponylang/release-notes-bot-action/pull/18))

### Changed

- Pull latest changes before pushing ([PR #10](https://github.com/ponylang/release-notes-bot-action/pull/10))
- Only update release notes if associated PR had changelog label ([PR #17](https://github.com/ponylang/release-notes-bot-action/pull/17))

## [0.1.0] - 2020-06-21

### Added

- Initial release

