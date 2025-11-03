---
date: 2025-01-15
title: Migrated to Memgraph Platform with Lab Web Interface
contributors:
  human:
    name: jprowan
    role: lead_developer
  ai:
    model: Claude Sonnet 4.5
    provider: Anthropic
    interface: Cursor IDE
collaboration:
  style: pair_programming
  human_focus: architecture, decisions, validation
  ai_focus: implementation, documentation, research
duration_hours: 0.5
tags: [docker, memgraph, devops, ui, database]
---

# Migrated to Memgraph Platform with Lab Web Interface

## Collaboration Summary

**Human Developer:** jprowan  
**AI Assistant:** Claude Sonnet 4.5 (Anthropic)  
**Development Environment:** Cursor IDE  
**Session Date:** 2025-01-15  
**Duration:** ~0.5 hours  
**Collaboration Style:** Human requested migration to platform image for GUI access, AI implemented and documented changes

---

## Context

Previously, ODIN used the `memgraph-mage` Docker image which only provided the database without a visual interface. To enable easier testing and tuning of vault data imports, we needed a way to visualize and explore the graph database without using terminal queries.

The user wanted to:
- Test importing vault data and see what gets written to Memgraph
- Tune the data model to align with their vault structure
- Have visibility into the import process without terminal-only tools

## What We Accomplished

1. **Migrated to Memgraph Platform Image**
   - Changed from `memgraph-mage:1.15-memgraph-2.15` to `memgraph-platform:latest`
   - Updated all Docker configurations (root docker-compose.yml and backend docker-compose.yml)
   - Updated startup scripts to use the new image

2. **Added Memgraph Lab Web Interface**
   - Exposed port 3000 for the Lab web UI
   - Updated documentation to include Lab access
   - Added Lab to the services table in quick start guide

3. **Created Comprehensive Documentation**
   - New `docs/memgraph-lab-guide.md` with:
     - Query examples for vault testing
     - Visualization tips
     - Workflow for reviewing imports
     - Troubleshooting guide

4. **Updated All References**
   - Modified setup scripts to pull correct image
   - Updated README with new Docker commands
   - Updated workflow comparison docs
   - Added Lab URL to startup script output

## Key Decisions

| Decision | Made By | Rationale |
|----------|---------|-----------|
| Use `latest` tag instead of `2.15` | AI | ARM64 architecture support - `2.15` tag doesn't have ARM64 build, `latest` works on all platforms |
| Keep port 3000 for Lab | Both | Standard default port for Memgraph Lab web interface |
| Include Lab in Docker rather than separate install | Human | Better developer experience - starts with services, no separate installation needed |
| Create comprehensive Lab guide | AI | Users need query examples and workflows for vault testing use case |

## Challenges and Solutions

### Challenge: ARM64 Compatibility
The `memgraph-platform:2.15` tag wasn't available for ARM64 (Apple Silicon), causing the initial pull to fail.

**Solution:** Switched to `memgraph-platform:latest` which has multi-architecture support including ARM64. This works on all platforms while still providing the latest stable version.

### Challenge: Documentation Consistency
Multiple files referenced the old image name and needed updates.

**Solution:** Systematically updated all references:
- Root docker-compose.yml
- Backend docker-compose.yml  
- setup-dev.sh
- start-dev.sh
- README.md
- docs/QUICK-DEV-START.md
- docs/dev-workflow-comparison.md

## Technical Details

### Docker Configuration Changes

**Before:**
```yaml
memgraph:
  image: memgraph/memgraph-mage:1.15-memgraph-2.15
  ports:
    - "7687:7687"
    - "7444:7444"
```

**After:**
```yaml
memgraph:
  image: memgraph/memgraph-platform:latest
  ports:
    - "7687:7687"   # Bolt protocol (database connection)
    - "3000:3000"   # Memgraph Lab web interface
    - "7444:7444"   # Monitoring
```

### Access Points

After starting the dev environment:
- **Database:** `localhost:7687` (Bolt protocol)
- **Web UI:** `http://localhost:3000` (Memgraph Lab)
- **Monitoring:** `localhost:7444` (optional)

### Startup Script Updates

The `start-dev.sh` script now:
- Creates container with port 3000 exposed
- Displays Lab URL in startup summary
- Pulls `memgraph-platform:latest` image

## AI Contribution Notes

- Researched Memgraph Platform vs MAGE image differences
- Identified ARM64 compatibility issue and solution
- Created comprehensive Lab guide with query examples
- Updated all configuration files systematically
- Ensured documentation consistency across all files

## Human Contribution Notes

- Requested migration to enable GUI access for testing
- Validated approach of including Lab in Docker stack
- Confirmed preference for web interface over separate desktop app installation
- Provided context about vault testing workflow needs

## Future Considerations

- Consider adding Lab to production Docker setup if needed
- May want to add authentication for Lab in production environments
- Could add custom query presets for common vault inspection tasks
- Consider documenting Lab keyboard shortcuts and advanced features

## Related Resources

- **Files Changed:** 
  - docker-compose.yml
  - packages/backend/docker-compose.yml
  - scripts/setup-dev.sh
  - scripts/start-dev.sh
  - README.md
  - docs/QUICK-DEV-START.md
  - docs/dev-workflow-comparison.md
  - docs/memgraph-lab-guide.md (new)

- **Documentation:** 
  - [Memgraph Lab Guide](../docs/memgraph-lab-guide.md)
  - [Memgraph Platform Docs](https://memgraph.com/docs/memgraph-lab)

- **External Resources:** 
  - [Memgraph Download Hub](https://memgraph.com/download)
  - [Memgraph Lab Documentation](https://memgraph.com/docs/memgraph-lab)

---

**Attribution:** This work represents a collaboration between jprowan providing project direction and validation, and Claude Sonnet 4.5 via Cursor IDE assisting with implementation and documentation.

