# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-21

### Added
- Command-line interface (CLI) with comprehensive testing infrastructure
- Protein analysis functionality with test coverage
- Project management system with `.labrat` folder support for project metadata
- Documentation structure including API, CLI, installation, and index pages
- Test documentation for contributors
- Comprehensive test suite covering:
  - CLI functionality
  - Math functions
  - Protein analysis
  - Archiver
  - File organizer
  - Project manager
- `jinja2-time` dependency for template functionality

### Changed
- PyPI package name changed from `labrat` to `pylabrat` to avoid naming conflicts
- Moved pull request template to `.github` folder for better organization

### Fixed
- Logic error in `dilute_stock` function
- Math function test failures
- Protein analysis implementation issues
- Various errors throughout the codebase
- Missing dependency declarations

### Improved
- Code comments and documentation throughout
- Test coverage and reliability
