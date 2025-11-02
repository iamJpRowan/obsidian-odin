# Contributing to ODIN

Thank you for your interest in contributing to ODIN! This document provides guidelines and information for developers working with this monorepo.

## Monorepo Structure

This project uses a monorepo structure with npm workspaces:

```
obsidian-odin/
├── packages/
│   ├── plugin/              # Obsidian plugin (TypeScript/React)
│   └── backend/             # BOR Backend (Python/FastAPI)
├── docker-compose.yml       # Orchestrates all services
├── package.json             # Root workspace config
└── .env.example             # Environment template
```

## Getting Started

### Prerequisites

- Node.js 14+ and npm
- Python 3.9.16
- Docker and Docker Compose (for full stack testing)
- An OpenAI API key

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/memgraph/odin.git
   cd odin
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Install dependencies:**
   ```bash
   # Install plugin dependencies
   npm install
   ```

## Development Workflow

### Working on the Plugin (Frontend)

```bash
# Navigate to plugin directory
cd packages/plugin

# Install dependencies (if not done at root)
npm install

# Start development mode (watches for changes)
npm run dev

# Build for production
npm run build
```

The plugin will compile to `packages/plugin/main.js`, which Obsidian will load.

**Key Files:**
- `src/index.ts` - Plugin entry point
- `src/ui/Main/Main.tsx` - Main UI component
- `src/ui/Graph/Graph.tsx` - Graph visualization
- `src/util/fetchData.ts` - API communication

### Working on the Backend

```bash
# Navigate to backend directory
cd packages/backend

# Create conda environment
conda create --name odin_backend python=3.9.16
conda activate odin_backend

# Install dependencies
pip install -e .

# Start development server (with auto-reload)
uvicorn core.restapi.api:app --reload --host 0.0.0.0 --port 8000
```

**Key Files:**
- `core/restapi/api.py` - FastAPI endpoints
- `core/knowledgebase/notes/VaultManager.py` - Vault processing logic
- `core/knowledgebase/prompts/` - LLM prompts (customize here!)
- `core/knowledgebase/QueryAgents.py` - LLM query handlers

### Running the Full Stack

```bash
# From repository root
docker compose up

# Rebuild after changes
docker compose up --build

# View logs
docker compose logs -f backend
docker compose logs -f plugin

# Stop all services
docker compose down
```

## Making Changes

### Adding New Plugin Features

1. Create or modify React components in `packages/plugin/src/ui/`
2. Add types to `packages/plugin/src/model/` or `packages/plugin/src/shared/types/`
3. Update `packages/plugin/src/index.ts` if adding new commands or views
4. Test in Obsidian by enabling the plugin

### Adding New Backend Endpoints

1. Edit `packages/backend/core/restapi/api.py` to add new routes
2. Implement logic in `packages/backend/core/knowledgebase/`
3. Test endpoint at http://localhost:8000/docs
4. Update plugin to call the new endpoint

### Customizing Relationship Extraction

The backend uses GPT-4 to extract concepts and relationships. To customize:

1. **Modify LLM Prompts:**
   - Edit files in `packages/backend/core/knowledgebase/prompts/`
   - `prompt_generate` - Initial graph creation
   - `prompt_update` - Incremental updates
   - `system_message_*` - System instructions

2. **Add Obsidian-specific parsers:**
   - Edit `packages/backend/core/knowledgebase/notes/VaultManager.py`
   - Parse wikilinks: `[[Link]]`
   - Parse tags: `#tag`
   - Parse YAML frontmatter
   - Extract Dataview fields

3. **Adjust graph schema:**
   - Modify `packages/backend/core/knowledgebase/MemgraphManager.py`
   - Update Cypher queries in `CypherQueryHandler.py`

## Testing

### Plugin Testing

1. **Development Testing:**
   - Link plugin to Obsidian vault: `ln -s $(pwd)/packages/plugin ~/.obsidian/plugins/odin`
   - Enable in Obsidian settings
   - Check browser console (Ctrl+Shift+I) for errors

2. **Build Testing:**
   ```bash
   cd packages/plugin
   npm run build
   # Verify main.js is created and has no errors
   ```

### Backend Testing

1. **API Testing:**
   - Visit http://localhost:8000/docs
   - Test endpoints interactively
   - Check response formats

2. **Database Testing:**
   ```bash
   # Connect to Memgraph
   docker exec -it memgraph mgconsole
   
   # Run Cypher queries
   MATCH (n) RETURN n LIMIT 10;
   MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 20;
   ```

3. **Integration Testing:**
   - Initialize a test vault
   - Create/modify/delete files
   - Verify graph updates correctly

## Code Style

### TypeScript (Plugin)

- Use TypeScript strict mode
- Follow existing component patterns
- Use styled-components for styling
- Keep components focused and small

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where possible
- Document functions with docstrings
- Keep modules focused on single responsibility

## Commit Guidelines

- Use clear, descriptive commit messages
- Prefix commits with scope: `plugin:`, `backend:`, `docs:`, `docker:`
- Examples:
  - `plugin: Add node filtering by tag`
  - `backend: Improve wikilink parsing`
  - `docs: Update installation instructions`

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/my-feature`
3. **Make your changes** following the guidelines above
4. **Test thoroughly** (both plugin and backend if applicable)
5. **Commit with descriptive messages**
6. **Push to your fork:** `git push origin feature/my-feature`
7. **Open a Pull Request** with:
   - Clear description of changes
   - Why the change is needed
   - How to test the changes
   - Screenshots (if UI changes)

## Understanding the Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        Data Flow                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  User Action (Obsidian)                                      │
│         │                                                     │
│         ▼                                                     │
│  Plugin UI (React)                                           │
│         │                                                     │
│         ▼                                                     │
│  fetchData() → HTTP POST/GET                                 │
│         │                                                     │
│         ▼                                                     │
│  Backend API (FastAPI)                                       │
│         │                                                     │
│         ├─→ VaultManager → Parse markdown                    │
│         │                                                     │
│         ├─→ QueryAgents → Call GPT-4                         │
│         │        │                                            │
│         │        ▼                                            │
│         │   Extract concepts & relationships                 │
│         │                                                     │
│         ├─→ MemgraphManager → Store in graph                 │
│         │        │                                            │
│         │        ▼                                            │
│         │   Cypher queries to Memgraph                       │
│         │                                                     │
│         ▼                                                     │
│  Response (JSON) → Back to Plugin                            │
│         │                                                     │
│         ▼                                                     │
│  Update UI (Graph visualization, highlights, etc.)           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Common Customization Scenarios

### 1. Change Graph Layout

**File:** `packages/plugin/src/shared/constants.ts`
```typescript
export const LAYOUT = "circle"; // Try: "grid", "concentric", "breadthfirst"
```

### 2. Add Custom Graph Node Properties

**Backend:** `packages/backend/core/knowledgebase/MemgraphManager.py`
- Modify node creation to add properties

**Plugin:** `packages/plugin/src/model/GraphNode.ts`
- Update TypeScript interface

### 3. Recognize Custom Markdown Patterns

**Backend:** `packages/backend/core/knowledgebase/notes/VaultManager.py`
```python
def parse_custom_syntax(content: str):
    # Add your custom parser here
    # Example: Parse ::field:: inline fields
    pass
```

### 4. Change Backend URL

**Plugin:** `packages/plugin/src/ui/Main/MainUtils.ts` and `Main.tsx`
- Replace hardcoded `http://localhost:8000` URLs
- Consider making this configurable in plugin settings

## Resources

- [Obsidian Plugin API](https://github.com/obsidianmd/obsidian-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Memgraph Cypher](https://memgraph.com/docs/cypher-manual)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [React Documentation](https://react.dev/)

## Getting Help

- **Issues:** Open an issue on GitHub
- **Discussions:** Use GitHub Discussions for questions
- **API Docs:** http://localhost:8000/docs (when backend is running)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to ODIN! 🚀

