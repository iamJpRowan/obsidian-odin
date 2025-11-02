# Testing Guide for ODIN Monorepo

This guide walks you through testing the monorepo setup.

## Quick Test (Automated)

Run the automated test script:

```bash
cd /Users/jprowan/Repos/obsidian-odin
bash test-setup.sh
```

This will check prerequisites and guide you through any missing requirements.

## Manual Testing Steps

### Prerequisites

Before starting, ensure you have:

1. **Docker Desktop** installed and running
   - Download: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version`

2. **OpenAI API Key** (for backend functionality)
   - Get from: https://platform.openai.com/api-keys
   - Needs GPT-4 access (recommended)

3. **Node.js** (optional, for plugin development)
   - Download: https://nodejs.org/ (v14+)
   - Verify: `node --version && npm --version`

### Step 1: Configure Environment

```bash
# Navigate to the repo
cd /Users/jprowan/Repos/obsidian-odin

# Copy the example environment file (if not already done)
cp .env.example .env

# Edit the .env file with your API key
nano .env  # or: code .env, vim .env, etc.
```

**Required edit in `.env`:**
```bash
# Change this line:
OPENAI_API_KEY=your_openai_api_key_here

# To your actual key:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Save and exit.

### Step 2: Test Plugin Build (Optional)

If you have Node.js installed and want to test the plugin build separately:

```bash
cd packages/plugin

# Install dependencies
npm install

# Build the plugin
npm run build

# Verify output
ls -lh main.js manifest.json
```

**Expected output:**
- `main.js` (compiled plugin, ~500KB-1MB)
- `manifest.json` (plugin metadata)

### Step 3: Start Docker Stack

```bash
# Return to project root
cd /Users/jprowan/Repos/obsidian-odin

# Start all services
docker compose up

# Or start in background:
# docker compose up -d
```

**What happens:**
1. Downloads Docker images (first time only, ~10 minutes)
2. Builds backend from `packages/backend/`
3. Starts Memgraph database (port 7687)
4. Starts Backend API (port 8000)
5. Builds plugin

**Wait for these messages:**
```
memgraph    | You are running Memgraph v2.15
odin-backend | INFO: Uvicorn running on http://0.0.0.0:8000
```

Press `Ctrl+C` to stop when done, or keep running for testing.

### Step 4: Verify Services

Open a **new terminal** (keep Docker running in the first):

#### Test 1: Backend API

```bash
# Test backend is responding
curl http://localhost:8000/docs

# Should return HTML of FastAPI docs page
```

Or open in browser: http://localhost:8000/docs

**Expected:** Interactive API documentation

#### Test 2: Memgraph Database

```bash
# Check container is running
docker ps | grep memgraph

# Connect to database
docker exec -it memgraph mgconsole

# Inside mgconsole, try:
SHOW STORAGE INFO;
EXIT;
```

#### Test 3: Check Logs

```bash
# Backend logs
docker compose logs backend

# Memgraph logs
docker compose logs memgraph

# Follow logs in real-time
docker compose logs -f
```

### Step 5: Test Plugin Files

```bash
cd /Users/jprowan/Repos/obsidian-odin/packages/plugin

# Check built files exist
ls -lh main.js manifest.json

# Verify manifest content
cat manifest.json
```

**Expected manifest.json:**
```json
{
  "id": "ODIN",
  "name": "ODIN",
  "version": "1.0.0",
  ...
}
```

### Step 6: Test in Obsidian

#### Option A: Symlink (Development)

```bash
# Create symlink to your vault's plugins folder
ln -s /Users/jprowan/Repos/obsidian-odin/packages/plugin \
      /path/to/your/vault/.obsidian/plugins/odin

# Example:
# ln -s /Users/jprowan/Repos/obsidian-odin/packages/plugin \
#       /Users/jprowan/Documents/MyVault/.obsidian/plugins/odin
```

#### Option B: Copy (Testing)

```bash
# Copy the plugin to your vault
cp -r /Users/jprowan/Repos/obsidian-odin/packages/plugin \
      /path/to/your/vault/.obsidian/plugins/odin
```

#### Enable in Obsidian

1. Open Obsidian
2. Settings → Community plugins
3. Turn off "Restricted mode"
4. Reload Obsidian (Ctrl/Cmd + R)
5. Find "ODIN" and toggle it ON

#### Verify Plugin Works

1. **Look for Graph Prompt View** in right sidebar
2. **Open the view** - should see:
   - Toggle: Vault view / File view
   - Graph visualization area
   - Prompt bar at bottom

3. **Test features:**
   - Switch to Vault view → Should show your vault as a graph
   - Switch to File view → Pick a note → Should show file-specific graph
   - Right-click text → Should see "Link prediction" and "Node suggestion"

4. **Check console for errors:**
   - Open Developer Tools: `Ctrl+Shift+I` (or `Cmd+Opt+I` on Mac)
   - Look for errors in Console tab

### Step 7: Test Backend Integration

With Docker still running and plugin enabled:

```bash
# Test initialization endpoint
curl -X POST http://localhost:8000/knowledge_base/general/init_local_repo \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/your/vault",
    "type": "Notes"
  }'

# Check response (should start processing)
```

**Note:** Replace `/path/to/your/vault` with actual vault path.

### Step 8: Query the Knowledge Graph

After initializing (may take a few minutes for large vaults):

```bash
# Connect to Memgraph
docker exec -it memgraph mgconsole

# Inside mgconsole:
# See all nodes
MATCH (n) RETURN n LIMIT 10;

# See relationships
MATCH (n)-[r]->(m) RETURN n.name, type(r), m.name LIMIT 20;

# Count nodes and edges
MATCH (n) RETURN count(n) as node_count;
MATCH ()-[r]->() RETURN count(r) as edge_count;

# Exit
EXIT;
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Or check port 7687 (Memgraph)
lsof -i :7687

# Stop Docker and restart
docker compose down
docker compose up
```

### Plugin Not Appearing

```bash
# Check plugin files exist
ls -la /path/to/vault/.obsidian/plugins/odin/

# Should have:
# - main.js
# - manifest.json

# Check Obsidian console for errors (Ctrl+Shift+I)
```

### Backend Connection Errors

```bash
# Check backend logs
docker compose logs backend

# Common issues:
# - Missing OPENAI_API_KEY in .env
# - API key invalid or no GPT-4 access
# - Port 8000 already in use

# Restart backend
docker compose restart backend
```

### Graph Not Populating

```bash
# Check Memgraph logs
docker compose logs memgraph

# Verify backend can reach Memgraph
docker exec odin-backend ping memgraph

# Check backend API is working
curl http://localhost:8000/docs
```

### Docker Build Failures

```bash
# Clean build
docker compose down -v  # WARNING: Deletes database!
docker compose build --no-cache
docker compose up
```

## Development Workflow

### Making Changes to Plugin

```bash
cd packages/plugin

# Watch mode (rebuilds on changes)
npm run dev

# In another terminal, test in Obsidian
# Changes will require Obsidian reload (Ctrl/Cmd + R)
```

### Making Changes to Backend

```bash
# Backend auto-reloads with Docker volumes
docker compose up

# Edit files in packages/backend/
# Changes should be reflected automatically

# To restart backend only:
docker compose restart backend
```

### Viewing Real-time Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f memgraph
```

## Clean Up

### Stop Services

```bash
# Stop containers (keeps data)
docker compose down

# Stop and remove volumes (DELETES graph data)
docker compose down -v
```

### Remove Test Data

```bash
# Remove built plugin
rm -f packages/plugin/main.js

# Remove dependencies
rm -rf packages/plugin/node_modules
```

## Success Checklist

- [ ] `.env` file created with valid API key
- [ ] Docker compose starts all services
- [ ] Backend API responds at http://localhost:8000/docs
- [ ] Memgraph accepts connections
- [ ] Plugin builds successfully (main.js created)
- [ ] Plugin appears in Obsidian
- [ ] Graph Prompt View visible in Obsidian
- [ ] Can switch between Vault and File views
- [ ] Right-click menu shows ODIN features
- [ ] Backend processes vault and creates graph

## Next Steps

Once everything is working:

1. **Customize prompts**: Edit `packages/backend/core/knowledgebase/prompts/`
2. **Add Obsidian syntax parsing**: Edit `packages/backend/core/knowledgebase/notes/VaultManager.py`
3. **Adjust graph visualization**: Edit `packages/plugin/src/ui/Graph/Graph.tsx`
4. **Change backend logic**: Edit `packages/backend/core/knowledgebase/`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidance.

---

**Need help?** Open an issue or check the logs!

