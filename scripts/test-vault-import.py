#!/usr/bin/env python3
"""
Test Vault Import Script

Loads the 100 most recently modified files from your Obsidian vault
and processes them through the same pipeline as the plugin would.

This allows you to:
- Test the default behavior before running on full vault
- See what data model is created
- Review in Memgraph Lab
- Iterate on prompts before full import

Prerequisites:
    1. Backend must be running (./scripts/start-dev.sh)
    2. Must be run in conda environment: conda activate odin_backend

Usage:
    conda activate odin_backend
    python scripts/test-vault-import.py /path/to/your/vault [--clear-db]

Options:
    --clear-db    Clear existing database before importing (optional)
    --limit N     Import N files instead of 100 (default: 100)
    --verbose     Enable verbose logging (shows Cypher queries)
"""

import sys
import os
import argparse
import logging
import time
from pathlib import Path
from typing import List, Tuple
from datetime import datetime

# Add backend to Python path
backend_path = Path(__file__).parent.parent / "packages" / "backend"
sys.path.insert(0, str(backend_path))

from core.knowledgebase.notes.VaultManager import VaultManager
from core.knowledgebase.MemgraphManager import MemgraphManager
from core.knowledgebase.Utils import Utils
from core.knowledgebase import constants

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def get_recent_files(vault_path: str, limit: int = 100, file_extensions: Tuple[str, ...] = ('.md', '.txt')) -> List[str]:
    """
    Get the N most recently modified files from the vault.
    
    Args:
        vault_path: Path to the Obsidian vault
        limit: Maximum number of files to return
        file_extensions: File extensions to include
        
    Returns:
        List of file paths sorted by modification time (newest first)
    """
    vault = Path(vault_path)
    if not vault.exists():
        raise ValueError(f"Vault path does not exist: {vault_path}")
    
    logger.info(f"Scanning vault: {vault_path}")
    
    all_files = []
    for file_path in vault.rglob('*'):
        # Skip hidden directories and files
        if any(part.startswith('.') for part in file_path.parts):
            continue
            
        # Skip Obsidian system directories
        if '.obsidian' in file_path.parts:
            continue
            
        # Only include markdown and text files
        if file_path.is_file() and file_path.suffix.lower() in file_extensions:
            try:
                mtime = file_path.stat().st_mtime
                all_files.append((mtime, str(file_path)))
            except (OSError, PermissionError) as e:
                logger.warning(f"Could not access {file_path}: {e}")
                continue
    
    # Sort by modification time (newest first)
    all_files.sort(key=lambda x: x[0], reverse=True)
    
    # Return just the file paths
    selected_files = [path for _, path in all_files[:limit]]
    
    logger.info(f"Found {len(all_files)} total files, selected {len(selected_files)} most recent")
    
    return selected_files


def format_time(seconds: float) -> str:
    """Format seconds into human-readable time."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def print_file_summary(files: List[str], vault_path: str):
    """Print a summary of the files to be imported."""
    logger.info("\n" + "="*70)
    logger.info("FILES TO IMPORT (most recent first)")
    logger.info("="*70)
    
    vault = Path(vault_path)
    for i, file_path in enumerate(files[:20], 1):  # Show first 20
        try:
            rel_path = Path(file_path).relative_to(vault)
            mtime = datetime.fromtimestamp(Path(file_path).stat().st_mtime)
            size = Path(file_path).stat().st_size
            logger.info(f"  {i:3d}. {rel_path} ({mtime.strftime('%Y-%m-%d %H:%M')}, {size:,} bytes)")
        except Exception as e:
            logger.warning(f"  {i:3d}. {file_path} (error: {e})")
    
    if len(files) > 20:
        logger.info(f"  ... and {len(files) - 20} more files")
    
    logger.info("="*70 + "\n")


def import_vault_files(vault_path: str, file_paths: List[str], clear_db: bool = False) -> dict:
    """
    Import files using the same process as VaultManager.populate_vault()
    but with only the selected files.
    
    Returns:
        Dictionary with statistics about the import
    """
    stats = {
        'files_processed': 0,
        'files_failed': 0,
        'total_time': 0,
        'cypher_time': 0,
        'db_time': 0,
        'embedding_time': 0,
        'errors': []
    }
    
    start_time = time.time()
    
    # Initialize managers
    vm = VaultManager(vault_path)
    mm = MemgraphManager()
    cm = vm.cm  # Get CollectionManager from VaultManager
    
    # Clear database if requested
    if clear_db:
        logger.info("Clearing existing database...")
        mm.delete_all()
        cm.delete_all()
        # Recreate collection after delete_all() resets ChromaDB
        cm._make_collection(cm.collection_name)
        logger.info("✓ Database cleared")
    
    # Check if database is empty to determine which prompt to use
    is_empty = mm.check_if_db_empty()
    logger.info(f"Database empty: {is_empty}")
    
    logger.info(f"\nStarting import of {len(file_paths)} files...")
    logger.info("="*70)
    
    # Process each file
    for i, file_path in enumerate(file_paths, 1):
        file_start = time.time()
        
        try:
            rel_path = Path(file_path).relative_to(Path(vault_path))
            logger.info(f"[{i}/{len(file_paths)}] Processing: {rel_path}")
            
            # Read file content
            file_text = Path(file_path).read_text(encoding='utf-8')
            file_size = len(file_text)
            logger.info(f"  File size: {file_size:,} characters")
            
            # Generate Cypher queries
            cypher_start = time.time()
            if i == 1 and is_empty:
                logger.info("  Using CREATE prompt (first file, empty DB)")
                res_queries = vm.ta.text_to_cypher_create(
                    file_text, vault_path, file_path
                )
            else:
                logger.info("  Using UPDATE prompt (integrating with existing data)")
                # Export current data for context
                data = mm.export_data_for_repo_path(vault_path)
                res_queries = vm.ta.data_and_text_to_cypher_update(
                    str(data), file_text, vault_path, file_path
                )
            
            cypher_time = time.time() - cypher_start
            stats['cypher_time'] += cypher_time
            logger.info(f"  Generated Cypher in {format_time(cypher_time)}")
            
            # Log Cypher preview (first 500 chars)
            cypher_preview = res_queries[:500].replace('\n', ' ')
            logger.debug(f"  Cypher preview: {cypher_preview}...")
            
            # Execute Cypher query
            db_start = time.time()
            mm.run_update_query(res_queries)
            db_time = time.time() - db_start
            stats['db_time'] += db_time
            logger.info(f"  Executed in Memgraph ({format_time(db_time)})")
            
            # Add to ChromaDB collection
            cm.add_file(file_path)
            logger.info("  Added to ChromaDB collection")
            
            file_time = time.time() - file_start
            logger.info(f"  ✓ Completed in {format_time(file_time)}")
            stats['files_processed'] += 1
            
        except Exception as e:
            stats['files_failed'] += 1
            stats['errors'].append({
                'file': file_path,
                'error': str(e)
            })
            logger.error(f"  ✗ Failed: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        # Progress update every 10 files
        if i % 10 == 0:
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = (len(file_paths) - i) * avg_time
            logger.info(f"\n  Progress: {i}/{len(file_paths)} files ({i*100//len(file_paths)}%)")
            logger.info(f"  Estimated time remaining: {format_time(remaining)}\n")
    
    # Update embeddings for all processed files
    logger.info("\n" + "="*70)
    logger.info("UPDATING EMBEDDINGS")
    logger.info("="*70)
    
    embedding_start = time.time()
    for i, file_path in enumerate(file_paths, 1):
        try:
            rel_path = Path(file_path).relative_to(Path(vault_path))
            logger.info(f"[{i}/{len(file_paths)}] Embedding: {rel_path}")
            mm.update_embeddings(file_path)
            logger.info(f"  ✓ Completed")
        except Exception as e:
            logger.error(f"  ✗ Failed: {e}")
            stats['errors'].append({
                'file': file_path,
                'error': f"Embedding: {str(e)}"
            })
    
    stats['embedding_time'] = time.time() - embedding_start
    stats['total_time'] = time.time() - start_time
    
    return stats


def print_statistics(stats: dict, file_count: int):
    """Print import statistics."""
    logger.info("\n" + "="*70)
    logger.info("IMPORT STATISTICS")
    logger.info("="*70)
    
    logger.info(f"Files processed: {stats['files_processed']}/{file_count}")
    logger.info(f"Files failed: {stats['files_failed']}")
    logger.info(f"\nTiming:")
    logger.info(f"  Total time: {format_time(stats['total_time'])}")
    logger.info(f"  Cypher generation: {format_time(stats['cypher_time'])} ({stats['cypher_time']/stats['total_time']*100:.1f}%)")
    logger.info(f"  Database execution: {format_time(stats['db_time'])} ({stats['db_time']/stats['total_time']*100:.1f}%)")
    logger.info(f"  Embedding generation: {format_time(stats['embedding_time'])} ({stats['embedding_time']/stats['total_time']*100:.1f}%)")
    
    if stats['files_processed'] > 0:
        avg_time = stats['total_time'] / stats['files_processed']
        logger.info(f"\nAverage time per file: {format_time(avg_time)}")
    
    if stats['errors']:
        logger.warning(f"\nErrors encountered: {len(stats['errors'])}")
        for error in stats['errors'][:5]:  # Show first 5 errors
            logger.warning(f"  - {Path(error['file']).name}: {error['error']}")
        if len(stats['errors']) > 5:
            logger.warning(f"  ... and {len(stats['errors']) - 5} more errors")
    
    logger.info("="*70)


def query_database_stats(vault_path: str):
    """Query and display database statistics."""
    logger.info("\n" + "="*70)
    logger.info("DATABASE STATISTICS")
    logger.info("="*70)
    
    mm = MemgraphManager()
    
    try:
        # Total nodes
        query = "MATCH (n) RETURN count(n) as node_count"
        result = list(mm.run_select_query(query))
        node_count = result[0]['node_count'] if result else 0
        logger.info(f"Total nodes: {node_count:,}")
        
        # Node types
        query = """
        MATCH (n)
        UNWIND labels(n) as label
        RETURN label, count(*) as count
        ORDER BY count DESC
        """
        results = list(mm.run_select_query(query))
        if results:
            logger.info("\nNode types:")
            for r in results:
                logger.info(f"  {r['label']}: {r['count']:,}")
        
        # Relationship types
        query = """
        MATCH ()-[r]->()
        RETURN DISTINCT type(r) as rel_type, count(*) as count
        ORDER BY count DESC
        """
        results = list(mm.run_select_query(query))
        if results:
            logger.info("\nRelationship types:")
            for r in results:
                logger.info(f"  {r['rel_type']}: {r['count']:,}")
        
        # Files represented
        query = """
        MATCH (n)
        WHERE n.file_path IS NOT NULL
        RETURN DISTINCT n.file_path as file_path
        """
        results = list(mm.run_select_query(query))
        logger.info(f"\nFiles represented in graph: {len(results)}")
        
    except Exception as e:
        logger.error(f"Error querying database: {e}")
    
    logger.info("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Import most recent vault files for testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import 100 most recent files
  python scripts/test-vault-import.py /path/to/vault
  
  # Import 50 files and clear database first
  python scripts/test-vault-import.py /path/to/vault --clear-db --limit 50
  
  # Import with verbose logging
  python scripts/test-vault-import.py /path/to/vault --verbose
        """
    )
    
    parser.add_argument(
        'vault_path',
        help='Path to your Obsidian vault'
    )
    
    parser.add_argument(
        '--clear-db',
        action='store_true',
        help='Clear existing database before importing'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Number of files to import (default: 100)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging (shows Cypher queries)'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate vault path
    vault_path = os.path.abspath(args.vault_path)
    if not os.path.exists(vault_path):
        logger.error(f"Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    logger.info("="*70)
    logger.info("ODIN VAULT TEST IMPORT")
    logger.info("="*70)
    logger.info(f"Vault path: {vault_path}")
    logger.info(f"File limit: {args.limit}")
    logger.info(f"Clear DB: {args.clear_db}")
    logger.info("="*70 + "\n")
    
    try:
        # Get recent files
        files = get_recent_files(vault_path, limit=args.limit)
        
        if not files:
            logger.error("No files found to import!")
            sys.exit(1)
        
        # Show summary
        print_file_summary(files, vault_path)
        
        # Confirm before proceeding
        if not args.clear_db:
            response = input("Proceed with import? (yes/no): ").lower().strip()
            if response != 'yes':
                logger.info("Import cancelled.")
                sys.exit(0)
        
        # Import files
        stats = import_vault_files(vault_path, files, clear_db=args.clear_db)
        
        # Print statistics
        print_statistics(stats, len(files))
        
        # Query database statistics
        query_database_stats(vault_path)
        
        logger.info("\n" + "="*70)
        logger.info("✓ IMPORT COMPLETE")
        logger.info("="*70)
        logger.info("\nNext steps:")
        logger.info("  1. Open Memgraph Lab: http://localhost:3000")
        logger.info("  2. Review the graph structure")
        logger.info("  3. Check if the data model matches your expectations")
        logger.info("  4. Iterate on prompts if needed")
        logger.info("  5. Run again with --clear-db to test changes")
        logger.info("="*70 + "\n")
        
    except KeyboardInterrupt:
        logger.info("\n\nImport interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nFatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()

