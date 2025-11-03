# CI/CD Workflow and PR Status Checking

Guide for working with GitHub Actions CI/CD and checking PR status from within the IDE.

## Overview

This project uses GitHub CLI (`gh`) and local validation scripts to enable checking PR status and fixing issues without leaving the IDE. The AI assistant can now see test failures and fix them automatically!

## Prerequisites

- ✅ GitHub CLI (`gh`) installed
- ✅ Authenticated with GitHub
- ✅ Node.js and npm for running local checks

## Quick Reference

```bash
# Check PR status (with detailed CI results)
./scripts/check-pr-status.sh

# Run local validation before pushing
./scripts/pre-push-check.sh

# Create a PR from current branch
gh pr create --title "Your title" --body "Description"

# View failed check logs
gh run view --log-failed

# List recent workflow runs
gh run list --limit 5
```

## Available Scripts

### `scripts/check-pr-status.sh`

Checks the status of the PR for the current branch and displays:
- PR number and title
- All CI check statuses (✅ passed, ❌ failed, ⏳ in progress)
- Direct links to failed check details
- Suggestions for next steps

**Example output:**
```
🔍 Checking PR status...

📍 Current branch: feat-dev-build-vault-OBCbe
✓ Found PR #123

📝 Title: Add plugin development workflow
🔗 URL: https://github.com/user/repo/pull/123

🔄 CI Checks:
─────────────────────────────────────────
✅ Test Plugin Build: PASSED
✅ Release workflow: PASSED
─────────────────────────────────────────

✅ All checks passed!
```

### `scripts/pre-push-check.sh`

Runs the same checks locally that GitHub Actions will run:
- TypeScript type checking (`tsc -noEmit`)
- Production build test
- Verifies build output exists

**Use before pushing** to catch issues early!

**Example output:**
```
🔍 Running pre-push checks...

📦 Installing dependencies (if needed)...
✓ Dependencies ready

🔍 Running TypeScript type check...
✅ TypeScript: PASSED

🔨 Testing production build...
✅ Build: PASSED

✅ Build output verified

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All pre-push checks passed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Safe to push your changes
```

## Workflow: Making Changes with AI

### Ideal Workflow (What the AI Does)

```bash
# 1. AI makes changes to code
# ... edits files ...

# 2. AI runs local checks (prevents CI failures)
./scripts/pre-push-check.sh

# 3. If checks pass, AI commits and pushes
git add .
git commit -m "feat: your changes"
git push

# 4. AI checks PR status to see if CI passed
./scripts/check-pr-status.sh

# 5. If CI failed, AI checks the logs
gh run view --log-failed

# 6. AI fixes the issues and repeats from step 2
```

This means the AI can:
- ✅ Catch errors before pushing (saves time!)
- ✅ See exactly what failed in CI
- ✅ Fix issues automatically
- ✅ Verify fixes work before pushing again

## GitHub Actions Workflows

### Test Workflow (`.github/workflows/test.yml`)

Runs on every push to `main`, `develop`, or PRs:

```yaml
- Install dependencies
- Run TypeScript type check
- Build plugin
- Verify build output
```

This catches:
- TypeScript type errors
- Build failures
- Missing dependencies
- Import errors

### Release Workflow (`.github/workflows/release.yml`)

Runs when you push a git tag:

```yaml
- Install dependencies
- Build plugin (production)
- Create GitHub release (draft)
- Attach: main.js, manifest.json, styles.css
```

## Common Scenarios

### Scenario 1: TypeScript Error in CI

**Problem:** PR checks fail with TypeScript error

**Solution:**
```bash
# 1. Check what failed
./scripts/check-pr-status.sh
# Shows: ❌ Test Plugin Build: FAILED

# 2. See detailed error
gh run view --log-failed
# Shows: src/index.ts(70,9): error TS2531: Object is possibly 'null'

# 3. Fix the error locally
# ... edit the file ...

# 4. Verify fix works
./scripts/pre-push-check.sh

# 5. Commit and push
git add src/index.ts
git commit -m "fix: handle null return from getRightLeaf"
git push

# 6. Verify CI passes
sleep 30  # Wait for CI to start
./scripts/check-pr-status.sh
```

### Scenario 2: Creating a New PR

```bash
# 1. Create and checkout feature branch
git checkout -b feat-awesome-feature

# 2. Make your changes
# ... edit files ...

# 3. Run local checks first
./scripts/pre-push-check.sh

# 4. If checks pass, commit and push
git add .
git commit -m "feat: add awesome feature"
git push -u origin feat-awesome-feature

# 5. Create PR
gh pr create \
  --title "feat: Add awesome feature" \
  --body "This PR adds an awesome feature that does X, Y, Z"

# 6. Check PR status
./scripts/check-pr-status.sh
```

### Scenario 3: Monitoring PR Status

```bash
# Check current status
./scripts/check-pr-status.sh

# Watch for changes (run periodically)
watch -n 30 ./scripts/check-pr-status.sh

# Or use gh directly
gh pr checks --watch
```

## GitHub CLI Commands Reference

### PR Management

```bash
# View current PR
gh pr view

# View PR in browser
gh pr view --web

# Create PR
gh pr create --title "Title" --body "Body"

# Create PR interactively
gh pr create

# List PRs
gh pr list

# Check PR status
gh pr checks

# Watch PR checks in real-time
gh pr checks --watch
```

### Workflow Runs

```bash
# List recent runs
gh run list

# List runs for specific workflow
gh run list --workflow=test.yml

# View specific run
gh run view <run-id>

# View logs of failed steps
gh run view --log-failed

# Watch a run in progress
gh run watch <run-id>

# Re-run a failed workflow
gh run rerun <run-id>
```

### Repository Info

```bash
# View repo in browser
gh repo view --web

# View actions tab
gh run list --web
```

## Integration with AI Assistant

The AI assistant (in agent mode) can now:

### Before Pushing

1. **Run pre-push checks automatically**
   ```bash
   ./scripts/pre-push-check.sh
   ```
   This catches 90% of CI failures before they happen!

2. **Fix issues if found**
   - Read error messages
   - Fix the code
   - Re-run checks
   - Only push when all checks pass ✅

### After Pushing

1. **Check PR status**
   ```bash
   ./scripts/check-pr-status.sh
   ```
   See immediately if CI checks pass or fail

2. **If checks fail, get details**
   ```bash
   gh run view --log-failed
   ```
   See exactly what went wrong

3. **Fix and re-push**
   - Fix the issue
   - Run pre-push checks
   - Push the fix
   - Verify CI passes

### Continuous Monitoring

The AI can periodically check PR status and proactively fix issues:
```bash
# Check status every 30 seconds
while true; do
  ./scripts/check-pr-status.sh
  sleep 30
done
```

## Troubleshooting

### `gh` command not found

```bash
# Install GitHub CLI
brew install gh  # macOS
# or
sudo apt install gh  # Linux

# Verify installation
gh --version
```

### Not authenticated

```bash
# Login to GitHub
gh auth login

# Check auth status
gh auth status
```

### Script permission denied

```bash
# Make scripts executable
chmod +x scripts/*.sh
```

### npm/npx not found in scripts

The scripts assume npm is in your PATH. If not:

```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
export PATH="/usr/local/bin:$PATH"

# Or use full path in scripts
/usr/local/bin/npm install
```

### CI passes locally but fails remotely

Common causes:
- **Different Node version:** CI uses Node 18.x, check yours with `node --version`
- **Missing dependencies:** Ensure all packages are in `package.json`
- **Environment variables:** Don't rely on local `.env` for builds
- **Git-ignored files:** CI can't access gitignored files

## Best Practices

### For Developers

1. **Always run pre-push checks before pushing**
   ```bash
   ./scripts/pre-push-check.sh && git push
   ```

2. **Check PR status after pushing**
   ```bash
   git push && sleep 30 && ./scripts/check-pr-status.sh
   ```

3. **Fix issues quickly**
   - Don't ignore failing checks
   - CI failures block merges
   - Fix → push → verify → repeat

### For AI Assistants

1. **Run pre-push checks automatically**
   - Catch errors before pushing
   - Saves time and CI resources

2. **Check PR status after every push**
   - Know immediately if something failed
   - Can fix issues proactively

3. **Use descriptive commit messages**
   - Helps in reviewing failed CI runs
   - Makes it clear what each commit does

## Resources

- **[GitHub CLI Documentation](https://cli.github.com/manual/)** - Full gh CLI reference
- **[GitHub Actions Documentation](https://docs.github.com/en/actions)** - CI/CD platform docs
- **[Plugin Development Guide](plugin-development.md)** - Local dev setup
- **[Plugin Release Guide](plugin-releases.md)** - Release process

## Scripts Location

```
scripts/
├── check-pr-status.sh   # Check PR CI status
└── pre-push-check.sh    # Run local validation
```

Both scripts are executable and can be run from the repository root.

---

This workflow enables fast, confident development with automatic error catching and fixing! 🚀

