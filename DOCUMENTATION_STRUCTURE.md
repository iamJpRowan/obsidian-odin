# Documentation Structure

This document outlines the documentation structure for the local LLM implementation.

## File Organization

### Quick Start
- **[START_HERE.md](START_HERE.md)** - Entry point for new users, quick setup guide

### Main Documentation (`docs/`)
- **[docs/README.md](docs/README.md)** - Documentation index with all guides
- **[docs/local-llm-setup.md](docs/local-llm-setup.md)** - Complete local LLM setup and configuration guide
- `docs/quickstart.md` - General ODIN quickstart (from main branch)
- `docs/contributing.md` - Developer guide (from main branch)
- `docs/testing.md` - Testing guide (from main branch)
- `docs/docker-build.md` - Docker guide (from main branch)

### Development Log (`devlog/`)
- **[devlog/2025-11-03-local-llm-implementation.md](devlog/2025-11-03-local-llm-implementation.md)** - Detailed implementation notes for local LLM feature
- `devlog/README.md` - Devlog index and guidelines
- `devlog/template.md` - Template for future devlog entries

### Helper Scripts
- **[test_local_llm.sh](test_local_llm.sh)** - Automated setup verification script
- **[packages/backend/core/run_server_venv.sh](packages/backend/core/run_server_venv.sh)** - Server startup with venv activation

## Documentation Hierarchy

```
START_HERE.md                           # Entry point
    ├─→ docs/local-llm-setup.md        # Full setup guide
    │       ├─→ Configuration options
    │       ├─→ Model selection
    │       ├─→ Performance tuning
    │       └─→ Troubleshooting
    │
    ├─→ devlog/2025-11-03...md         # Implementation details
    │       ├─→ Technical decisions
    │       ├─→ Challenges & solutions
    │       └─→ Future considerations
    │
    └─→ docs/README.md                  # All documentation
            ├─→ docs/quickstart.md
            ├─→ docs/contributing.md
            ├─→ docs/testing.md
            └─→ docs/docker-build.md
```

## Modified Files (Code)

1. **packages/backend/core/knowledgebase/constants.py**
   - Added LLM_PROVIDER and EMBEDDING_PROVIDER configuration
   - Added OLLAMA_BASE_URL configuration

2. **packages/backend/core/knowledgebase/TextAnalizer.py**
   - Added conditional LLM provider selection (Ollama vs OpenAI)

3. **packages/backend/core/knowledgebase/QueryAgents.py**
   - Added conditional LLM provider selection
   - Added appropriate agent type for each provider

4. **packages/backend/core/knowledgebase/notes/CollectionManager.py**
   - Added conditional embedding provider selection

5. **packages/backend/core/knowledgebase/notes/Embeddings.py**
   - Implemented local embedding generation with sentence-transformers

6. **packages/backend/requirements.txt**
   - Added sentence-transformers dependency

7. **packages/backend/template.env**
   - Updated with LLM and embedding provider configuration options

## Documentation Standards

All documentation follows these principles:

### Structure
- Clear hierarchy from quick start to deep technical details
- Cross-references between related documents
- Consistent formatting and style

### Content
- **Quick starts** - Get users running immediately
- **Setup guides** - Comprehensive configuration details
- **Devlogs** - Technical implementation details and decisions
- **Helper scripts** - Automated verification and setup

### Maintenance
- Devlog entries dated and immutable (historical record)
- Guides updated as features evolve
- Cross-references updated when structure changes

## For Developers

When adding features:

1. **Update relevant guides** in `docs/` (usually `local-llm-setup.md` or `contributing.md`)
2. **Create devlog entry** in `devlog/YYYY-MM-DD-feature-name.md` using the template
3. **Update docs/README.md** if adding new documentation files
4. **Update START_HERE.md** if changing quick start procedure

## For Users

Reading order for new users:

1. **START_HERE.md** - Quick overview and immediate steps
2. **docs/local-llm-setup.md** - Detailed setup and configuration
3. **test_local_llm.sh** - Verify your setup works
4. **devlog/** (optional) - Understand technical decisions and implementation

## Navigation Tips

- Start with `START_HERE.md` for quick setup
- Use `docs/README.md` as central navigation hub
- Check `docs/local-llm-setup.md` for troubleshooting
- Read devlog for understanding "why" decisions were made
- Run `test_local_llm.sh` anytime to verify setup

---

**Note:** This structure follows ODIN's established documentation patterns from the main repository while adding local LLM specific content in the appropriate places.

