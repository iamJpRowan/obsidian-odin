# Memgraph Lab Guide for Vault Testing

This guide shows you how to use Memgraph Lab to review and tune your vault data model.

## Quick Access

After starting your dev environment with `./scripts/start-dev.sh`:

```bash
open http://localhost:3000
```

Or visit: **http://localhost:3000** in your browser

## First Time Setup

When you first open Memgraph Lab:

1. **Connect to Database**
   - Click "Connect to Memgraph" if prompted
   - Connection settings are pre-configured:
     - Host: `localhost`
     - Port: `7687`
     - No authentication needed

2. You should see the main interface with:
   - Query editor at the top
   - Graph visualization in the center
   - Query history/results at the bottom

## Useful Queries for Vault Testing

### Basic Database Inspection

```cypher
// Count all nodes
MATCH (n) RETURN count(n) as total_nodes;

// See all node types (labels)
MATCH (n) 
RETURN DISTINCT labels(n) as node_type, count(*) as count
ORDER BY count DESC;

// See all relationship types
MATCH ()-[r]->()
RETURN DISTINCT type(r) as relationship_type, count(*) as count
ORDER BY count DESC;

// View database schema
CALL schema.node_type_properties() YIELD nodeLabels, propertyName, propertyTypes
RETURN nodeLabels, propertyName, propertyTypes;
```

### Inspecting Individual Files

```cypher
// Find all nodes from a specific file
MATCH (n)
WHERE n.file_path CONTAINS 'your-note-name.md'
RETURN n;

// Find all nodes from a specific file with their relationships
MATCH path = (n)-[r]-(m)
WHERE n.file_path CONTAINS 'your-note-name.md'
RETURN path
LIMIT 50;

// Get all file paths in the database
MATCH (n)
WHERE n.file_path IS NOT NULL
RETURN DISTINCT n.file_path
ORDER BY n.file_path;
```

### Exploring Graph Structure

```cypher
// View a sample subgraph (random 50 connections)
MATCH path = (n)-[r]->(m)
RETURN path
LIMIT 50;

// Find nodes with the most connections (hubs)
MATCH (n)-[r]-()
RETURN n, labels(n) as type, count(r) as connections
ORDER BY connections DESC
LIMIT 20;

// Find nodes with no connections (isolated)
MATCH (n)
WHERE NOT (n)--()
RETURN n, labels(n) as type;
```

### Testing Your Data Model

```cypher
// See what properties exist on a specific node type
MATCH (n:YourNodeType)
RETURN DISTINCT keys(n) as properties
LIMIT 1;

// Count nodes by type
MATCH (n)
UNWIND labels(n) as label
RETURN label, count(*) as count
ORDER BY count DESC;

// Find multi-labeled nodes (if any)
MATCH (n)
WHERE size(labels(n)) > 1
RETURN n, labels(n) as all_labels;
```

## Visualization Tips

### Style Graph Nodes

Click on a node in the visualization to:
- See all its properties
- Expand its connections
- Style it (color, size, etc.)

### Customize Display

1. **Settings (gear icon)**
   - Adjust physics simulation
   - Change node/edge colors
   - Set label properties

2. **Graph Style Sheet**
   - Click on node types in the legend
   - Customize appearance per node type
   - Set which property shows as label

### Better Visualization

```cypher
// Limit results for cleaner graphs
MATCH path = (n)-[r]->(m)
RETURN path
LIMIT 25;

// Focus on specific relationship types
MATCH path = (n)-[r:MENTIONS]->(m)
RETURN path
LIMIT 50;

// Depth-limited exploration from a node
MATCH path = (start)-[*1..2]-(connected)
WHERE start.file_path CONTAINS 'starting-note.md'
RETURN path;
```

## Workflow for Testing Vault Import

### 1. Start Fresh
```cypher
// Clear all data (CAUTION: destroys all data!)
MATCH (n) DETACH DELETE n;
```

### 2. Import a Test File
Use your test import script or the backend API to import 1-3 representative notes.

### 3. Review Results
```cypher
// See what was created
MATCH (n)
RETURN n;

// Check the structure
MATCH path = (n)-[r]->(m)
RETURN path;
```

### 4. Analyze the Model

Ask yourself:
- Are the right concepts being extracted?
- Are relationships meaningful?
- Are node types appropriate?
- Are important properties captured?
- Is there too much/too little granularity?

### 5. Iterate

If the model isn't right:
1. Adjust your prompt templates in `packages/backend/core/knowledgebase/prompts/`
2. Clear the database
3. Re-import the same test files
4. Compare the results in Memgraph Lab

## Common Patterns to Look For

### Good Signs

✅ Concepts from your notes become nodes
✅ Relationships reflect actual connections in your thinking
✅ Similar concepts are linked together
✅ File structure is preserved in properties

### Warning Signs

⚠️ Too many unique node types (over-fragmentation)
⚠️ Too few node types (under-fragmentation)
⚠️ Disconnected nodes that should be related
⚠️ Missing important concepts from the text
⚠️ Relationships pointing the wrong direction

## Exporting Results

### Save a Query

Click the "Save" icon next to a query to keep it for later reference.

### Export Data

```cypher
// Export as JSON format (copy from results)
MATCH (n)
RETURN n
LIMIT 100;
```

Or use the API endpoint:
```bash
curl http://localhost:8000/knowledge_base/general/get_all_for_repo \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/vault"}' \
  > vault_export.json
```

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter` - Run query
- `Ctrl/Cmd + Space` - Autocomplete
- `Escape` - Clear selection
- Double-click node - Expand connections

## Troubleshooting

### "No database connection"
```bash
# Check if Memgraph is running
docker ps | grep memgraph

# Restart if needed
docker restart memgraph
```

### "Query too slow"
- Add `LIMIT` clauses to large queries
- Use `WHERE` clauses to filter early
- Index frequently queried properties

### "Can't see my data"
```cypher
// Verify data exists
MATCH (n) RETURN count(n);

// Check if it's in the right database
CALL mg.procedures() YIELD *;
```

## Next Steps

Once you're comfortable with Memgraph Lab:
1. Test with progressively larger subsets of your vault
2. Tune your prompts based on what you see
3. Document any custom node types or relationships you want
4. Create saved queries for common inspection tasks

## Resources

- [Cypher Query Language](https://memgraph.com/docs/cypher-manual)
- [Memgraph Lab Documentation](https://memgraph.com/docs/memgraph-lab)
- ODIN Backend: `packages/backend/core/knowledgebase/`
- Prompt Templates: `packages/backend/core/knowledgebase/prompts/`

