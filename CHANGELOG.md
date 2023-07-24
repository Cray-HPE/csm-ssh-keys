# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Dependencies
- Use `update_external_versions` to get latest patch version of `cfs-ssh-trust` Python module.

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
