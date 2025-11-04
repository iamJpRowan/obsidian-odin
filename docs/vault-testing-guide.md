# Vault Testing Guide

This guide explains how to safely test importing your Obsidian vault data into ODIN before running on your full vault.

## Quick Start

```bash
# 1. Ensure backend is running
./scripts/start-dev.sh

# 2. Activate conda environment
conda activate odin_backend

# 3. Run test import (100 most recent files)
python scripts/test-vault-import.py /path/to/your/vault

# 4. Review results in Memgraph Lab
open http://localhost:3000
```

## Test Import Script

The `test-vault-import.py` script loads your 100 most recently modified files and processes them through the same pipeline as the plugin would.

### Features

- ✅ **Selective import**: Only imports most recent files (default: 100)
- ✅ **Same process**: Uses identical code path as plugin
- ✅ **Progress logging**: See exactly what's happening
- ✅ **Statistics**: Detailed timing and error reporting
- ✅ **Safe testing**: Can clear database before each test

### Usage

#### Basic Import (100 files)
```bash
python scripts/test-vault-import.py /path/to/your/vault
```

#### Custom Number of Files
```bash
python scripts/test-vault-import.py /path/to/your/vault --limit 50
```

#### Clear Database First
```bash
python scripts/test-vault-import.py /path/to/your/vault --clear-db
```

#### Verbose Logging (shows Cypher queries)
```bash
python scripts/test-vault-import.py /path/to/your/vault --verbose
```

#### Combined Options
```bash
python scripts/test-vault-import.py /path/to/your/vault --clear-db --limit 50 --verbose
```

### What the Script Does

1. **Scans your vault** for markdown files (`.md`, `.txt`)
2. **Selects most recent** files by modification time
3. **Processes each file**:
   - First file: Uses `text_to_cypher_create` (if DB is empty)
   - Subsequent files: Uses `data_and_text_to_cypher_update` (integrates with existing)
   - Executes Cypher queries in Memgraph
   - Adds to ChromaDB collection
4. **Updates embeddings** for all processed files
5. **Reports statistics** about the import

### Output Example

```
======================================================================
ODIN VAULT TEST IMPORT
======================================================================
Vault path: /Users/john/Documents/MyVault
File limit: 100
Clear DB: False
======================================================================

Scanning vault: /Users/john/Documents/MyVault
Found 5000 total files, selected 100 most recent

======================================================================
FILES TO IMPORT (most recent first)
======================================================================
    1. Projects/Project Alpha/notes.md (2025-01-15 14:32, 2,543 bytes)
    2. Daily Notes/2025-01-15.md (2025-01-15 12:10, 1,234 bytes)
    3. Research/Ideas.md (2025-01-15 11:45, 5,678 bytes)
    ...

======================================================================
[1/100] Processing: Projects/Project Alpha/notes.md
  File size: 2,543 characters
  Using CREATE prompt (first file, empty DB)
  Generated Cypher in 2.3s
  Executed in Memgraph (0.1s)
  Added to ChromaDB collection
  ✓ Completed in 2.5s

[2/100] Processing: Daily Notes/2025-01-15.md
  File size: 1,234 characters
  Using UPDATE prompt (integrating with existing data)
  Generated Cypher in 1.8s
  Executed in Memgraph (0.1s)
  Added to ChromaDB collection
  ✓ Completed in 2.0s

...

======================================================================
IMPORT STATISTICS
======================================================================
Files processed: 100/100
Files failed: 0

Timing:
  Total time: 5.2m
  Cypher generation: 3.1m (59.6%)
  Database execution: 0.2m (3.8%)
  Embedding generation: 1.9m (36.5%)

Average time per file: 3.1s
======================================================================
```

## Reviewing Results

### 1. Open Memgraph Lab

```bash
open http://localhost:3000
```

### 2. Run Basic Queries

```cypher
// See all nodes
MATCH (n) RETURN n LIMIT 50;

// Count by type
MATCH (n)
UNWIND labels(n) as label
RETURN label, count(*) as count
ORDER BY count DESC;

// See relationships
MATCH path = (n)-[r]->(m)
RETURN path
LIMIT 50;
```

### 3. Check Specific Files

```cypher
// Find nodes from a specific file
MATCH (n)
WHERE n.file_path CONTAINS 'your-note-name.md'
RETURN n;
```

### 4. Analyze Structure

Look for:
- ✅ Are key concepts extracted as nodes?
- ✅ Are relationships meaningful?
- ✅ Is the granularity appropriate?
- ⚠️ Too many/few node types?
- ⚠️ Missing important connections?

## Iterating on Prompts

If the data model doesn't match your expectations:

### 1. Review Current Prompts

```bash
# View the prompts being used
cat packages/backend/core/knowledgebase/prompts/prompt_generate
cat packages/backend/core/knowledgebase/prompts/system_message_generate
```

### 2. Modify Prompts

Edit the prompt files in `packages/backend/core/knowledgebase/prompts/`:
- `prompt_generate` - How first file creates graph
- `system_message_generate` - Instructions for graph creation
- `prompt_update` - How subsequent files integrate
- `system_message_update` - Instructions for integration

### 3. Test Again

```bash
# Clear and re-import to see changes
python scripts/test-vault-import.py /path/to/your/vault --clear-db
```

### 4. Compare Results

Use Memgraph Lab to compare:
- Node types created
- Relationship patterns
- Property structures

## Scaling Up

Once you're satisfied with 100 files:

### Test with More Files
```bash
python scripts/test-vault-import.py /path/to/your/vault --limit 500
```

### Full Vault Import

When ready, you can use the plugin's initialization or modify the script to process all files:

```bash
# Option 1: Use the plugin (when enabled)
# The plugin will call the backend API to import all files

# Option 2: Modify script to remove limit
# Edit scripts/test-vault-import.py and change default limit
```

## Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the conda environment
conda activate odin_backend

# Verify backend is accessible
cd packages/backend
python -c "from core.knowledgebase.MemgraphManager import MemgraphManager; print('OK')"
```

### "Cannot connect to Memgraph"
```bash
# Check if Memgraph is running
docker ps | grep memgraph

# Restart if needed
docker restart memgraph
```

### Import is too slow
- Each file makes an LLM call, which takes 1-3 seconds
- For 100 files, expect 5-10 minutes total
- Consider testing with fewer files first: `--limit 10`

### Files not found
- Verify the vault path is correct
- Check that files have `.md` or `.txt` extensions
- Ensure you have read permissions

### Errors during import
- Check backend logs: `tail -f backend.log`
- Try with `--verbose` to see detailed error messages
- Some files may fail (corrupted, encoding issues) - this is normal

## Best Practices

1. **Start small**: Test with 10-20 files first
2. **Review thoroughly**: Spend time in Memgraph Lab before scaling
3. **Iterate on prompts**: Tune the model structure before full import
4. **Document custom types**: If you add specific node types, document them
5. **Backup first**: Consider backing up your vault before full import
6. **Test incrementally**: Increase file count gradually (10 → 50 → 100 → 500)

## Next Steps

After successful testing:
- Review the [Memgraph Lab Guide](memgraph-lab-guide.md) for query patterns
- Tune prompts based on your vault's structure
- Plan your full vault import strategy
- Consider data validation queries

## Related Documentation

- [Memgraph Lab Guide](memgraph-lab-guide.md) - Visual graph exploration
- [Quick Dev Start](QUICK-DEV-START.md) - Development setup
- [Contributing Guide](contributing.md) - Codebase structure

