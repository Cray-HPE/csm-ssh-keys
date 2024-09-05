# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Dependencies
- CSM 1.6 moved to Kubernetes 1.24, so use client v24.x to ensure compatability
- Bump `tj-actions/changed-files` from 44 to 45 ([#61](https://github.com/Cray-HPE/csm-ssh-keys/pull/61))

## [1.6.2] - 2024-08-21
### Changed
- Change how RPM release value is determined

### Dependencies
- Bump `tj-actions/changed-files` from 42 to 44 ([#59](https://github.com/Cray-HPE/csm-ssh-keys/pull/59), [#60](https://github.com/Cray-HPE/csm-ssh-keys/pull/60))
- Simplify how latest stable `cfs-trust` patch version is determined

## [1.6.1] - 2024-02-22
### Dependencies
- Bump `cfs-trust` from 1.6 to 1.7 for CSM 1.6

## [1.6.0] - 2024-02-22
### Dependencies
- Bump `tj-actions/changed-files` from 37 to 42 ([#46](https://github.com/Cray-HPE/csm-ssh-keys/pull/46), [#48](https://github.com/Cray-HPE/csm-ssh-keys/pull/48), [#50](https://github.com/Cray-HPE/csm-ssh-keys/pull/50), [#51](https://github.com/Cray-HPE/csm-ssh-keys/pull/51), [#53](https://github.com/Cray-HPE/csm-ssh-keys/pull/53))
- Bump `actions/checkout` from 3 to 4 ([#47](https://github.com/Cray-HPE/csm-ssh-keys/pull/47))
- Bump `stefanzweifel/git-auto-commit-action` from 4 to 5 ([#49](https://github.com/Cray-HPE/csm-ssh-keys/pull/49))
- Bump `kubernetes` from 12.0.1 to 22.6.0 to match CSM 1.6 Kubernetes version

## [1.5.6] - 2023-08-14
### Changed
- RPM OS type changed to `noos`. (CASMCMS-8691)
- Update Python module to reflect that Docker Alpine image is using Python 3.9
- Disabled concurrent Jenkins builds on same branch/commit
- Added build timeout to avoid hung builds

## [1.5.5] - 2023-07-24
### Dependencies
- Use `update_external_versions` to get latest patch version of `cfs-ssh-trust` Python module.
- Bumped depndency patch versions
| Package                  | From    | To       |
|--------------------------|---------|----------|
| `cachetools`             | 4.2.1   | 4.2.4    |
| `oauthlib`               | 3.1.0   | 3.1.1    |
| `python-dateutil`        | 2.8.1   | 2.8.2    |
| `requests-oauthlib`      | 1.3.0   | 1.3.1    |
| `rsa`                    | 4.7     | 4.7.2    |
| `urllib3`                | 1.26.3  | 1.26.16  |

## [1.5.4] - 2023-07-18
### Dependencies
- Bump `PyYAML` from 5.4.1 to 6.0.1 to avoid build issue caused by https://github.com/yaml/pyyaml/issues/601

## [1.5.3] - 2023-06-21
### Added
- Support for SLES SP5

## [1.5.2] - 2023-05-26
### Changed
- Enabled building of unstable artifacts
- Updated header of update_versions.conf to reflect new tool options

### Fixed
- Update Chart with correct image version strings during builds.
- Fixed authorized_keys file permissions

### Removed
- Removed defunct files leftover from previous versioning system

## [1.5.1] - 2022-12-20
### Added
- Add Artifactory authentication to Jenkinsfile
- Authenticate to CSM's artifactory

## [1.5.0] - 2022-07-14
### Added
- Support for SLES SP4

### Changed
- Convert to gitflow/gitversion.
