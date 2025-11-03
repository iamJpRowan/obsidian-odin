# Getting Started with Development

Welcome! This guide will get you developing on ODIN in under 5 minutes.

## Quick Start

### First Time Setup (One Time Only)

```bash
# 1. Run the automated setup
./scripts/setup-dev.sh

# 2. Add your OpenAI API key
cp .env.example .env    # If .env doesn't exist
nano .env               # Add your key: OPENAI_API_KEY=sk-...
```

That's it! The script handles:
- ✅ Creating conda environment
- ✅ Installing all Python dependencies
- ✅ Installing all npm dependencies
- ✅ Pulling Docker images

### Daily Development

```bash
# Start everything
./scripts/start-dev.sh

# Make your changes - they auto-reload!
# - Edit Python files → backend restarts instantly
# - Edit TypeScript files → plugin rebuilds instantly

# Stop when done
./scripts/stop-dev.sh
```

## What's Running?

After `start-dev.sh`, you'll have:

| Service | Location | URL | Auto-Reload |
|---------|----------|-----|-------------|
| **Memgraph** | Docker | localhost:7687 | - |
| **Backend API** | Local (conda) | http://localhost:8000 | ✅ Yes |
| **Plugin Build** | Local (npm) | - | ✅ Yes |

## Making Changes

### Editing Backend Code

```bash
# Backend auto-reloads on file save!
cd packages/backend/core/
# Edit any .py file
# Save → See reload in backend.log (< 1 second)
```

**Common backend files:**
- `restapi/api.py` - API endpoints
- `knowledgebase/notes/VaultManager.py` - Vault processing
- `knowledgebase/prompts/` - LLM prompts (text files)
- `knowledgebase/QueryAgents.py` - LLM query logic

### Editing Plugin Code

```bash
# Plugin auto-rebuilds on file save!
cd packages/plugin/src/
# Edit any .ts or .tsx file
# Save → See rebuild in plugin.log (< 2 seconds)
```

**Common plugin files:**
- `ui/Main/Main.tsx` - Main UI component
- `ui/Graph/Graph.tsx` - Graph visualization
- `util/fetchData.ts` - API calls to backend

### Testing Your Changes

```bash
# 1. Backend API docs (interactive testing)
open http://localhost:8000/docs

# 2. Check backend logs
tail -f backend.log

# 3. Check plugin build logs
tail -f plugin.log

# 4. Query Memgraph database
docker exec -it memgraph mgconsole
# Then: MATCH (n) RETURN n LIMIT 10;
```

## Common Development Tasks

### Adding a Python Package

```bash
# 1. Add to requirements.txt
echo "requests==2.31.0" >> packages/backend/requirements.txt

# 2. Reinstall
cd packages/backend
conda activate odin_backend
pip install -e .

# Backend will auto-reload with new package available
```

### Adding an npm Package

```bash
cd packages/plugin
npm install lodash

# Plugin watch will auto-rebuild
```

### Resetting the Database

```bash
# Stop and remove Memgraph
docker stop memgraph
docker rm memgraph

# Next time you run start-dev.sh, fresh database will be created
```

### Before Committing

Always test with full Docker stack to ensure production parity:

```bash
# Stop local development
./scripts/stop-dev.sh

# Test full stack
docker compose down -v
docker compose up --build

# If it works, you're good to commit!
```

## Troubleshooting

### "Cannot connect to backend"

```bash
# Check backend is running
curl http://localhost:8000/docs

# If not, check logs
tail -f backend.log

# Restart everything
./scripts/stop-dev.sh
./scripts/start-dev.sh
```

### "Conda environment not found"

```bash
# Run setup again
./scripts/setup-dev.sh
```

### "Port 8000 already in use"

```bash
# Find what's using it
lsof -i :8000

# Kill it
kill -9 <PID>
```

### "Module not found" in Python

```bash
cd packages/backend
conda activate odin_backend
pip install -e .
```

## Development Workflow Cheat Sheet

```bash
# ═══ Daily Workflow ═══
./scripts/start-dev.sh         # Start everything
# ... code, code, code ...
tail -f backend.log            # Watch backend
tail -f plugin.log             # Watch plugin
./scripts/stop-dev.sh          # Stop everything

# ═══ Testing ═══
open http://localhost:8000/docs           # API docs
docker exec -it memgraph mgconsole        # Database

# ═══ Before Commit ═══
docker compose up --build      # Full stack test

# ═══ Reset Database ═══
docker stop memgraph && docker rm memgraph

# ═══ Clean Everything ═══
./scripts/stop-dev.sh
docker compose down -v
```

## Why This Approach?

**Speed**: Changes reload in < 1 second vs 5-10 seconds with full Docker

**Simplicity**: One command to start, one to stop

**Debugging**: Direct access to logs and Python debugger

**Confidence**: Still test with full Docker before committing

## More Information

- **[Quick Dev Start](docs/QUICK-DEV-START.md)** - Detailed guide
- **[Workflow Comparison](docs/dev-workflow-comparison.md)** - Different approaches explained
- **[Contributing](docs/contributing.md)** - Code structure and patterns
- **[Main README](README.md)** - Full project documentation

---

**Happy coding! 🚀** Remember: save file → auto-reload (< 1 sec) → test!

