#!/bin/bash

# ODIN Development Stop Script
# Stops all running development services

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the repo root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}🛑 Stopping ODIN Development Environment${NC}\n"

# Stop backend
if [ -f "$REPO_ROOT/.backend.pid" ]; then
    BACKEND_PID=$(cat "$REPO_ROOT/.backend.pid")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping backend (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID
        echo -e "${GREEN}✓ Backend stopped${NC}"
    else
        echo -e "${YELLOW}Backend not running${NC}"
    fi
    rm "$REPO_ROOT/.backend.pid"
else
    echo -e "${YELLOW}No backend PID file found${NC}"
fi

# Stop plugin watch
if [ -f "$REPO_ROOT/.plugin.pid" ]; then
    PLUGIN_PID=$(cat "$REPO_ROOT/.plugin.pid")
    if ps -p $PLUGIN_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping plugin watch (PID: $PLUGIN_PID)...${NC}"
        kill $PLUGIN_PID
        echo -e "${GREEN}✓ Plugin watch stopped${NC}"
    else
        echo -e "${YELLOW}Plugin watch not running${NC}"
    fi
    rm "$REPO_ROOT/.plugin.pid"
else
    echo -e "${YELLOW}No plugin PID file found${NC}"
fi

# Stop Memgraph (but don't remove the container - preserves data)
if docker ps | grep -q memgraph; then
    echo -e "${YELLOW}Stopping Memgraph container...${NC}"
    docker stop memgraph
    echo -e "${GREEN}✓ Memgraph stopped${NC}"
else
    echo -e "${YELLOW}Memgraph not running${NC}"
fi

echo -e "\n${GREEN}✨ All services stopped${NC}"
echo -e "\n${YELLOW}Note: Memgraph container still exists (data preserved)${NC}"
echo -e "${YELLOW}To remove it completely: docker rm memgraph${NC}\n"

