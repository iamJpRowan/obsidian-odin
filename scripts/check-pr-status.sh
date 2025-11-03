#!/bin/bash
# Check PR status and display results

set -e

echo "🔍 Checking PR status..."
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

# Get current branch
BRANCH=$(git branch --show-current)
echo "📍 Current branch: $BRANCH"
echo ""

# Check if there's a PR for this branch
PR_NUMBER=$(gh pr view --json number -q .number 2>/dev/null || echo "")

if [ -z "$PR_NUMBER" ]; then
    echo "ℹ️  No PR found for this branch"
    echo ""
    echo "💡 To create a PR, run:"
    echo "   gh pr create --title 'Your PR title' --body 'PR description'"
    exit 0
fi

echo "✓ Found PR #$PR_NUMBER"
echo ""

# Get PR details
PR_TITLE=$(gh pr view --json title -q .title)
PR_URL=$(gh pr view --json url -q .url)

echo "📝 Title: $PR_TITLE"
echo "🔗 URL: $PR_URL"
echo ""

# Check CI status
echo "🔄 CI Checks:"
echo "─────────────────────────────────────────"

gh pr checks --json name,state,link | jq -r '.[] | 
  if .state == "SUCCESS" or .state == "success" then
    "✅ \(.name): PASSED"
  elif .state == "FAILURE" or .state == "failure" then
    "❌ \(.name): FAILED\n   Details: \(.link)"
  elif .state == "PENDING" or .state == "pending" or .state == "IN_PROGRESS" then
    "⏳ \(.name): IN PROGRESS"
  else
    "⚠️  \(.name): \(.state)"
  end'

echo "─────────────────────────────────────────"
echo ""

# Check if any checks failed
FAILED=$(gh pr checks --json state -q '[.[] | select(.state == "FAILURE" or .state == "failure")] | length')

if [ "$FAILED" -gt 0 ]; then
    echo "❌ $FAILED check(s) failed"
    echo ""
    echo "💡 To see detailed logs of failed checks:"
    echo "   gh run view --log-failed"
    echo ""
    echo "💡 To see specific workflow run:"
    echo "   gh run list --limit 5"
    exit 1
else
    PENDING=$(gh pr checks --json state -q '[.[] | select(.state == "PENDING" or .state == "pending" or .state == "IN_PROGRESS")] | length')
    if [ "$PENDING" -gt 0 ]; then
        echo "⏳ Waiting for $PENDING check(s) to complete..."
        exit 0
    else
        echo "✅ All checks passed!"
        exit 0
    fi
fi

