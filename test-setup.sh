#!/bin/bash
# ODIN Setup and Testing Script
# Run this in your terminal: bash test-setup.sh

set -e  # Exit on error

echo "🔍 ODIN Monorepo Setup & Test Script"
echo "======================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track what we need to do
NEEDS_ENV_KEY=false
NEEDS_DOCKER=false
NEEDS_NODE=false

echo "Step 1: Checking prerequisites..."
echo "-----------------------------------"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js is installed: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js is NOT installed"
    NEEDS_NODE=true
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm is installed: $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm is NOT installed"
    NEEDS_NODE=true
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}✓${NC} Docker is installed: $DOCKER_VERSION"
else
    echo -e "${RED}✗${NC} Docker is NOT installed"
    NEEDS_DOCKER=true
fi

# Check Docker Compose
if command -v docker compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker Compose is available"
elif command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker Compose (standalone) is available"
else
    echo -e "${RED}✗${NC} Docker Compose is NOT available"
    NEEDS_DOCKER=true
fi

echo ""

# Check .env file
echo "Step 2: Checking environment configuration..."
echo "----------------------------------------------"

if [ -f .env ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    
    # Check if API key is set
    if grep -q "your_openai_api_key_here" .env 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC}  .env still has placeholder API key"
        NEEDS_ENV_KEY=true
    elif grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        echo -e "${GREEN}✓${NC} OpenAI API key appears to be configured"
    else
        echo -e "${YELLOW}⚠${NC}  Cannot verify if API key is set"
        NEEDS_ENV_KEY=true
    fi
else
    echo -e "${RED}✗${NC} .env file does not exist"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env file"
    NEEDS_ENV_KEY=true
fi

echo ""

# Report what needs to be done
if [ "$NEEDS_NODE" = true ] || [ "$NEEDS_DOCKER" = true ] || [ "$NEEDS_ENV_KEY" = true ]; then
    echo "⚠️  Action Required:"
    echo "-------------------"
    
    if [ "$NEEDS_ENV_KEY" = true ]; then
        echo -e "${YELLOW}1.${NC} Edit .env and add your OpenAI API key:"
        echo "   nano .env"
        echo "   (Replace 'your_openai_api_key_here' with your actual key)"
        echo ""
    fi
    
    if [ "$NEEDS_NODE" = true ]; then
        echo -e "${YELLOW}2.${NC} Install Node.js (for manual development):"
        echo "   Download from: https://nodejs.org/"
        echo "   Or use Homebrew: brew install node"
        echo ""
    fi
    
    if [ "$NEEDS_DOCKER" = true ]; then
        echo -e "${YELLOW}3.${NC} Install Docker (REQUIRED for full stack):"
        echo "   Download from: https://www.docker.com/products/docker-desktop"
        echo ""
    fi
    
    echo "After completing the above, re-run this script."
    exit 0
fi

echo "✅ All prerequisites are met!"
echo ""

# Test plugin build (if Node is available)
if [ "$NEEDS_NODE" = false ]; then
    echo "Step 3: Testing plugin build..."
    echo "--------------------------------"
    
    cd packages/plugin
    
    if [ ! -d "node_modules" ]; then
        echo "Installing plugin dependencies..."
        npm install
    else
        echo -e "${GREEN}✓${NC} Dependencies already installed"
    fi
    
    echo "Building plugin..."
    npm run build
    
    if [ -f "main.js" ]; then
        SIZE=$(wc -c < main.js | tr -d ' ')
        echo -e "${GREEN}✓${NC} Plugin built successfully! (main.js: $SIZE bytes)"
    else
        echo -e "${RED}✗${NC} Plugin build failed - main.js not created"
        exit 1
    fi
    
    cd ../..
    echo ""
fi

# Test Docker setup
echo "Step 4: Testing Docker setup..."
echo "--------------------------------"

echo "Checking if containers are already running..."
if docker ps | grep -q "odin-backend\|odin-plugin\|memgraph"; then
    echo -e "${YELLOW}⚠${NC}  ODIN containers are already running"
    echo ""
    echo "Options:"
    echo "  1. Stop and rebuild: docker compose down && docker compose up --build"
    echo "  2. View logs: docker compose logs -f"
    echo "  3. Continue with current containers"
else
    echo "No ODIN containers running."
    echo ""
    echo "To start the full stack, run:"
    echo -e "${GREEN}docker compose up${NC}"
    echo ""
    echo "This will:"
    echo "  • Start Memgraph (graph database) on port 7687"
    echo "  • Start Backend API on port 8000"
    echo "  • Build and run the plugin"
    echo ""
    echo "Press Ctrl+C to stop when done testing."
fi

echo ""
echo "Step 5: Verification checklist..."
echo "----------------------------------"
echo "After starting Docker, verify:"
echo ""
echo "1. Backend API is accessible:"
echo "   curl http://localhost:8000/docs"
echo "   (Should return HTML of the API docs)"
echo ""
echo "2. Memgraph is running:"
echo "   docker ps | grep memgraph"
echo ""
echo "3. View logs:"
echo "   docker compose logs backend"
echo "   docker compose logs memgraph"
echo ""
echo "4. Plugin files exist:"
echo "   ls -lh packages/plugin/main.js"
echo "   ls -lh packages/plugin/manifest.json"
echo ""
echo "5. For Obsidian testing:"
echo "   - Copy/link this folder to your vault's .obsidian/plugins/"
echo "   - Enable ODIN in Obsidian settings"
echo "   - Look for 'Graph Prompt View' in the right sidebar"
echo ""

echo "======================================"
echo "Setup check complete! 🚀"
echo "======================================"

