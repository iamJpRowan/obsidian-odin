---
date: 2025-11-02
title: Monorepo Setup and Backend Integration
contributors:
  human:
    name: jprowan
    role: lead_developer
  ai:
    model: Claude Sonnet 3.5
    provider: Anthropic
    interface: Cursor IDE
collaboration:
  style: pair_programming
  human_focus: architecture decisions, requirements definition, validation
  ai_focus: implementation, file operations, documentation writing
duration_hours: 2.5
tags: [refactor, monorepo, backend-integration, docker, documentation, langchain]
---

# Monorepo Setup and Backend Integration

## Collaboration Summary

**Human Developer:** jprowan  
**AI Assistant:** Claude Sonnet 3.5 (Anthropic)  
**Development Environment:** Cursor IDE  
**Session Date:** 2025-11-02  
**Duration:** ~2.5 hours  
**Collaboration Style:** AI-driven pair programming with human oversight and decision-making

---

## Context

The ODIN Obsidian plugin was originally a frontend-only repository that required users to separately install and configure the BOR backend. This created friction for users who wanted to customize the knowledge graph extraction logic or understand the full data flow from UI to database.

**Goal:** Transform the repository into a monorepo containing both the plugin and backend, making it easier to customize, develop, and understand the complete system.

## What We Accomplished

### 1. Repository Restructuring

**Before:**
```
obsidian-odin/
├── src/          # Plugin code
├── manifest.json
├── package.json
└── ...
```

**After:**
```
obsidian-odin/
├── packages/
│   ├── plugin/     # Plugin (TypeScript/React)
│   └── backend/    # BOR Backend (Python/FastAPI)
├── docker-compose.yml
├── .env.example
└── Documentation files
```

### 2. Files Created

#### Configuration
- **`.env.example`** - Complete environment configuration template
- **`package.json`** (root) - npm workspaces configuration
- **`docker-compose.yml`** (updated) - Monorepo-aware service orchestration

#### Documentation
- **`CONTRIBUTING.md`** - Comprehensive developer guide with data flow diagrams
- **`QUICKSTART.md`** - 5-minute setup guide
- **`TESTING.md`** - Step-by-step testing instructions
- **`README.md`** (rewritten) - Complete project documentation
- **`test-setup.sh`** - Automated setup verification script
- **`docs.md`** (updated) - Docker image building guide

### 3. Backend Integration

- Integrated complete BOR backend codebase from https://github.com/memgraph/bor
- Fixed missing dependencies (`langchain-community`, `langchain-openai`)
- All backend code including:
  - FastAPI REST endpoints
  - LLM prompt templates (customizable!)
  - Memgraph database integration
  - Knowledge graph processing logic

### 4. Services Running

All three services are now running and communicating:

```
✅ memgraph       - Graph database (ports 7687, 7444)
✅ odin-backend   - FastAPI server (port 8000)
✅ odin-plugin    - Frontend build (port 1234)
```

**Backend API is accessible at:** http://localhost:8000/docs

### 5. Issue Fixed During Setup

**Problem:** Backend was failing to start with `ModuleNotFoundError: No module named 'langchain_community'`

**Solution:** Updated `packages/backend/requirements.txt` to include:
- `langchain-community`
- `langchain-openai`

## Key Decisions

| Decision | Made By | Rationale |
|----------|---------|-----------|
| Adopt monorepo structure | jprowan | Enable easier customization and understanding of full stack |
| Use `packages/` convention | AI (Claude) | Industry standard for monorepos (used by Babel, Jest, etc.) |
| Integrate full BOR backend | jprowan | Core requirement for customization goal |
| Fix langchain dependencies | AI (Claude) | Identified missing modules during Docker build troubleshooting |
| Preserve git history with `git mv` | AI (Claude) | Maintain file history for future reference |
| Create comprehensive docs | Joint decision | Lower barrier to entry for new users/contributors |

## Challenges and Solutions

### Challenge 1: Missing Python Dependencies
**Problem:** Backend container failed to start with module import errors.

**Solution:** AI identified missing `langchain-community` and `langchain-openai` packages during error analysis. Updated `requirements.txt` to include these dependencies.

### Challenge 2: Preserving Git History
**Problem:** Moving files to new directory structure could lose git history.

**Solution:** Used `git mv` for all file relocations to preserve commit history and blame information.

### Challenge 3: Documentation Coherence
**Problem:** Multiple documentation files needed to be consistent and cross-referenced.

**Solution:** Created clear hierarchy with README as entry point, QUICKSTART for speed, and CONTRIBUTING for depth.

## Testing Status

### ✅ Completed Tests

1. **Docker Setup**
   - All containers build successfully
   - All services start and stay running
   - Backend API responds correctly

2. **Backend API**
   - Swagger UI accessible at http://localhost:8000/docs
   - FastAPI server running without errors
   - Memgraph database connected

3. **Configuration**
   - `.env` file created with API key
   - Environment variables loading correctly
   - Docker compose orchestration working

### ⏭️ Next Steps for Users

1. **Test in Obsidian:**
   ```bash
   # Symlink to your vault's plugins folder
   ln -s /Users/jprowan/Repos/obsidian-odin/packages/plugin \
         /path/to/your/vault/.obsidian/plugins/odin
   
   # Enable plugin in Obsidian settings
   ```

2. **Initialize Your Vault:**
   - Backend needs to process your vault
   - This creates the knowledge graph
   - May take several minutes for large vaults

3. **Customize Prompts:**
   - Edit `packages/backend/core/knowledgebase/prompts/`
   - Adjust how GPT-4 extracts relationships
   - Add Obsidian-specific syntax parsing

## Key Benefits of Monorepo

1. **Single Source of Truth** - Everything in one place
2. **Easy Customization** - Can modify both frontend and backend
3. **Better Documentation** - Full data flow is visible
4. **Coordinated Development** - Changes to both sides stay in sync
5. **Simplified Testing** - One `docker compose up` starts everything

## AI Contribution Notes

**Claude Sonnet 3.5** provided:
- File restructuring operations using git commands
- Docker configuration updates for monorepo structure
- Complete documentation writing (README, QUICKSTART, TESTING, CONTRIBUTING)
- Dependency troubleshooting and resolution
- Automated test script creation
- Best practices research for monorepo structure

**Capabilities leveraged:**
- File read/write operations across 100+ files
- Git integration (mv, status checking)
- Codebase semantic understanding
- Multi-language fluency (Python, TypeScript, Bash, Docker, Markdown)
- Documentation generation with proper formatting

**Limitations encountered:**
- Required human approval for git operations
- No direct terminal execution (proposed commands for approval)
- Needed human validation for architectural decisions

## Human Contribution Notes

**jprowan** provided:
- Initial vision for monorepo structure
- Strategic decision to integrate BOR backend
- OpenAI API key configuration
- Validation of all proposed changes
- Git commit authority
- Project direction and requirements

**Domain expertise:**
- Understanding of Obsidian plugin ecosystem
- Knowledge of target user needs
- Requirements for customization features

## Directory Structure (Final)

```
obsidian-odin/
├── packages/
│   ├── plugin/              # Obsidian plugin (TypeScript/React)
│   │   ├── src/
│   │   │   ├── index.ts    # Plugin entry point
│   │   │   ├── ui/         # React components
│   │   │   ├── model/      # TypeScript models
│   │   │   └── util/       # Helper functions
│   │   ├── manifest.json   # Obsidian manifest
│   │   ├── package.json
│   │   └── esbuild.config.mjs
│   │
│   └── backend/             # BOR Backend (Python/FastAPI)
│       ├── core/
│       │   ├── knowledgebase/
│       │   │   ├── notes/          # Vault processing
│       │   │   ├── prompts/        # ⭐ LLM prompts (customize!)
│       │   │   ├── QueryAgents.py  # AI query handlers
│       │   │   └── VaultManager.py # ⭐ Add custom parsers here
│       │   └── restapi/
│       │       └── api.py          # FastAPI endpoints
│       ├── requirements.txt
│       └── Dockerfile
│
├── docker-compose.yml       # Orchestrates all services
├── .env.example             # Configuration template
├── .env                     # Your actual config (git ignored)
│
├── README.md                # Main documentation
├── QUICKSTART.md            # 5-minute setup
├── TESTING.md               # Testing guide
├── CONTRIBUTING.md          # Developer guide
├── test-setup.sh            # Automated setup checker
│
└── package.json             # Root workspace config
```

## Commands Reference

### Development
```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Rebuild after code changes
docker compose up --build

# View logs
docker compose logs -f backend
```

### Testing
```bash
# Run automated setup check
bash test-setup.sh

# Test backend API
curl http://localhost:8000/docs

# Check service status
docker ps
```

### Troubleshooting
```bash
# Stop everything
docker compose down

# Stop and remove volumes (fresh start)
docker compose down -v

# View specific service logs
docker logs odin-backend
docker logs memgraph
```

## What's Different from Original BOR

1. **Fixed Dependencies** - Added missing langchain packages
2. **Integrated Structure** - Everything in one repo
3. **Better Docs** - Complete setup and customization guides
4. **Automated Testing** - Setup verification script
5. **Development Ready** - Easy to modify and extend

## Success Metrics

- ✅ All Docker containers running
- ✅ Backend API responding (http://localhost:8000/docs)
- ✅ Memgraph database connected
- ✅ No critical errors in logs
- ✅ Complete documentation created
- ✅ Git history preserved (used `git mv`)

## Future Considerations

- Add CI/CD pipeline for automated testing
- Create example vault configurations
- Add more detailed customization examples
- Consider adding pre-commit hooks for code quality
- Explore adding tests for backend endpoints
- Document common vault structure patterns

## Related Resources

- **Backend API Docs:** http://localhost:8000/docs (when running)
- **Original BOR:** https://github.com/memgraph/bor
- **Obsidian Plugin API:** https://github.com/obsidianmd/obsidian-api
- **Memgraph Docs:** https://memgraph.com/docs
- **LangChain Docs:** https://python.langchain.com/

## Git Commit Information

**Commit message:**
```bash
refactor: convert to monorepo with integrated BOR backend

Major changes:
- Restructure as monorepo with packages/plugin and packages/backend
- Integrate BOR backend from https://github.com/memgraph/bor
- Fix backend dependencies (add langchain-community, langchain-openai)
- Add comprehensive documentation (README, QUICKSTART, TESTING, CONTRIBUTING)
- Update docker-compose for monorepo structure
- Add .env.example with all configuration options
- Add automated test-setup.sh script

This allows users to customize both frontend and backend in one place,
making it easier to tune relationship extraction for their specific vaults.
```

**Files affected:**
- 100+ files added (BOR backend integration)
- 30+ files moved (frontend restructuring)
- 5 new documentation files
- 1 dependency fix (requirements.txt)

---

**Attribution:** This work represents a collaboration between jprowan (human developer) providing project vision, architectural decisions, and validation, and Claude Sonnet 3.5 (AI assistant via Cursor IDE) assisting with implementation, file operations, documentation generation, and technical research. All strategic decisions were made by the human; AI provided execution and technical recommendations subject to human approval.

