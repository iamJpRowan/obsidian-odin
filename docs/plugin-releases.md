# Plugin Release Guide

Guide for releasing new versions of the ODIN plugin following Obsidian's official release guidelines.

## Prerequisites Checklist

- [ ] On the `main` branch with all changes committed
- [ ] Plugin builds successfully locally
- [ ] All features tested in development vault
- [ ] Write access to the repository
- [ ] npm installed and dependencies up to date

## Quick Release

```bash
cd packages/plugin

# For bug fixes (1.0.0 → 1.0.1)
npm run release

# For new features (1.0.0 → 1.1.0)
npm run release:minor

# For breaking changes (1.0.0 → 2.0.0)
npm run release:major
```

## Release Workflow

### Step 1: Test Locally

```bash
cd packages/plugin
npm run dev
```

Test thoroughly in your development vault:
- [ ] All features work as expected
- [ ] No console errors (open DevTools: `Cmd+Option+I` or `Ctrl+Shift+I`)
- [ ] Plugin loads correctly
- [ ] UI components render properly
- [ ] Backend API calls succeed

### Step 2: Create Release

Choose the appropriate release type:

```bash
cd packages/plugin

# Patch release (bug fixes only)
npm run release

# Minor release (new features, backwards compatible)
npm run release:minor

# Major release (breaking changes)
npm run release:major
```

### Step 3: Automated Process

When you run a release command, this happens automatically:

1. **`npm version`** - Increments version in `package.json`
2. **version-bump.mjs** - Updates `manifest.json` and `versions.json`
3. **Git commit** - Creates commit with version bump
4. **Git tag** - Creates tag (e.g., `v1.0.1`)
5. **Git push** - Pushes commits and tags to GitHub
6. **GitHub Actions** - Detects tag and:
   - Checks out code
   - Installs dependencies
   - Builds plugin (`main.js`)
   - Creates draft release with artifacts

### Step 4: Finalize on GitHub

1. Go to your repository's [Releases page](https://github.com/your-username/your-repo/releases)
2. Find the draft release created by GitHub Actions
3. Edit the release notes (see [Release Notes Template](#release-notes-template))
4. Click **Publish release**

### Step 5: Submit to Obsidian (First Release Only)

For your first public release, submit to the Obsidian Community Plugins directory:

1. Fork [obsidian-releases](https://github.com/obsidianmd/obsidian-releases)
2. Add your plugin to `community-plugins.json`:
   ```json
   {
     "id": "ODIN",
     "name": "ODIN",
     "author": "Your Name",
     "description": "Using graphs to find structure in unstructured data",
     "repo": "your-username/obsidian-odin"
   }
   ```
3. Submit a pull request
4. Wait for Obsidian team review

See [Obsidian's submission guide](https://docs.obsidian.md/Plugins/Releasing/Submit+your+plugin) for details.

## Semantic Versioning

Follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

### PATCH (0.0.X) - Bug Fixes
- Bug fixes
- Performance improvements
- Minor UI tweaks
- Documentation updates
- No new features

**Example:** `1.2.3 → 1.2.4`

### MINOR (0.X.0) - New Features
- New features (backwards compatible)
- New configuration options
- Non-breaking API additions
- Deprecations (with warnings)

**Example:** `1.2.4 → 1.3.0`

### MAJOR (X.0.0) - Breaking Changes
- Breaking API changes
- Removal of features
- Major architectural changes
- Changes requiring user migration
- Minimum Obsidian version increase (major bump)

**Example:** `1.3.0 → 2.0.0`

## Files Updated Automatically

The release process updates these files:

| File | Purpose | Updated By |
|------|---------|------------|
| `package.json` | npm version | `npm version` command |
| `manifest.json` | Plugin version (Obsidian reads this) | `version-bump.mjs` script |
| `versions.json` | Version compatibility matrix | `version-bump.mjs` script |

**Example `versions.json`:**
```json
{
  "1.0.0": "0.15.0",
  "1.0.1": "0.15.0",
  "1.1.0": "0.15.0",
  "2.0.0": "0.16.0"
}
```

Key = plugin version, Value = minimum Obsidian version required

## Release Notes Template

Good release notes help users understand changes:

```markdown
## v1.2.0 - 2025-11-02

### ✨ New Features
- Added graph visualization filtering by date range
- Implemented keyboard shortcuts (see [docs](link))
- Support for custom node colors in graph

### 🚀 Improvements
- Graph rendering 3x faster for large vaults (1000+ notes)
- Improved error messages when backend is unreachable
- Better handling of special characters in note names

### 🐛 Bug Fixes
- Fixed crash when processing notes with emoji in titles
- Graph nodes now update correctly when notes are renamed
- Resolved memory leak in graph rendering

### ⚠️ Breaking Changes
- Configuration format changed: see [migration guide](link)
- Minimum Obsidian version is now 0.16.0
- Removed deprecated `oldFeature` API (use `newFeature` instead)

### 📚 Documentation
- Added [Plugin Development Guide](docs/plugin-development.md)
- Updated API examples
```

## Troubleshooting

### Release Failed in GitHub Actions

**Check the logs:**
1. Go to repository **Actions** tab
2. Find the failed workflow
3. Review error messages

**Common fixes:**
```bash
# Delete the failed tag
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# Fix the issue locally
# Then try releasing again
npm run release
```

### Wrong Version Number

**To undo a release:**
```bash
# Delete tag locally and remotely
git tag -d v1.0.1
git push origin :refs/tags/v1.0.1

# Delete GitHub release in UI

# Reset versions in files
# Edit package.json, manifest.json, versions.json
# Commit the corrections

# Release again with correct version
npm run release
```

### Build Works Locally But Fails in CI

**Common issues:**

1. **Missing dependencies**
   ```bash
   # Ensure all deps are in package.json
   npm install --save missing-package
   ```

2. **Node version mismatch**
   ```bash
   # GitHub Actions uses Node 18.x
   nvm use 18
   npm run build  # Test locally
   ```

3. **Path issues**
   - Workflow uses `working-directory: packages/plugin`
   - Ensure paths in scripts are relative to plugin directory

4. **Environment variables**
   - Don't rely on `.env` for builds
   - `.env` is only for local development

### Plugin Not Loading in Obsidian

**Check console for errors:**
1. Open Obsidian DevTools (`Cmd+Option+I` or `Ctrl+Shift+I`)
2. Look for red error messages
3. Check that plugin loads without exceptions

**Verify required files:**
```bash
cd /path/to/vault/.obsidian/plugins/ODIN
ls -la
# Should show:
# - main.js
# - manifest.json
# - styles.css (optional)
```

**Validate manifest.json:**
```bash
cat manifest.json | jq .  # Pretty-print and validate JSON
```

### Development Mode Not Copying

**Check .env configuration:**
```bash
cd packages/plugin
cat .env

# Should contain:
# OBSIDIAN_VAULT_PATH=/path/to/your/vault
# PLUGIN_ID=ODIN
```

**Verify vault path:**
```bash
# Path should exist and be writable
ls -la /path/to/your/vault/.obsidian/plugins/
```

**Restart dev server:**
```bash
# Stop current process (Ctrl+C)
npm run dev
```

## Best Practices

### Pre-Release Checklist

- [ ] All features tested thoroughly
- [ ] No console errors in DevTools
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated
- [ ] Remove any `console.log` debugging statements
- [ ] Check TypeScript compilation (`npx tsc -noEmit`)
- [ ] Test with minimum Obsidian version

### Version Numbering Decision Tree

```
Did you break backwards compatibility?
├─ Yes → MAJOR version
└─ No → Did you add new features?
    ├─ Yes → MINOR version
    └─ No → PATCH version
```

### Minimum Obsidian Version

Update `minAppVersion` in `manifest.json` when using new Obsidian APIs:

```json
{
  "id": "ODIN",
  "minAppVersion": "0.16.0"
}
```

Check [Obsidian API Changelog](https://github.com/obsidianmd/obsidian-api/blob/master/CHANGELOG.md) for version requirements.

## GitHub Actions Configuration

The release workflow is in `.github/workflows/release.yml`:

```yaml
name: Release Obsidian Plugin

on:
  push:
    tags:
      - "*"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18.x"
      - name: Build plugin
        working-directory: packages/plugin
        run: |
          npm install
          npm run build
      - name: Create release
        run: |
          gh release create "$tag" --draft \
            packages/plugin/main.js \
            packages/plugin/manifest.json \
            packages/plugin/styles.css
```

This runs automatically when you push a tag via `npm run release`.

## Resources

- **[Obsidian Release Guide](https://docs.obsidian.md/Plugins/Releasing/Release+your+plugin+with+GitHub+Actions)** - Official documentation
- **[Plugin Submission](https://docs.obsidian.md/Plugins/Releasing/Submit+your+plugin)** - How to submit to community plugins
- **[Obsidian API](https://github.com/obsidianmd/obsidian-api)** - API documentation and changelog
- **[Semantic Versioning](https://semver.org/)** - Versioning specification
- **[Plugin Development](plugin-development.md)** - Local development setup

## Quick Command Reference

```bash
# Setup (first time)
cd packages/plugin
npm install
npm run setup:vault

# Development
npm run dev              # Watch mode with hot-reload

# Production build
npm run build            # Build without copying to vault

# Releases
npm run release          # Patch (1.0.0 → 1.0.1)
npm run release:minor    # Minor (1.0.0 → 1.1.0)
npm run release:major    # Major (1.0.0 → 2.0.0)
```

---

For issues with the release process, open an issue on GitHub or see the [main documentation](README.md).

