# ODIN Quick Start Guide

Get ODIN up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Docker and Docker Compose installed
- [ ] OpenAI API key (with GPT-4 access recommended)
- [ ] Obsidian installed with an active vault

## Installation Steps

### 1. Clone into Obsidian Plugins

```bash
# Navigate to your vault's plugins folder
cd /path/to/your/vault/.obsidian/plugins

# Clone the repository
git clone https://github.com/memgraph/odin.git obsidian-odin
cd obsidian-odin
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

**Minimum required in `.env`:**
```
OPENAI_API_KEY=sk-your-actual-api-key-here
LLM_MODEL_NAME=gpt-4
```

### 3. Start Services

```bash
# Start all services (Memgraph, Backend, Plugin build)
docker compose up
```

**Wait for:**
- ✓ Memgraph database starts (port 7687)
- ✓ Backend API starts (port 8000)
- ✓ Plugin builds successfully

This may take 5-10 minutes on first run.

### 4. Enable Plugin in Obsidian

1. Open Obsidian
2. Go to **Settings** → **Community plugins**
3. Click **"Turn on community plugins"** (disable restricted mode)
4. Find **"ODIN"** in the plugin list
5. Toggle it **ON**
6. Reload Obsidian if needed (Ctrl/Cmd + R)

### 5. Verify It's Working

1. Look for the **Graph Prompt View** in the right sidebar
2. Try switching between **Vault view** and **File view**
3. Right-click text in a note to see:
   - Link prediction
   - Node suggestion
   - Generate questions

## Troubleshooting

### Plugin doesn't appear
```bash
# Check that files exist
ls -la /path/to/vault/.obsidian/plugins/obsidian-odin/packages/plugin/main.js
ls -la /path/to/vault/.obsidian/plugins/obsidian-odin/packages/plugin/manifest.json

# If missing, rebuild
cd /path/to/vault/.obsidian/plugins/obsidian-odin/packages/plugin
npm run build
```

### Backend connection errors
```bash
# Check backend is running
curl http://localhost:8000/docs

# Check Docker containers
docker ps

# View backend logs
docker compose logs backend
```

### Graph not updating
```bash
# Check Memgraph is running
docker ps | grep memgraph

# Restart all services
docker compose restart
```

### OpenAI API errors
- Verify your API key is correct in `.env`
- Check you have GPT-4 access at https://platform.openai.com/
- Try `gpt-3.5-turbo` for testing (expect lower quality)

## Next Steps

### Customize for Your Vault

1. **Adjust LLM Prompts:**
   ```bash
   cd packages/backend/core/knowledgebase/prompts/
   # Edit prompt files to match your note-taking style
   ```

2. **Add Obsidian Syntax Support:**
   ```bash
   cd packages/backend/core/knowledgebase/notes/
   # Edit VaultManager.py to parse wikilinks, tags, etc.
   ```

3. **Query Your Graph Directly:**
   ```bash
   docker exec -it memgraph mgconsole
   
   # Try these Cypher queries:
   MATCH (n) RETURN n LIMIT 10;
   MATCH (n)-[r]->(m) RETURN n.name, type(r), m.name LIMIT 20;
   ```

### Development Mode

If you want to modify the code:

```bash
# Plugin development (auto-rebuilds)
cd packages/plugin
npm install
npm run dev

# Backend development (auto-reloads)
cd packages/backend
conda create --name odin_backend python=3.9.16
conda activate odin_backend
pip install -e .
uvicorn core.restapi.api:app --reload
```

## Useful Commands

```bash
# Start services in background
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f plugin

# Rebuild after code changes
docker compose up --build

# Clean everything (including database)
docker compose down -v
```

## Key Files to Know

- **`.env`** - Your configuration (API keys, model settings)
- **`packages/plugin/src/`** - Plugin UI code (TypeScript/React)
- **`packages/backend/core/knowledgebase/prompts/`** - LLM prompts (customize here!)
- **`packages/backend/core/knowledgebase/notes/VaultManager.py`** - Vault parsing logic
- **`docker-compose.yml`** - Service orchestration

## Get Help

- **Backend API Docs:** http://localhost:8000/docs (when running)
- **Issue Tracker:** https://github.com/memgraph/odin/issues
- **Full Docs:** See [README.md](README.md)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Happy knowledge graphing!** 🧠📊

