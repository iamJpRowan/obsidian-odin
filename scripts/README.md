# Helper Scripts

These scripts enable checking PR status and running local validation from within the IDE.

## Available Scripts

### `check-pr-status.sh`

Check the CI status of the PR for the current branch.

**Usage:**
```bash
./scripts/check-pr-status.sh
```

**Features:**
- Shows PR number, title, and URL
- Displays all CI check statuses with color coding:
  - ✅ Green for passed
  - ❌ Red for failed
  - ⏳ Yellow for in progress
- Provides direct links to failed check details
- Suggests next steps if checks fail

**Example output:**
```
🔍 Checking PR status...

📍 Current branch: feat-awesome-feature
✓ Found PR #123

📝 Title: Add awesome feature
🔗 URL: https://github.com/user/repo/pull/123

🔄 CI Checks:
─────────────────────────────────────────
✅ build: PASSED
─────────────────────────────────────────

✅ All checks passed!
```

### `pre-push-check.sh`

Run local validation checks before pushing to catch errors early.

**Usage:**
```bash
./scripts/pre-push-check.sh
```

**What it checks:**
1. Dependencies are installed
2. TypeScript type checking passes
3. Production build succeeds
4. Build output (main.js) exists

**Use before pushing** to prevent CI failures!

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

## Integration with Development Workflow

### Recommended Workflow

```bash
# 1. Make changes
# ... edit files ...

# 2. Run local checks
./scripts/pre-push-check.sh

# 3. If checks pass, commit and push
git add .
git commit -m "feat: your changes"
git push

# 4. Check PR status
sleep 30  # Wait for CI to start
./scripts/check-pr-status.sh

# 5. If CI failed, see what went wrong
gh run view --log-failed

# 6. Fix issues and repeat from step 2
```

### AI Assistant Integration

When in agent mode, the AI assistant can:

1. **Run pre-push checks automatically** before every push
2. **Check PR status** after pushing
3. **Read CI failure logs** if checks fail
4. **Fix issues** and push again
5. **Verify fixes** by checking PR status again

This creates a tight feedback loop where the AI can:
- Catch 90% of errors before CI runs
- See exactly what failed if CI does fail
- Fix issues immediately without human intervention
- Verify fixes work before considering the task done

## Requirements

- **GitHub CLI (`gh`)** - For PR status checking
  ```bash
  brew install gh  # macOS
  gh auth login    # Authenticate
  ```

- **Node.js and npm** - For building and type checking
  ```bash
  cd packages/plugin
  npm install
  ```

- **jq** - For parsing JSON (usually pre-installed on macOS)
  ```bash
  brew install jq  # If needed
  ```

## Troubleshooting

### "gh command not found"
```bash
brew install gh
gh auth login
```

### "Permission denied"
```bash
chmod +x scripts/*.sh
```

### "npm command not found"
Make sure npm is in your PATH or use the full path in the scripts.

### "No PR found for this branch"
You haven't created a PR yet. Create one with:
```bash
gh pr create --title "Your title" --body "Description"
```

## More Information

See the [CI/CD Workflow Guide](../docs/ci-workflow.md) for comprehensive documentation on:
- GitHub CLI usage
- CI/CD workflows
- Common scenarios
- Best practices
- AI assistant integration patterns

## Quick Reference

```bash
# Check PR status
./scripts/check-pr-status.sh

# Run local checks
./scripts/pre-push-check.sh

# View failed CI logs
gh run view --log-failed

# List recent workflow runs
gh run list --limit 5

# Create a PR
gh pr create

# View PR in browser
gh pr view --web
```

---

These scripts enable fast, confident development with immediate feedback! 🚀

