# Changelog

All notable changes to the ODIN project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Restructured repository as monorepo with `packages/plugin` and `packages/backend`
- Reorganized documentation into `docs/` directory
- Created `devlog/` for detailed development history
- Improved documentation structure and navigation

## [2.0.0] - 2025-11-02

### Added
- Integrated BOR backend directly into repository
- Complete Docker Compose setup for all services
- Comprehensive documentation (README, QUICKSTART, TESTING, CONTRIBUTING)
- Automated setup verification script (`test-setup.sh`)
- `.env.example` with all configuration options
- Development log system for tracking design decisions

### Fixed
- Backend Python dependencies (added `langchain-community` and `langchain-openai`)
- Docker container orchestration for monorepo structure

### Changed
- Converted from frontend-only repository to full monorepo
- Updated all documentation to reflect monorepo structure
- Reorganized project structure with `packages/` directory

## [1.x.x] - Previous Versions

Previous versions of ODIN were distributed as separate plugin and backend repositories.
For historical information, see:
- Plugin: https://github.com/memgraph/odin (original)
- Backend: https://github.com/memgraph/bor (original)

---

## Version History Notes

### Versioning Strategy

- **Major versions** (x.0.0): Breaking changes, major architectural changes
- **Minor versions** (0.x.0): New features, non-breaking changes
- **Patch versions** (0.0.x): Bug fixes, documentation updates

### Release Process

1. Update this CHANGELOG.md with all changes
2. Update version in `packages/plugin/manifest.json`
3. Update version in `packages/plugin/package.json`
4. Tag release in git: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
5. Push tag: `git push origin vX.Y.Z`

### Documentation of Changes

For detailed implementation notes and design decisions behind major changes, 
see the [development log](devlog/).

---

**Note:** This changelog focuses on user-facing changes. For technical implementation
details and development history, see the `devlog/` directory.

