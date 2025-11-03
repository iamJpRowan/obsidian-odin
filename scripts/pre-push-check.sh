#!/bin/bash
# Pre-push validation - runs local checks before pushing

set -e

echo "🔍 Running pre-push checks..."
echo ""

# Change to plugin directory
cd "$(dirname "$0")/../packages/plugin"

echo "📦 Installing dependencies (if needed)..."
if [ ! -d "node_modules" ]; then
    npm install
fi
echo "✓ Dependencies ready"
echo ""

# TypeScript type checking
echo "🔍 Running TypeScript type check..."
if npx tsc -noEmit -skipLibCheck; then
    echo "✅ TypeScript: PASSED"
else
    echo "❌ TypeScript: FAILED"
    echo ""
    echo "💡 Fix TypeScript errors before pushing"
    exit 1
fi
echo ""

# Build test
echo "🔨 Testing production build..."
if npm run build > /dev/null 2>&1; then
    echo "✅ Build: PASSED"
else
    echo "❌ Build: FAILED"
    echo ""
    echo "💡 Run 'npm run build' to see detailed error"
    exit 1
fi
echo ""

# Check if main.js was created
if [ ! -f "main.js" ]; then
    echo "❌ Build output (main.js) not found"
    exit 1
fi
echo "✅ Build output verified"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All pre-push checks passed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Safe to push your changes"
exit 0

