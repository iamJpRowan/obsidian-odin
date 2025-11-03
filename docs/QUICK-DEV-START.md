# Quick Development Start Guide

> **TL;DR:** This is the recommended workflow for active development. Docker is only used for Memgraph (the database), while backend and plugin run locally for fast iteration.

## Why This Approach?

- **Fast iteration**: Auto-reload for both Python and TypeScript (< 1 second)
- **Easy debugging**: Direct access to logs and debuggers
- **Simple**: Docker only where it adds value (Memgraph database)

## One-Time Setup

```bash
# 1. Run the setup script (only needed once)
./scripts/setup-dev.sh

# 2. Add your OpenAI API key to .env
nano .env
# Set: OPENAI_API_KEY=sk-...
```

That's it! The setup script will:
- ✅ Check all prerequisites (conda, Node.js, Docker)
- ✅ Create conda environment `odin_backend`
- ✅ Install Python dependencies
- ✅ Install npm dependencies
- ✅ Pull Memgraph Docker image

## Daily Development

```bash
# Start everything
./scripts/start-dev.sh

# Code away! Everything auto-reloads:
# - Edit Python files → backend restarts automatically
# - Edit TypeScript files → plugin rebuilds automatically

# Stop everything when done
./scripts/stop-dev.sh
```

## What's Running?

After `./scripts/start-dev.sh`:

| Service | Where | URL | Auto-reload? |
|---------|-------|-----|--------------|
| Memgraph | Docker | localhost:7687 | - |
| Memgraph Lab | Docker | http://localhost:3000 | - |
| Backend | Local (conda) | http://localhost:8000 | ✅ Yes |
| Plugin Build | Local (npm) | - | ✅ Yes |

## View Logs

```bash
# Backend logs
tail -f backend.log

# Plugin build logs  
tail -f plugin.log

# Memgraph logs
docker logs -f memgraph
```

## Test Your Changes

```bash
# 1. Backend API is live at:
open http://localhost:8000/docs

# 2. Enable plugin in Obsidian:
#    Settings → Community Plugins → Enable "ODIN"

# 3. Check Memgraph database:
# Option A: Visual interface (recommended)
open http://localhost:3000

# Option B: Command line
docker exec -it memgraph mgconsole
# Then: MATCH (n) RETURN n LIMIT 10;
```

## Common Tasks

### Adding Python Dependencies

```bash
# 1. Edit packages/backend/requirements.txt
# 2. Reinstall
cd packages/backend
conda activate odin_backend
pip install -e .

# Backend will auto-reload with new packages
```

### Adding npm Dependencies

```bash
cd packages/plugin
npm install <package-name>

# Plugin watch will auto-rebuild
```

### Resetting the Database

```bash
# Stop and remove Memgraph container
docker stop memgraph
docker rm memgraph

# Start fresh (next time you run start-dev.sh, it creates new container)
```

### Full Stack Test (Before Committing)

```bash
# Stop local development
./scripts/stop-dev.sh

# Test with full Docker stack
docker compose down -v
docker compose up --build

# If everything works, commit your changes
```

## Troubleshooting

### "Cannot connect to backend"
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Check logs
tail -f backend.log

# Restart backend
./scripts/stop-dev.sh && ./scripts/start-dev.sh
```

### "Memgraph connection refused"
```bash
# Check if Memgraph is running
docker ps | grep memgraph

# Restart Memgraph
docker restart memgraph
```

### "Module not found" errors
```bash
# Reinstall dependencies
cd packages/backend
conda activate odin_backend
pip install -e .
```

### Port already in use
```bash
# Find what's using port 8000
lsof -i :8000

# Stop the process
kill -9 <PID>

# Or use different port
cd packages/backend
conda activate odin_backend
uvicorn core.restapi.api:app --reload --port 8001
```

## When to Use Full Docker

Use `docker compose up` when:
- ✅ Testing the full production-like stack
- ✅ Troubleshooting platform-specific issues
- ✅ Sharing environment with others
- ✅ Before creating a PR

Use local development (this guide) when:
- ✅ Actively coding (most of the time)
- ✅ Debugging
- ✅ Iterating quickly

## Next Steps

- **[Vault Testing Guide](vault-testing-guide.md)** - Test importing your vault data
- **[Memgraph Lab Guide](memgraph-lab-guide.md)** - Visual graph database exploration
- **[Contributing Guide](contributing.md)** - Learn about the codebase structure
- **[Testing Guide](testing.md)** - How to test your changes
- **[Plugin Development](plugin-development.md)** - Plugin-specific tips

---

**Happy coding! 🚀** Changes to `.py` and `.ts` files auto-reload instantly.

