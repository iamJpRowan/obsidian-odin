# Development Workflow Comparison

This document explains the different ways to run ODIN during development and when to use each approach.

## Three Approaches

### 1. Hybrid Development (⭐ Recommended)

**When:** Daily active development

**What:**
- Memgraph in Docker
- Backend runs locally with `uvicorn --reload`
- Plugin builds locally with `npm run dev`

**Start:**
```bash
./scripts/start-dev.sh
```

**Pros:**
- ✅ Fastest iteration (< 1 second for changes)
- ✅ Direct access to logs
- ✅ Easy debugging with Python debugger
- ✅ Auto-reload for both Python and TypeScript

**Cons:**
- ⚠️ Requires one-time setup of conda environment
- ⚠️ Slightly different from production environment

---

### 2. Full Docker Stack

**When:** Testing production-like deployment, troubleshooting platform issues, before committing

**What:**
- Everything runs in Docker containers
- Memgraph, backend, and plugin build

**Start:**
```bash
docker compose up --build
```

**Pros:**
- ✅ Identical environment for all developers
- ✅ Matches production deployment
- ✅ No local Python/conda needed
- ✅ Easy to reset (docker compose down -v)

**Cons:**
- ❌ Slower iteration (5-10 seconds per backend restart)
- ❌ Harder to debug
- ❌ Logs require docker compose logs
- ❌ Container rebuild needed for dependency changes

---

### 3. Full Local Development

**When:** Maximum control, advanced debugging

**What:**
- Memgraph in Docker (or native install)
- Backend runs locally with `uvicorn --reload`
- Plugin builds locally with `npm run dev`
- Manual management of each service

**Start:**
```bash
# Terminal 1: Memgraph
docker run -p 7687:7687 -p 3000:3000 memgraph/memgraph-platform:latest

# Terminal 2: Backend
cd packages/backend
conda activate odin_backend
uvicorn core.restapi.api:app --reload

# Terminal 3: Plugin
cd packages/plugin
npm run dev
```

**Pros:**
- ✅ Maximum control
- ✅ See all logs directly in terminals
- ✅ Easy to restart individual services
- ✅ Best for debugging with breakpoints

**Cons:**
- ⚠️ More complex setup
- ⚠️ Multiple terminals to manage
- ⚠️ Easy to forget to start a service

---

## Recommendation by Task

| Task | Approach |
|------|----------|
| Adding new Python function | 🏆 Hybrid (start-dev.sh) |
| Adding new TypeScript component | 🏆 Hybrid (start-dev.sh) |
| Modifying LLM prompts | 🏆 Hybrid (start-dev.sh) |
| Adding Python dependency | 🏆 Hybrid (pip install -e .) |
| Adding npm dependency | 🏆 Hybrid (npm install) |
| Debugging Python with breakpoints | 🥈 Full Local (ipdb) |
| Testing before commit | 🥉 Full Docker |
| Troubleshooting "works on my machine" | 🥉 Full Docker |
| CI/CD pipeline | 🥉 Full Docker |
| Sharing with team | 🥉 Full Docker |

## Performance Comparison

Measured on MacBook Pro M1:

| Operation | Hybrid | Full Docker | Full Local |
|-----------|--------|-------------|------------|
| First startup | 10s | 60s | 5s |
| Python file change | 0.8s | 8s | 0.8s |
| TypeScript file change | 1.2s | 1.2s | 1.2s |
| Add Python dependency | 15s | 90s | 15s |
| View logs | instant | 2s | instant |
| Full rebuild | 30s | 120s | 30s |

## Quick Reference

```bash
# Hybrid (recommended)
./scripts/setup-dev.sh        # One time
./scripts/start-dev.sh        # Daily
./scripts/stop-dev.sh         # When done

# Full Docker
docker compose up --build     # Start
docker compose down           # Stop

# Full Local
# See approach 3 above
```

## Environment Variables

All approaches use `.env` file in the repo root:

```bash
OPENAI_API_KEY=sk-...
LLM_MODEL_NAME=gpt-4
MEMGRAPH_HOST=localhost        # Or "memgraph" for Docker
MEMGRAPH_PORT=7687
```

The hybrid approach automatically sources `.env` when starting the backend.

## Switching Between Approaches

You can switch freely:

```bash
# From Docker to Hybrid:
docker compose down
./scripts/start-dev.sh

# From Hybrid to Docker:
./scripts/stop-dev.sh
docker compose up

# From anything to clean state:
./scripts/stop-dev.sh
docker compose down -v
# Fresh start with any approach
```

## Summary

**For 90% of development work**: Use the hybrid approach (`./scripts/start-dev.sh`)

**Before committing**: Test with full Docker (`docker compose up --build`)

**For deep debugging**: Use full local with multiple terminals

This gives you the best of all worlds: fast iteration during development, but confidence that your changes work in a production-like environment before committing.

