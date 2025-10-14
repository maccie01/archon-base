"""
Retry uploading failed knowledge base documents.

This script reads the upload_results.json and retries only the failed files.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path

import aiohttp

# Configuration
BASE_URL = "https://archon.nexorithm.io"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/documents/upload"
KNOWLEDGEBASE_DIR = Path("/Users/janschubert/tools/archon/knowledgebase")
DELAY_BETWEEN_UPLOADS = 3  # seconds - slower to avoid overwhelming server

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("retry_failed_uploads.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def extract_tags_from_path(file_path: Path):
    """Extract appropriate tags based on file path."""
    parts = file_path.relative_to(KNOWLEDGEBASE_DIR).parts
    tags = []

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


async def upload_file(session: aiohttp.ClientSession, file_path: Path):
    """Upload a single file to the server."""
    tags = extract_tags_from_path(file_path)
    relative_path = file_path.relative_to(KNOWLEDGEBASE_DIR)

    try:
        with open(file_path, "rb") as f:
            file_content = f.read()

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
                }
            else:
                error_text = await response.text()
                logger.error(
                    f"✗ Failed to upload {relative_path}: HTTP {response.status}"
                )
                return {
                    "success": False,
                    "file": str(relative_path),
                    "error": f"HTTP {response.status}",
                }

    except Exception as e:
        logger.error(f"✗ Exception uploading {relative_path}: {str(e)}")
        return {
            "success": False,
            "file": str(relative_path),
            "error": str(e),
        }


async def main():
    """Main retry process."""
    logger.info("=" * 80)
    logger.info("RETRY FAILED UPLOADS")
    logger.info("=" * 80)

    # Load failed files from previous upload
    try:
        with open("upload_results.json", "r") as f:
            previous_results = json.load(f)
            failed_files = [item["file"] for item in previous_results["failed"]]
    except FileNotFoundError:
        logger.error("upload_results.json not found. Run main upload first.")
        return

    logger.info(f"Found {len(failed_files)} failed files to retry")
    logger.info("")

    start_time = time.time()
    results = {
        "success": [],
        "failed": [],
        "progress_ids": [],
    }

    async with aiohttp.ClientSession() as session:
        for i, file_path_str in enumerate(failed_files, 1):
            file_path = KNOWLEDGEBASE_DIR / file_path_str
            logger.info(f"[{i}/{len(failed_files)}] Uploading: {file_path_str}")

            result = await upload_file(session, file_path)

            if result["success"]:
                results["success"].append(result)
                if result.get("progress_id"):
                    results["progress_ids"].append(result["progress_id"])
            else:
                results["failed"].append(result)

            # Delay between uploads to avoid overwhelming server
            if i < len(failed_files):
                await asyncio.sleep(DELAY_BETWEEN_UPLOADS)

    # Summary
    elapsed = time.time() - start_time
    logger.info("")
    logger.info("=" * 80)
    logger.info("RETRY SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total retried: {len(failed_files)}")
    logger.info(f"Successful: {len(results['success'])}")
    logger.info(f"Failed: {len(results['failed'])}")
    logger.info(f"Time elapsed: {elapsed:.2f} seconds")
    logger.info("")

    if results["failed"]:
        logger.info("Still failed:")
        for result in results["failed"]:
            logger.info(f"  - {result['file']}: {result.get('error', 'Unknown error')}")
        logger.info("")

    # Save results
    results_file = Path("retry_results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to: {results_file}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Retry interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)
