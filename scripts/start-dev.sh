#!/bin/bash

# ODIN Development Startup Script
# Starts Memgraph in Docker, backend locally, and plugin watch mode

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the repo root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}🚀 Starting ODIN Development Environment${NC}\n"

# Check if .env exists
if [ ! -f "$REPO_ROOT/.env" ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and add your OPENAI_API_KEY${NC}"
    exit 1
fi

# Check if conda environment exists
if ! conda env list | grep -q "odin_backend"; then
    echo -e "${RED}❌ Error: odin_backend conda environment not found${NC}"
    echo -e "${YELLOW}Run: ./scripts/setup-dev.sh to set up your environment${NC}"
    exit 1
fi

# Step 1: Start Memgraph in Docker
echo -e "${BLUE}📊 Starting Memgraph database...${NC}"
if docker ps | grep -q memgraph; then
    echo -e "${GREEN}✓ Memgraph already running${NC}"
elif docker ps -a | grep -q memgraph; then
    echo -e "${YELLOW}Starting existing Memgraph container...${NC}"
    docker start memgraph
    echo -e "${GREEN}✓ Memgraph started${NC}"
else
    echo -e "${YELLOW}Creating new Memgraph container...${NC}"
    docker run -d \
        --name memgraph \
        -p 7687:7687 \
        -p 3000:3000 \
        -p 7444:7444 \
        -e MEMGRAPH="--log-level=TRACE" \
        memgraph/memgraph-platform:latest
    echo -e "${GREEN}✓ Memgraph created and started${NC}"
fi

# Give Memgraph a moment to fully start
sleep 2

# Step 2: Start backend in background
echo -e "\n${BLUE}🐍 Starting backend server...${NC}"
cd "$REPO_ROOT/packages/backend"

# Source .env file for environment variables
set -a
source "$REPO_ROOT/.env"
set +a

# Start backend in background with conda
echo -e "${YELLOW}Backend will run with auto-reload on http://localhost:8000${NC}"
conda run -n odin_backend uvicorn core.restapi.api:app --reload --host 0.0.0.0 --port 8000 > "$REPO_ROOT/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$REPO_ROOT/.backend.pid"
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo -e "${GREEN}  Logs: tail -f backend.log${NC}"

# Step 3: Start plugin build watch
echo -e "\n${BLUE}⚛️  Starting plugin build watch...${NC}"
cd "$REPO_ROOT/packages/plugin"
echo -e "${YELLOW}Plugin will auto-rebuild on changes${NC}"
npm run dev > "$REPO_ROOT/plugin.log" 2>&1 &
PLUGIN_PID=$!
echo $PLUGIN_PID > "$REPO_ROOT/.plugin.pid"
echo -e "${GREEN}✓ Plugin watch started (PID: $PLUGIN_PID)${NC}"
echo -e "${GREEN}  Logs: tail -f plugin.log${NC}"

# Summary
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Development environment is ready!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e ""
echo -e "🌐 Backend API:    ${BLUE}http://localhost:8000${NC}"
echo -e "📚 API Docs:       ${BLUE}http://localhost:8000/docs${NC}"
echo -e "📊 Memgraph:       ${BLUE}localhost:7687${NC}"
echo -e "🎨 Memgraph Lab:   ${BLUE}http://localhost:3000${NC}"
echo -e ""
echo -e "📝 View Logs:"
echo -e "   Backend:  ${YELLOW}tail -f backend.log${NC}"
echo -e "   Plugin:   ${YELLOW}tail -f plugin.log${NC}"
echo -e ""
echo -e "🛑 Stop Services:  ${YELLOW}./scripts/stop-dev.sh${NC}"
echo -e ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e ""
echo -e "${YELLOW}Tip: Changes to Python and TypeScript files will auto-reload!${NC}"
echo -e ""

cd "$REPO_ROOT"

