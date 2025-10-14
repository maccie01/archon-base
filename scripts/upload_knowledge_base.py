"""
Batch upload knowledge base documents to Archon production server.

This script uploads all markdown files from the knowledgebase directory
to the production server via the /api/documents/upload endpoint.

Date: 2025-10-14
Server: archon.nexorithm.io

Usage:
    python upload_knowledge_base.py [--yes]

    --yes  Skip confirmation prompt and proceed with upload
"""

import argparse
import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List

import aiohttp

# Configuration
BASE_URL = "https://archon.nexorithm.io"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/documents/upload"
PROGRESS_ENDPOINT = f"{BASE_URL}/api/progress"
KNOWLEDGEBASE_DIR = Path("/Users/janschubert/tools/archon/knowledgebase")
BATCH_SIZE = 5  # Upload 5 files at a time
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("upload_knowledge_base.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def extract_tags_from_path(file_path: Path) -> List[str]:
    """Extract appropriate tags based on file path."""
    parts = file_path.relative_to(KNOWLEDGEBASE_DIR).parts
    tags = []

    # Add category-based tags
    if "global" in parts:
        tags.append("global")
        if "01-react-frontend" in parts:
            tags.extend(["react", "frontend"])
        elif "02-nodejs-backend" in parts:
            tags.extend(["nodejs", "backend"])
        elif "03-database-orm" in parts:
            tags.extend(["database", "orm"])
        elif "04-security-auth" in parts:
            tags.extend(["security", "authentication"])
        elif "05-testing-quality" in parts:
            tags.extend(["testing", "quality"])
        elif "06-configuration" in parts:
            tags.append("configuration")

    elif "projects" in parts:
        tags.append("project")
        if "netzwaechter_refactored" in parts:
            tags.append("netzwaechter")
            # Add sub-category tags
            if "01-database" in parts:
                tags.append("database")
            elif "02-api-endpoints" in parts:
                tags.extend(["api", "endpoints"])
            elif "03-authentication" in parts:
                tags.append("authentication")
            elif "04-frontend" in parts:
                tags.append("frontend")
            elif "05-backend" in parts:
                tags.append("backend")
            elif "06-configuration" in parts:
                tags.append("configuration")
            elif "07-standards" in parts:
                tags.append("standards")

    elif "knowledge-organization" in parts:
        tags.extend(["meta", "documentation"])

    return tags


def find_markdown_files() -> List[Path]:
    """Find all markdown files in knowledgebase (excluding backups)."""
    files = []
    for md_file in KNOWLEDGEBASE_DIR.rglob("*.md"):
        # Skip backup directories
        if ".backups" in md_file.parts:
            continue
        # Skip archive directories
        if "archive" in md_file.parts:
            continue
        files.append(md_file)

    return sorted(files)


async def upload_file(
    session: aiohttp.ClientSession, file_path: Path, attempt: int = 1
) -> Dict:
    """Upload a single file to the server."""
    tags = extract_tags_from_path(file_path)
    relative_path = file_path.relative_to(KNOWLEDGEBASE_DIR)

    try:
        # Read file content
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Prepare form data
        data = aiohttp.FormData()
        data.add_field(
            "file",
            file_content,
            filename=file_path.name,
            content_type="text/markdown",
        )
        data.add_field("tags", json.dumps(tags))
        data.add_field("knowledge_type", "technical")
        data.add_field("extract_code_examples", "true")

        # Upload file
        async with session.post(UPLOAD_ENDPOINT, data=data) as response:
            if response.status == 200:
                result = await response.json()
                logger.info(
                    f"✓ Uploaded: {relative_path} (progress_id: {result.get('progressId')})"
                )
                return {
                    "success": True,
                    "file": str(relative_path),
                    "progress_id": result.get("progressId"),
                    "tags": tags,
                }
            else:
                error_text = await response.text()
                logger.error(
                    f"✗ Failed to upload {relative_path}: HTTP {response.status} - {error_text}"
                )

                # Retry on server errors
                if response.status >= 500 and attempt < RETRY_ATTEMPTS:
                    logger.info(
                        f"  Retrying {relative_path} (attempt {attempt + 1}/{RETRY_ATTEMPTS})..."
                    )
                    await asyncio.sleep(RETRY_DELAY * attempt)
                    return await upload_file(session, file_path, attempt + 1)

                return {
                    "success": False,
                    "file": str(relative_path),
                    "error": f"HTTP {response.status}: {error_text}",
                }

    except Exception as e:
        logger.error(f"✗ Exception uploading {relative_path}: {str(e)}")

        # Retry on exceptions
        if attempt < RETRY_ATTEMPTS:
            logger.info(
                f"  Retrying {relative_path} (attempt {attempt + 1}/{RETRY_ATTEMPTS})..."
            )
            await asyncio.sleep(RETRY_DELAY * attempt)
            return await upload_file(session, file_path, attempt + 1)

        return {
            "success": False,
            "file": str(relative_path),
            "error": str(e),
        }


async def check_progress(session: aiohttp.ClientSession, progress_id: str) -> Dict:
    """Check the progress of a document upload."""
    try:
        async with session.get(f"{PROGRESS_ENDPOINT}/{progress_id}") as response:
            if response.status == 200:
                return await response.json()
            return {"status": "unknown", "error": f"HTTP {response.status}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def upload_batch(
    session: aiohttp.ClientSession, files: List[Path]
) -> List[Dict]:
    """Upload a batch of files concurrently."""
    tasks = [upload_file(session, file_path) for file_path in files]
    return await asyncio.gather(*tasks)


async def main(skip_confirmation: bool = False):
    """Main upload process."""
    logger.info("=" * 80)
    logger.info("ARCHON KNOWLEDGE BASE BATCH UPLOAD")
    logger.info("=" * 80)
    logger.info(f"Server: {BASE_URL}")
    logger.info(f"Source: {KNOWLEDGEBASE_DIR}")
    logger.info("")

    # Find all markdown files
    logger.info("Scanning for markdown files...")
    files = find_markdown_files()
    logger.info(f"Found {len(files)} files to upload")
    logger.info("")

    # Calculate total size
    total_size = sum(f.stat().st_size for f in files)
    logger.info(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    logger.info("")

    # Confirm before starting
    if not skip_confirmation:
        try:
            response = input("Proceed with upload? (yes/no): ")
            if response.lower() != "yes":
                logger.info("Upload cancelled by user")
                return
        except EOFError:
            logger.error("Cannot read from stdin. Use --yes flag to skip confirmation.")
            sys.exit(1)
    else:
        logger.info("Skipping confirmation (--yes flag provided)")

    logger.info("")
    logger.info("Starting upload...")
    logger.info("")

    start_time = time.time()
    results = {
        "success": [],
        "failed": [],
        "progress_ids": [],
    }

    # Upload in batches
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(files), BATCH_SIZE):
            batch = files[i : i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(files) + BATCH_SIZE - 1) // BATCH_SIZE

            logger.info(f"Batch {batch_num}/{total_batches} ({len(batch)} files):")

            batch_results = await upload_batch(session, batch)

            for result in batch_results:
                if result["success"]:
                    results["success"].append(result)
                    if result.get("progress_id"):
                        results["progress_ids"].append(result["progress_id"])
                else:
                    results["failed"].append(result)

            # Brief pause between batches
            if i + BATCH_SIZE < len(files):
                await asyncio.sleep(1)

    # Summary
    elapsed = time.time() - start_time
    logger.info("")
    logger.info("=" * 80)
    logger.info("UPLOAD SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total files: {len(files)}")
    logger.info(f"Successful: {len(results['success'])}")
    logger.info(f"Failed: {len(results['failed'])}")
    logger.info(f"Time elapsed: {elapsed:.2f} seconds")
    logger.info("")

    if results["failed"]:
        logger.info("Failed files:")
        for result in results["failed"]:
            logger.info(f"  - {result['file']}: {result.get('error', 'Unknown error')}")
        logger.info("")

    # Save results to file
    results_file = Path("upload_results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Detailed results saved to: {results_file}")

    logger.info("")
    logger.info(
        f"Note: {len(results['progress_ids'])} documents are being processed asynchronously."
    )
    logger.info(
        "You can check their status in the Archon UI under Progress → Active Operations"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload knowledge base files to Archon server"
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt and proceed with upload",
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(skip_confirmation=args.yes))
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Upload interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)
