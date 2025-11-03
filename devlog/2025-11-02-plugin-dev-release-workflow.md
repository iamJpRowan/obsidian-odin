---
date: 2025-11-02
title: Plugin Development and Release Workflow Setup
contributors:
  human:
    name: jprowan
    role: lead_developer
  ai:
    model: Claude Sonnet 4.5
    provider: Anthropic
    interface: Cursor IDE
collaboration:
  style: pair_programming
  human_focus: requirements definition, workflow decisions, validation
  ai_focus: implementation, configuration, documentation writing
duration_hours: 1.5
tags: [plugin, development, release-automation, github-actions, obsidian, documentation]
---

# Plugin Development and Release Workflow Setup

## Collaboration Summary

**Human Developer:** jprowan  
**AI Assistant:** Claude Sonnet 4.5 (Anthropic)  
**Development Environment:** Cursor IDE  
**Session Date:** 2025-11-02  
**Duration:** ~1.5 hours  
**Collaboration Style:** AI-driven implementation with human oversight and requirements definition

---

## Context

The ODIN plugin needed a professional development workflow that would:
1. Enable fast iteration during development with automatic hot-reload to the developer's vault
2. Follow Obsidian's official plugin release guidelines
3. Automate the release process with GitHub Actions
4. Support team development with environment-based configuration

**Goal:** Create a complete development and release setup that allows developers to work efficiently and release updates professionally.

## What We Accomplished

### 1. Development Environment Setup

#### Environment Configuration
- **`.env.example`** - Template for vault configuration
- **`.gitignore`** - Prevents build artifacts and `.env` from being committed
- **Environment variable support** - Each developer can specify their own vault path

#### Enhanced Build System
Updated `esbuild.config.mjs` with:
- **Vault path resolution** - Reads from `.env` file
- **Auto-copy plugin** - Copies built files to vault automatically
- **Directory creation** - Ensures `.obsidian/plugins/ODIN/` exists
- **Helpful logging** - Shows build status and copy confirmations
- **Development-only copying** - Production builds don't copy to vault

#### New npm Scripts
Added to `package.json`:
```bash
npm run setup:vault      # Creates .env from template
npm run release          # Patch version (1.0.0 → 1.0.1)
npm run release:minor    # Minor version (1.0.0 → 1.1.0)
npm run release:major    # Major version (1.0.0 → 2.0.0)
```

#### Plugin Styles
Created `styles.css` - Base stylesheet for plugin (required for releases)

### 2. Release Automation

#### GitHub Actions Workflows

**.github/workflows/release.yml** - Automated releases:
- Triggers on git tags (created by `npm run release`)
- Builds plugin with production settings
- Creates draft GitHub release
- Attaches `main.js`, `manifest.json`, and `styles.css`

**.github/workflows/test.yml** - CI testing:
- Runs on pushes to main/develop branches
- Type checks TypeScript code
- Builds plugin to verify no errors
- Validates build output exists

Both workflows use Node.js 18.x and respect the monorepo structure (`working-directory: packages/plugin`).

### 3. Comprehensive Documentation

#### Plugin-Specific Documentation
- **`packages/plugin/DEV-SETUP.md`** - Quick start guide for plugin development
- **`packages/plugin/SETUP-COMPLETE.md`** - Summary of all changes made

#### Project Documentation
- **`docs/plugin-development.md`** - Complete development guide
  - Setup instructions
  - Development workflow
  - Project structure
  - Troubleshooting
  - React/TypeScript patterns
  
- **`docs/plugin-releases.md`** - Complete release guide
  - Release process steps
  - Semantic versioning guidelines
  - GitHub Actions configuration
  - Troubleshooting
  - Best practices

- **`docs/README.md`** - Updated to include new guides

#### Development Log
- **`devlog/2025-11-02-plugin-dev-release-workflow.md`** - This file
- **`devlog/README.md`** - Updated index with this entry

### 4. Package Dependencies

Added `dotenv` to `devDependencies` for environment variable support.

## Key Decisions

| Decision | Made By | Rationale |
|----------|---------|-----------|
| Use `.env` for vault path | jprowan | Allows each developer to use their own vault without conflicts |
| Auto-copy only in dev mode | AI (Claude) | Production builds shouldn't modify user's filesystem |
| Follow Obsidian's official guidelines | jprowan | Ensures professional releases and compatibility with community plugins |
| Use GitHub Actions for releases | Joint decision | Industry standard, free for public repos, well-documented |
| Create draft releases | AI (Claude) | Allows human review/editing of release notes before publishing |
| Match existing docs structure | jprowan | Maintains consistency with monorepo documentation style |
| Semantic versioning scripts | AI (Claude) | Makes version bumping foolproof and consistent |

## Development Workflow

### Before This Setup

```
1. Edit code in src/
2. Run npm run build
3. Manually copy files to vault
4. Reload Obsidian
5. Repeat for every change
```

### After This Setup

```
1. Run npm run dev once
2. Edit code in src/
3. Save file (auto-rebuilds and copies)
4. Press Cmd+R in Obsidian
5. See changes instantly!
```

### Release Workflow

**Before:**
- Manual version updates in multiple files
- Manual git tagging
- Manual release creation
- Manual file uploads

**After:**
```bash
npm run release  # Everything automated!
```

## Technical Details

### esbuild Configuration

The custom `copy-to-vault` plugin in `esbuild.config.mjs`:

```javascript
{
  name: "copy-to-vault",
  setup(build) {
    build.onEnd(async (result) => {
      if (!vaultPluginDir || prod) return;
      
      if (result.errors.length > 0) {
        console.error("❌ Build failed, not copying to vault");
        return;
      }

      // Copy main.js, manifest.json, styles.css
      fs.copyFileSync("main.js", path.join(vaultPluginDir, "main.js"));
      fs.copyFileSync("manifest.json", path.join(vaultPluginDir, "manifest.json"));
      // ... etc
    });
  },
}
```

This runs after every successful build in dev mode, automatically copying the required files to the vault.

### Version Management

The `version-bump.mjs` script (already existed) integrates with npm version hooks:

1. `npm version patch` runs
2. Updates `package.json` version
3. Triggers `version` script in `package.json`
4. Runs `version-bump.mjs`
5. Updates `manifest.json` and `versions.json`
6. Commits changes and creates tag
7. Pushes to GitHub (new: added by release scripts)

### GitHub Actions Triggers

Release workflow triggers on any tag push:
```yaml
on:
  push:
    tags:
      - "*"
```

Test workflow triggers on branch pushes:
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
```

## AI Contribution Notes

**Claude Sonnet 4.5** provided:

**Implementation:**
- esbuild configuration enhancements
- GitHub Actions workflow creation
- npm scripts for release automation
- Environment variable setup

**Documentation:**
- Complete development guide
- Complete release guide
- Quick-start guides
- Troubleshooting sections
- This devlog entry

**Research:**
- Obsidian plugin release best practices
- GitHub Actions patterns for monorepos
- Semantic versioning guidelines
- esbuild plugin system

**Capabilities Leveraged:**
- File write operations across multiple directories
- Understanding of monorepo structure from earlier session
- Multi-language fluency (TypeScript, Bash, YAML, Markdown)
- Documentation generation matching existing style
- Web search for Obsidian's official guidelines

**Limitations Encountered:**
- No npm in sandbox (user will need to run `npm install`)
- Required manual approval for file writes
- Could not test the actual workflow end-to-end

## Human Contribution Notes

**jprowan** provided:

**Requirements:**
- Need for fast development iteration
- Requirement to follow Obsidian's official guidelines
- Preference for automatic file copying during development
- Desire for professional release automation

**Decisions:**
- Confirmed using `.env` for developer-specific configuration
- Validated the proposed workflow structure
- Approved GitHub Actions approach
- Requested documentation match existing style

**Validation:**
- Will test the development workflow with actual vault
- Will verify GitHub Actions on first release
- Ensured documentation fits project structure

## Challenges and Solutions

### Challenge 1: Vault Path Configuration
**Problem:** Each developer needs to build to their own vault, but can't commit vault paths to git.

**Solution:** Use `.env` file (gitignored) with `.env.example` template. Added `setup:vault` script to create `.env` from template easily.

### Challenge 2: Monorepo Structure in GitHub Actions
**Problem:** GitHub Actions workflows need to work with packages/plugin subdirectory.

**Solution:** Use `working-directory: packages/plugin` in workflow steps. This keeps workflows clean and explicit about location.

### Challenge 3: Draft vs Published Releases
**Problem:** Automatic releases could publish before human review of release notes.

**Solution:** Use `--draft` flag in `gh release create`. Human must manually publish after adding release notes.

### Challenge 4: Documentation Organization
**Problem:** Plugin-specific docs needed to fit into existing docs structure.

**Solution:** 
- Quick guides in `packages/plugin/` for immediate reference
- Comprehensive guides in `docs/` for project-wide accessibility
- Updated `docs/README.md` to include new guides
- Created devlog entry following established template

## Files Created/Modified

### Created
```
packages/plugin/
├── .env.example           # Vault path template
├── .gitignore            # Ignore build outputs and .env
├── styles.css            # Plugin styles
├── DEV-SETUP.md          # Quick development guide
└── SETUP-COMPLETE.md     # Summary of changes

.github/workflows/
├── release.yml           # Automated releases
└── test.yml              # CI testing

docs/
├── plugin-development.md # Comprehensive dev guide
└── plugin-releases.md    # Comprehensive release guide

devlog/
└── 2025-11-02-plugin-dev-release-workflow.md  # This file
```

### Modified
```
packages/plugin/
├── esbuild.config.mjs    # Added vault copying
└── package.json          # Added scripts and dotenv

docs/
└── README.md             # Added new doc links

devlog/
└── README.md             # Added entry to index
```

## Testing Status

### ✅ Configuration Created
- [x] `.env.example` template exists
- [x] `.gitignore` excludes build files
- [x] GitHub Actions workflows created
- [x] Documentation written and organized

### ⏭️ Requires User Testing
- [ ] Run `npm install` to get dotenv package
- [ ] Run `npm run setup:vault` and configure vault path
- [ ] Test `npm run dev` with actual vault
- [ ] Verify files copy to vault correctly
- [ ] Test hot-reload workflow in Obsidian
- [ ] Create test release to verify GitHub Actions

### ⏭️ First Release Testing
- [ ] Run `npm run release` for test release
- [ ] Verify GitHub Action builds successfully
- [ ] Confirm draft release created
- [ ] Check artifacts attached correctly
- [ ] Test publishing process

## Documentation Structure (Final)

```
docs/
├── README.md                 # Updated index
├── quickstart.md            # Existing: 5-minute setup
├── contributing.md          # Existing: general contribution guide
├── testing.md               # Existing: testing instructions
├── docker-build.md          # Existing: Docker management
├── plugin-development.md    # NEW: Plugin dev setup
└── plugin-releases.md       # NEW: Plugin release workflow

packages/plugin/
├── DEV-SETUP.md            # NEW: Quick dev guide
└── SETUP-COMPLETE.md       # NEW: Summary of changes

devlog/
├── README.md               # Updated with this entry
├── 2025-11-02-monorepo-setup.md         # Previous entry
└── 2025-11-02-plugin-dev-release-workflow.md  # This entry
```

## Benefits of This Setup

### For Individual Developers
- ✅ Fast iteration (save → reload)
- ✅ No manual file copying
- ✅ Personal vault configuration
- ✅ Clear error messages
- ✅ Source maps for debugging

### For Teams
- ✅ Consistent development environment
- ✅ Standardized release process
- ✅ Automated CI testing
- ✅ Clear documentation
- ✅ Easy onboarding

### For Users
- ✅ Professional releases
- ✅ Proper versioning
- ✅ Reliable builds
- ✅ GitHub integration
- ✅ Follows Obsidian standards

## Future Considerations

### Potential Enhancements
- Add automated testing (unit tests, integration tests)
- Create example vault configurations
- Add pre-commit hooks for code quality
- Set up Prettier/ESLint automation
- Add release note templates
- Create release checklist automation

### Documentation Improvements
- Add video walkthrough of development setup
- Create animated GIFs of hot-reload workflow
- Add more React/TypeScript examples
- Document common plugin patterns
- Add debugging tips and tricks

### Workflow Improvements
- Consider automated release notes from commits
- Add semantic-release for fully automated versioning
- Set up branch protection rules
- Add code review requirements
- Create issue/PR templates

## Success Metrics

- ✅ Complete development environment configured
- ✅ Automatic file copying implemented
- ✅ GitHub Actions workflows created
- ✅ Comprehensive documentation written
- ✅ Documentation matches existing style
- ✅ Devlog entry created
- ✅ All TODOs completed
- ⏭️ User testing pending (requires npm install)

## Related Resources

### Official Documentation
- **[Obsidian Release Guide](https://docs.obsidian.md/Plugins/Releasing/Release+your+plugin+with+GitHub+Actions)** - Referenced for workflow design
- **[Obsidian Plugin API](https://github.com/obsidianmd/obsidian-api)** - API reference
- **[Semantic Versioning](https://semver.org/)** - Versioning standard

### Project Documentation
- **[Plugin Development Guide](../docs/plugin-development.md)** - How to develop
- **[Plugin Release Guide](../docs/plugin-releases.md)** - How to release
- **[Previous Devlog](2025-11-02-monorepo-setup.md)** - Monorepo setup

### Tools and Libraries
- **[esbuild](https://esbuild.github.io/)** - JavaScript bundler
- **[dotenv](https://www.npmjs.com/package/dotenv)** - Environment variables
- **[GitHub Actions](https://docs.github.com/en/actions)** - CI/CD platform

## Commands Reference

### Setup (One Time)
```bash
cd packages/plugin
npm install
npm run setup:vault
# Edit .env with your vault path
```

### Daily Development
```bash
npm run dev
# Edit files in src/
# Save → auto-rebuild → Cmd+R in Obsidian
```

### Releases
```bash
npm run release          # Patch: 1.0.0 → 1.0.1
npm run release:minor    # Minor: 1.0.0 → 1.1.0
npm run release:major    # Major: 1.0.0 → 2.0.0
```

## What Makes This Professional

1. **Follows Official Guidelines** - Uses Obsidian's recommended workflow
2. **Automated CI/CD** - GitHub Actions for testing and releases
3. **Semantic Versioning** - Proper version management
4. **Draft Releases** - Human review before publishing
5. **Comprehensive Docs** - Matching project documentation style
6. **Developer Experience** - Fast iteration with hot-reload
7. **Team-Friendly** - Per-developer configuration
8. **Git Integration** - Proper tagging and history

---

**Attribution:** This work represents a collaboration between jprowan (human developer) providing requirements, workflow decisions, and validation, and Claude Sonnet 4.5 (AI assistant via Cursor IDE) assisting with implementation, configuration, documentation generation, and research. All strategic decisions were made by the human; AI provided execution and technical recommendations subject to human approval.

