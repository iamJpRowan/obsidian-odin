[![react](https://img.shields.io/badge/React-61DBFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![typescript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![styledcomponents](https://img.shields.io/badge/styled_components-DB7093?style=for-the-badge&logo=styledcomponents&logoColor=white)](https://styled-components.com/)
[![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

[![obsidian](https://img.shields.io/badge/obsidian-7C3AED?style=for-the-badge&logo=obsidian&logoColor=white)](https://obsidian.md/)
[![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

# ODIN - Obsidian Driven Information Network

> **Monorepo Edition**: This repository now contains both the Obsidian plugin (frontend) and the BOR backend in a unified workspace for easier development and customization.

## Table of contents
1. [Features](#features)
2. [Architecture](#architecture)
3. [Disclaimer](#disclaimer)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
	1. [Docker (Recommended)](#docker-installation)
	2. [Manual](#manual-installation)
6. [Project Structure](#project-structure)
7. [Customization](#customization)
8. [Development](#development)
9. [Documentation](#documentation)

## Features

<img src="./packages/plugin/src/assets/images/odin.png" alt="odin">

Most features are accessible through the `Graph Prompt view` button in the menu opened by clicking the `Expand` button in the right upper corner of Obsidian.

1. **Prompt Bar for LLM Queries**

<p align="center">
  <img src="./packages/plugin/src/assets/images/odin-promptbar.png" alt="odin prompt bar" width="400">
</p>

- ODIN integrates Large Language Models (LLMs) into Obsidian using LangChain, allowing you to ask questions about the data stored in your knowledge graph right from the prompt bar.
  
2. **Graph Visualization**

- `Vault view` will give you a comprehensive understanding of your notes and knowledge by visualizing your entire Obsidian vault as a dynamic knowledge graph.
- Switch between `Vault view` and `File view` to get a detailed visualization of specific files.
- By clicking nodes in the `File view` you will get highlighted sentences thematically connected to that node in your editor.

3. **Dropdown Menu Functions**

<p align="center">
  <img src="./packages/plugin/src/assets/images/odin-dropdown.png" alt="odin dropdown menu" width="400">
</p>

Right click on the highlighted text in the editor to access the following features:

- **Generate questions**: Extract thought-provoking questions from your markdown files, encouraging deeper contemplation and critical thinking.

- **Link prediction**: Automatically generate links to other markdown files in your vault that are thematically connected to the highlighted text, enriching your notes with relevant references.

- **Node suggestion**: Access thematically connected nodes related to the highlighted text, fostering meaningful connections and comprehensive understanding of your information.

## Architecture

ODIN consists of three main components:

```
┌─────────────────────────────────────────────────────────────┐
│                      ODIN Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────┐         ┌───────────────────┐        │
│  │  Obsidian Plugin  │────────▶│   BOR Backend     │        │
│  │   (TypeScript)    │ HTTP    │    (Python)       │        │
│  │   React + Cyto.js │         │  FastAPI + AI     │        │
│  └───────────────────┘         └─────────┬─────────┘        │
│                                           │                   │
│                                           ▼                   │
│                                 ┌───────────────────┐        │
│                                 │    Memgraph DB    │        │
│                                 │  (Graph Database) │        │
│                                 └───────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

- **Plugin**: Obsidian plugin UI (React + TypeScript)
- **Backend**: Python FastAPI server with LangChain + OpenAI integration
- **Database**: Memgraph for storing and querying knowledge graphs

## Disclaimer

> **Warning**
> - It is **strongly recommended** that you have access to **GPT-4** via the OpenAI API. GPT-3.5 will probably fail to make correct knowledge graphs from your data.
> - The `init_repo`, `update_file` and `add_file` endpoints may be untested with your specific vault structure.
> - **Here be dragons.** 🐉

## Prerequisites

Before you begin, make sure you have the following:

- **Obsidian** installed on your system
- An active **Obsidian vault**
- An **OpenAI API key** (with GPT-4 access recommended)

## Installation

### Docker Installation (Recommended)

Docker setup automatically installs and runs Memgraph database, the backend, and the plugin build process.

#### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/) installed

#### Steps

1. **Clone the Repository:**
   ```bash
   # Clone inside your Obsidian vault's plugins folder
   cd your_vault/.obsidian/plugins
   git clone https://github.com/memgraph/odin.git obsidian-odin
   cd obsidian-odin
   ```

2. **Configure Environment Variables:**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # Required: OPENAI_API_KEY=your_actual_api_key_here
   # Recommended: LLM_MODEL_NAME=gpt-4
   ```

3. **Start All Services:**
   ```bash
   docker compose up
   ```
   
   This will start:
   - **Memgraph** (graph database) on port 7687
   - **Backend** (BOR API) on port 8000
   - **Plugin build** process

   The first run may take up to 10 minutes to download and build everything.

4. **Enable the Plugin in Obsidian:**
   - In Obsidian settings, navigate to "Options" → "Community plugins"
   - Click "Turn on community plugins" (disable restricted mode)
   - Find "ODIN" in the list and toggle it on
   - If you don't see ODIN, reload Obsidian

### Manual Installation

For development or if you want to customize the backend logic.

#### Prerequisites
- [Node.js](https://nodejs.org/) v14+ and npm
- [Python](https://www.python.org/) 3.9.16
- [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) (recommended)
- [Memgraph](https://memgraph.com/docs/memgraph/installation)

#### Steps

1. **Clone the Repository:**
   ```bash
   cd your_vault/.obsidian/plugins
   git clone https://github.com/memgraph/odin.git obsidian-odin
   cd obsidian-odin
   ```

2. **Install Plugin Dependencies:**
   ```bash
   npm install
   npm run dev  # Starts the plugin build in watch mode
   ```

3. **Set Up Backend:**
   ```bash
   # Create conda environment
   conda create --name odin_backend python=3.9.16
   conda activate odin_backend
   
   # Install backend dependencies
   cd packages/backend
   pip install -e .
   
   # Configure environment
   cp ../../.env.example ../../.env
   # Edit .env with your OpenAI API key
   ```

4. **Start Memgraph:**
   ```bash
   # Option 1: Using Docker
   docker run -p 7687:7687 -p 7444:7444 memgraph/memgraph-mage:1.15-memgraph-2.15
   
   # Option 2: Native installation
   # Follow: https://memgraph.com/docs/memgraph/installation
   ```

5. **Start Backend Server:**
   ```bash
   cd packages/backend
   uvicorn core.restapi.api:app --reload
   ```

6. **Enable Plugin in Obsidian** (same as Docker steps above)

## Project Structure

```
obsidian-odin/
├── packages/
│   ├── plugin/              # Obsidian plugin (TypeScript/React)
│   │   ├── src/
│   │   │   ├── index.ts     # Plugin entry point
│   │   │   ├── ui/          # React components
│   │   │   ├── model/       # TypeScript models
│   │   │   └── util/        # Utility functions
│   │   ├── manifest.json    # Obsidian plugin manifest
│   │   ├── package.json
│   │   └── esbuild.config.mjs
│   │
│   └── backend/             # BOR Backend (Python/FastAPI)
│       ├── core/
│       │   ├── knowledgebase/     # Graph logic
│       │   │   ├── notes/         # Vault processing
│       │   │   ├── prompts/       # LLM prompts (customize here!)
│       │   │   └── Utils.py
│       │   └── restapi/
│       │       └── api.py         # FastAPI endpoints
│       ├── requirements.txt
│       └── Dockerfile
│
├── docker-compose.yml       # Orchestrates all services
├── .env.example             # Environment configuration template
├── package.json             # Root workspace config
└── README.md                # This file
```

## Customization

### Understanding Your Vault's Relationships

The backend (BOR) uses GPT-4 to analyze your markdown files and extract:
- **Nodes**: Key concepts, entities, topics
- **Edges**: Relationships between concepts
- **Embeddings**: Vector representations for semantic search

### How to Tune for Your Vault

The relationship extraction happens in the backend. To customize:

1. **Modify LLM Prompts:**
   ```bash
   cd packages/backend/core/knowledgebase/prompts/
   # Edit these files to change how GPT-4 interprets your notes:
   # - prompt_generate: Initial graph creation
   # - prompt_update: File update logic
   # - system_message_*: System-level instructions
   ```

2. **Add Obsidian-Specific Parsers:**
   
   Edit `packages/backend/core/knowledgebase/notes/VaultManager.py` to recognize:
   - Wikilinks: `[[Page Name]]`
   - Tags: `#topic`
   - YAML frontmatter relationships
   - Dataview inline fields
   
   Example: Parse existing links before sending to GPT-4 to ensure they're preserved.

3. **Adjust Model Settings:**
   
   In `.env`:
   ```bash
   LLM_MODEL_NAME=gpt-4               # Try gpt-4-turbo-preview
   LLM_MODEL_TEMPERATURE=0.2          # Lower = more deterministic
   EMBEDDING_MODEL_NAME=text-embedding-ada-002
   ```

4. **Query the Graph Directly:**
   ```bash
   # Connect to Memgraph to see what's stored
   docker exec -it memgraph mgconsole
   
   # Example Cypher queries:
   MATCH (n) RETURN n LIMIT 25;                    # Show nodes
   MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50;   # Show relationships
   MATCH (n {file_path: "/path/to/note.md"}) RETURN n;
   ```

### Backend API Documentation

When the backend is running, visit: **http://localhost:8000/docs**

This shows all available endpoints for customization.

## Development

### Quick Start (Recommended)

For the **fastest development experience** with auto-reload:

```bash
# One-time setup
./scripts/setup-dev.sh

# Daily workflow - starts Memgraph (Docker) + Backend & Plugin (local)
./scripts/start-dev.sh

# Stop everything
./scripts/stop-dev.sh
```

**See [Quick Dev Start Guide](docs/QUICK-DEV-START.md) for detailed instructions.**

This hybrid approach gives you:
- ✅ **Instant feedback**: Backend and plugin auto-reload in < 1 second
- ✅ **Easy debugging**: Direct access to logs and Python debugger
- ✅ **Simple setup**: Docker only for Memgraph database

### Working on the Plugin

```bash
# Development mode (auto-rebuild on changes)
npm run dev

# Production build
npm run build
```

### Working on the Backend

```bash
cd packages/backend

# Activate environment
conda activate odin_backend

# Run with auto-reload
uvicorn core.restapi.api:app --reload

# Run tests (if available)
pytest
```

### Docker Development (Full Stack Testing)

Use Docker when you need to test the full production-like stack:

```bash
# Build and start all services
docker compose up --build

# Rebuild specific service
docker compose build backend

# View logs
docker compose logs -f backend

# Stop all services
docker compose down

# Clean everything (including volumes)
docker compose down -v
```

## Documentation

### 📚 Available Documentation

- **[Quick Dev Start](docs/QUICK-DEV-START.md)** - ⭐ Start here for development (recommended workflow)
- **[Quickstart Guide](docs/quickstart.md)** - Get up and running in 5 minutes
- **[Contributing Guide](docs/contributing.md)** - Developer guide for customization
- **[Testing Guide](docs/testing.md)** - How to test your changes
- **[Docker Build Guide](docs/docker-build.md)** - Building and managing Docker images
- **[Development Log](devlog/)** - Detailed history of design decisions and implementation
- **[Changelog](CHANGELOG.md)** - Version history and release notes

### 🔧 Troubleshooting

#### Plugin doesn't appear in Obsidian
- Ensure you cloned into `your_vault/.obsidian/plugins/`
- Check that `manifest.json` and `main.js` exist
- Reload Obsidian (Ctrl/Cmd + R)

#### Backend connection errors
- Verify backend is running: `curl http://localhost:8000/docs`
- Check Docker logs: `docker compose logs backend`
- Ensure `.env` has valid `OPENAI_API_KEY`

#### Graph not updating
- Check Memgraph is running: `docker ps | grep memgraph`
- Initialize repo: Backend should auto-call `/knowledge_base/general/init_local_repo`
- Check backend logs for errors

#### GPT-4 API errors
- Verify API key has GPT-4 access
- Check OpenAI usage limits
- Try `gpt-3.5-turbo` for testing (expect lower quality)

## Contributing

Contributions are welcome! This monorepo structure makes it easier to:
- See the full data flow from UI → API → Database
- Test changes across the stack
- Customize for your specific vault structure

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Memgraph** for the graph database
- **Obsidian** for the extensible note-taking platform
- **OpenAI** for GPT-4 and embeddings
- Original **ODIN** and **BOR** teams

---

**Need Help?** Open an issue or check the backend API docs at http://localhost:8000/docs when running.
