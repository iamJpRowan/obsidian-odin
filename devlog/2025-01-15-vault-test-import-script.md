---
date: 2025-01-15
title: Vault Test Import Script and Cypher Generation Improvements
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
  human_focus: architecture, decisions, validation, testing
  ai_focus: implementation, documentation, prompt engineering
duration_hours: 2.5
tags: [vault-import, cypher, llm, testing, prompt-engineering, memgraph]
---

# Vault Test Import Script and Cypher Generation Improvements

## Collaboration Summary

**Human Developer:** jprowan  
**AI Assistant:** Claude Sonnet 4.5 (Anthropic)  
**Development Environment:** Cursor IDE  
**Session Date:** 2025-01-15  
**Duration:** ~2.5 hours  
**Collaboration Style:** Human guided testing and validation, AI implemented improvements and fixes

---

## Context

The user wanted to test importing their Obsidian vault data (thousands of files) into ODIN before running on the full vault. This required:
1. A safe way to import small portions for testing
2. Visibility into what gets written to Memgraph
3. Ability to tune the data model to match their vault structure
4. Fixing Cypher generation issues that were preventing successful imports

## What We Accomplished

1. **Created Test Vault Import Script**
   - `scripts/test-vault-import.py` - Selective import of N most recent files
   - Progress logging with detailed statistics
   - Database statistics after import
   - Configurable file limits and database clearing

2. **Fixed Cypher Generation Issues**
   - Added Cypher extraction from LLM markdown responses
   - Implemented post-processing to fix common syntax errors:
     - Removed MATCH statements after CREATE
     - Fixed DATETIME() function calls (Memgraph doesn't support this)
     - Validated Cypher structure before execution
   - Improved prompts with explicit syntax rules and examples

3. **Improved Prompts**
   - Created `system_message_generate_improved` with:
     - Explicit Cypher syntax rules
     - Examples of correct/incorrect patterns
     - Clear instructions to output only Cypher code
   - Added fallback mechanism to use improved prompts when available

4. **Fixed ChromaDB Collection Management**
   - Fixed collection recreation after `delete_all()` resets ChromaDB
   - Updated `.gitignore` to exclude ChromaDB data directories

5. **Enhanced Documentation**
   - `docs/vault-testing-guide.md` - Comprehensive guide for testing vault imports
   - `docs/improving-cypher-generation.md` - Strategies for improving LLM output
   - Updated `docs/QUICK-DEV-START.md` with testing workflow

## Key Decisions

| Decision | Made By | Rationale |
|----------|---------|-----------|
| Create selective import script (100 files) | Human | Needed safe testing before full vault import |
| Extract Cypher from markdown code blocks | AI | LLM was returning explanations with code blocks |
| Post-process Cypher to fix errors | Both | Faster than retraining model, immediate results |
| Use improved prompts with fallback | AI | Backward compatible, easy to test |
| Fix ChromaDB collection after reset | AI | Collection reference was stale after reset |
| Add ChromaDB to .gitignore | Human | Data directory shouldn't be in version control |

## Challenges and Solutions

### Challenge 1: LLM Returning Explanations Instead of Pure Cypher
The LLM was generating markdown-formatted responses with explanations before the Cypher code.

**Solution:** Created `extract_cypher_from_response()` method that:
- Extracts code from markdown code blocks (```cypher ... ```)
- Handles multiple code block formats
- Falls back to extracting Cypher after keywords like "Cypher Queries:"

### Challenge 2: Invalid Cypher Syntax
Generated Cypher had several syntax errors:
- MATCH statements after CREATE (won't find newly created nodes)
- DATETIME() function calls (not supported in Memgraph)
- Inline node creation in relationships

**Solution:** Implemented `fix_common_cypher_errors()` that:
- Removes MATCH statements when CREATE has been used
- Converts DATETIME() calls to string literals
- Validates query structure

### Challenge 3: ChromaDB Collection Error
After clearing database, ChromaDB collection was deleted but reference remained.

**Solution:** Added collection recreation after `delete_all()`:
```python
cm.delete_all()
cm._make_collection(cm.collection_name)  # Recreate after reset
```

### Challenge 4: File Selection for Testing
User wanted to test with representative recent files, not random selection.

**Solution:** Script sorts files by modification time and selects N most recent, providing visibility into what will be imported.

## Technical Details

### Test Import Script Features

**File Selection:**
- Sorts by modification time (newest first)
- Filters markdown and text files only
- Skips hidden directories and Obsidian system files
- Shows preview of files to be imported

**Progress Tracking:**
- Real-time logging of each file processed
- Timing statistics per file and overall
- Progress updates every 10 files with ETA
- Error reporting with file-specific details

**Database Statistics:**
- Node count and types
- Relationship types
- Files represented in graph
- Query examples for Memgraph Lab

### Cypher Extraction Logic

```python
@staticmethod
def extract_cypher_from_response(response: str) -> str:
    # 1. Try markdown code blocks (```cypher ... ```)
    # 2. Try generic code blocks with Cypher keywords
    # 3. Extract after keywords like "Cypher Queries:"
    # 4. Fall back to pure Cypher if starts with CREATE/MERGE
```

### Post-Processing Fixes

```python
@staticmethod
def fix_common_cypher_errors(cypher: str) -> str:
    # - Remove MATCH after CREATE
    # - Fix DATETIME() -> string
    # - Validate structure
```

### Improved Prompt Structure

**System Message:**
- Explicit syntax rules (8 rules)
- Examples of correct patterns
- Examples of incorrect patterns (what NOT to do)
- Clear instruction: "Output ONLY Cypher code"

**User Prompt:**
- Simplified format
- Reminder about structure
- Emphasis on no explanations

## Test Results

### Initial Test (2 files)
- ✅ 100% success rate
- ✅ Cypher executed successfully
- ✅ Nodes created in Memgraph
- ✅ Files added to ChromaDB

### Scale Test (100 files - partial)
- Processed 18 files successfully
- Success rate: ~83% (15/18)
- Average time: ~1-2 minutes per file
- Common errors:
  - "Unbound variable" (variable scoping)
  - "MATCH after CREATE" (post-processing needs improvement)
  - Extraction failures (LLM returning text instead of code)

**Performance:**
- 10 files in ~12 minutes
- Estimated: ~1.8 hours for 100 files
- Memory usage: Stable at ~14-15 GB

## AI Contribution Notes

- Created comprehensive test import script with progress tracking
- Implemented Cypher extraction from various LLM response formats
- Designed post-processing error correction system
- Created improved prompts with syntax rules and examples
- Fixed ChromaDB collection management issue
- Generated comprehensive documentation for testing workflow
- Analyzed model trade-offs and provided recommendations

**Key capabilities demonstrated:**
- Pattern recognition for code extraction
- Error analysis and systematic fixing
- Prompt engineering with examples
- Performance analysis and optimization suggestions

## Human Contribution Notes

- Provided vault path and testing requirements
- Validated approach of selective file import
- Requested visibility into import process
- Guided focus on fixing syntax errors first
- Made decision to test with 100 files before full import
- Identified ChromaDB being tracked in git
- Validated that current solution is sufficient (no need for larger model yet)

**Strategic decisions:**
- Start with small batches (2 files) before scaling
- Focus on fixing infrastructure before model upgrades
- Prioritize post-processing over model changes (faster iteration)
- Test thoroughly before full vault import

## Future Considerations

### Immediate Improvements Needed
1. **Enhanced Post-Processing**
   - Better handling of variable scoping issues
   - More robust MATCH-after-CREATE detection
   - Fix for extraction failures (LLM returning explanations)

2. **Prompt Refinement**
   - Add few-shot examples from actual successful imports
   - Include Memgraph-specific syntax notes
   - Add negative examples based on actual errors

3. **Error Handling**
   - Better error messages for debugging
   - Option to retry failed files
   - Save failed Cypher queries for analysis

### Longer Term
- Consider larger model (llama3.2:11b or 70b-q4) if semantic accuracy needs improvement
- Add validation layer that checks Cypher before execution
- Create feedback loop: learn from errors to improve prompts
- Consider two-stage generation (extract structure → generate Cypher)

### Testing Strategy
- Continue testing with larger batches (100 → 500 → 1000)
- Monitor success rate and error patterns
- Iterate on prompts based on real-world errors
- Document successful patterns for future reference

## Related Resources

- **Files Created:**
  - `scripts/test-vault-import.py`
  - `docs/vault-testing-guide.md`
  - `docs/improving-cypher-generation.md`
  - `packages/backend/core/knowledgebase/prompts/system_message_generate_improved`
  - `packages/backend/core/knowledgebase/prompts/prompt_generate_improved`

- **Files Modified:**
  - `packages/backend/core/knowledgebase/TextAnalizer.py` (extraction + post-processing)
  - `.gitignore` (ChromaDB exclusions)

- **Documentation:**
  - [Vault Testing Guide](../docs/vault-testing-guide.md)
  - [Improving Cypher Generation](../docs/improving-cypher-generation.md)
  - [Memgraph Lab Guide](../docs/memgraph-lab-guide.md)

- **External Resources:**
  - [Memgraph Cypher Documentation](https://memgraph.com/docs/cypher-manual)
  - [Ollama Model Library](https://ollama.com/library)

---

**Attribution:** This work represents a collaboration between jprowan providing testing requirements, validation, and strategic direction, and Claude Sonnet 4.5 via Cursor IDE assisting with implementation, prompt engineering, and documentation.

