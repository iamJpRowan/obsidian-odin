#!/bin/bash

# ODIN Development Setup Script (One-time)
# Sets up conda environment and installs all dependencies

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the repo root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${BLUE}🔧 ODIN Development Environment Setup${NC}\n"

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check conda
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ Error: conda not found${NC}"
    echo -e "${YELLOW}Please install conda: https://docs.conda.io/en/latest/miniconda.html${NC}"
    exit 1
fi
echo -e "${GREEN}✓ conda found${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Error: Node.js not found${NC}"
    echo -e "${YELLOW}Please install Node.js: https://nodejs.org/${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found ($(node --version))${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ Error: npm not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm found ($(npm --version))${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Error: Docker not found${NC}"
    echo -e "${YELLOW}Please install Docker: https://www.docker.com/${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

# Check for .env file
echo -e "\n${BLUE}Checking environment configuration...${NC}"
if [ ! -f "$REPO_ROOT/.env" ]; then
    if [ -f "$REPO_ROOT/.env.example" ]; then
        echo -e "${YELLOW}Creating .env from .env.example...${NC}"
        cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
        echo -e "${GREEN}✓ .env created${NC}"
        echo -e "${RED}⚠️  ACTION REQUIRED: Edit .env and add your OPENAI_API_KEY${NC}"
        echo -e "${YELLOW}   Run: nano .env${NC}"
    else
        echo -e "${RED}❌ Error: .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Create conda environment
echo -e "\n${BLUE}Setting up Python environment...${NC}"
if conda env list | grep -q "odin_backend"; then
    echo -e "${YELLOW}odin_backend environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing environment...${NC}"
        conda env remove -n odin_backend -y
        echo -e "${YELLOW}Creating new environment...${NC}"
        conda create -n odin_backend python=3.9.16 -y
    fi
else
    echo -e "${YELLOW}Creating odin_backend conda environment...${NC}"
    conda create -n odin_backend python=3.9.16 -y
fi
echo -e "${GREEN}✓ Conda environment ready${NC}"

# Install backend dependencies
echo -e "\n${BLUE}Installing backend dependencies...${NC}"
cd "$REPO_ROOT/packages/backend"
conda run -n odin_backend pip install -e .
conda run -n odin_backend python -m nltk.downloader punkt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Install plugin dependencies
echo -e "\n${BLUE}Installing plugin dependencies...${NC}"
cd "$REPO_ROOT/packages/plugin"
npm install
echo -e "${GREEN}✓ Plugin dependencies installed${NC}"

# Pull Memgraph Docker image
echo -e "\n${BLUE}Pulling Memgraph Docker image...${NC}"
docker pull memgraph/memgraph-platform:latest
echo -e "${GREEN}✓ Memgraph image ready${NC}"

# Summary
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Setup complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Edit .env and add your OPENAI_API_KEY"
echo -e "   ${BLUE}nano .env${NC}"
echo -e ""
echo -e "2. Start development environment:"
echo -e "   ${BLUE}./scripts/start-dev.sh${NC}"
echo -e ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e ""

cd "$REPO_ROOT"

