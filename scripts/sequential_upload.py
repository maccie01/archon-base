#!/usr/bin/env python3
"""
Sequential knowledge base upload - uploads one file at a time with delays
to avoid overloading the server.

Usage: python3 sequential_upload.py
"""

import json
import sys
import time
from pathlib import Path
import requests

# Configuration
SERVER_URL = "https://archon.nexorithm.io"
KB_DIR = Path("/Users/janschubert/tools/archon/knowledgebase")
DELAY_BETWEEN_FILES = 2  # seconds
RESULTS_FILE = Path("sequential_upload_results.json")

def find_all_markdown_files():
    """Find ALL markdown files in knowledge base."""
    files = []
    for md_file in KB_DIR.rglob("*.md"):
        if ".backups" not in md_file.parts:
            files.append(md_file)
    return sorted(files)

def extract_tags(file_path):
    """Extract tags from file path."""
    parts = file_path.relative_to(KB_DIR).parts[:-1]
    tags = []
    for part in parts:
        tag = part.replace('_', ' ').replace('-', ' ').lower()
        tags.append(tag)
    return tags

def upload_file(file_path):
    """Upload single file and return result."""
    relative_path = str(file_path.relative_to(KB_DIR))
    tags = extract_tags(file_path)
    
    try:
        # Read file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Prepare multipart form data
        files = {
            'file': (file_path.name, file_content, 'text/markdown')
        }
        data = {
            'tags': json.dumps(tags),
            'knowledge_type': 'technical',
            'extract_code_examples': 'true'
        }
        
        # Upload
        response = requests.post(
            f"{SERVER_URL}/api/documents/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ {relative_path}")
            return {
                'success': True,
                'file': relative_path,
                'progress_id': result.get('progressId'),
                'tags': tags
            }
        else:
            print(f"✗ {relative_path}: HTTP {response.status_code}")
            return {
                'success': False,
                'file': relative_path,
                'error': f'HTTP {response.status_code}'
            }
            
    except Exception as e:
        print(f"✗ {relative_path}: {str(e)[:80]}")
        return {
            'success': False,
            'file': relative_path,
            'error': str(e)
        }

def main():
    print("=" * 80)
    print("SEQUENTIAL KNOWLEDGE BASE UPLOAD")
    print("=" * 80)
    print(f"Server: {SERVER_URL}")
    print(f"Source: {KB_DIR}")
    print()
    
    # Find all files
    print("Scanning for markdown files...")
    files = find_all_markdown_files()
    print(f"Found {len(files)} files")
    print()
    
    # Confirm
    response = input(f"Upload {len(files)} files sequentially? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled")
        return
    
    print()
    print("Starting upload (one file every 2 seconds)...")
    print()
    
    results = {'success': [], 'failed': []}
    
    for idx, file_path in enumerate(files, 1):
        print(f"[{idx}/{len(files)}] ", end='')
        result = upload_file(file_path)
        
        if result['success']:
            results['success'].append(result)
        else:
            results['failed'].append(result)
        
        # Delay between files (except last)
        if idx < len(files):
            time.sleep(DELAY_BETWEEN_FILES)
    
    # Summary
    print()
    print("=" * 80)
    print("UPLOAD COMPLETE")
    print("=" * 80)
    print(f"Total files: {len(files)}")
    print(f"Successful: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    print()
    
    if results['failed']:
        print("Failed files:")
        for item in results['failed']:
            print(f"  - {item['file']}: {item.get('error', 'Unknown')}")
        print()
    
    # Save results
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to: {RESULTS_FILE}")
    print()
    print(f"Note: {len(results['success'])} documents are being processed in the background.")
    print("Check progress in Archon UI → Progress → Active Operations")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUpload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
