#!/bin/bash

# Archon Knowledge Base Cleanup Script
# Generated from audit performed on 2025-10-15
#
# IMPORTANT: Review each command before execution
# This script provides the commands needed but requires manual execution

set -e

API_KEY="ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
BASE_URL="http://localhost:8181/api"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=============================================================="
echo "Archon Knowledge Base Cleanup Script"
echo "=============================================================="
echo ""
echo "This script will guide you through cleaning up the Archon KB"
echo "Execute each phase carefully and verify results"
echo ""

# Phase 1: Delete Duplicate Project
echo -e "${YELLOW}=== PHASE 1: Delete Duplicate Project ===${NC}"
echo ""
echo "Current duplicate projects:"
echo "  1. 3ff9cfb0-fbe2-4bf9-b176-9b0599bd7796 (Netzwaechter - ASCII) - TO DELETE"
echo "  2. 6d49dbb3-42d6-45f3-89b0-fdbc5d55d1eb (Netzwächter - Unicode) - TO KEEP"
echo ""
echo "Command to delete duplicate project:"
echo ""
echo "curl -X DELETE -H 'Authorization: Bearer ${API_KEY}' \\"
echo "  ${BASE_URL}/projects/3ff9cfb0-fbe2-4bf9-b176-9b0599bd7796"
echo ""
read -p "Execute Phase 1? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -X DELETE -H "Authorization: Bearer ${API_KEY}" \
      "${BASE_URL}/projects/3ff9cfb0-fbe2-4bf9-b176-9b0599bd7796"
    echo ""
    echo -e "${GREEN}Phase 1 complete!${NC}"
    echo ""
    echo "Verify deletion:"
    curl -s -H "Authorization: Bearer ${API_KEY}" \
      "${BASE_URL}/projects" | grep -o '"id":"[^"]*","title":"[^"]*"' || echo "No projects found"
    echo ""
fi

# Phase 2: Get All Netzwächter Knowledge Items
echo -e "${YELLOW}=== PHASE 2: Link Knowledge Items to Project ===${NC}"
echo ""
echo "This phase requires fetching all Netzwächter-related knowledge items"
echo "and linking them to project: 6d49dbb3-42d6-45f3-89b0-fdbc5d55d1eb"
echo ""
echo "Step 1: Get all knowledge items (this may take a moment)..."
echo ""

KEPT_PROJECT_ID="6d49dbb3-42d6-45f3-89b0-fdbc5d55d1eb"

read -p "Fetch Netzwächter knowledge items? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Create temporary file to store knowledge item IDs
    TEMP_FILE="/tmp/netzwaechter_items.json"

    echo "Fetching page 1..."
    curl -s -H "Authorization: Bearer ${API_KEY}" \
      "${BASE_URL}/knowledge-items?page=1&per_page=100" > "${TEMP_FILE}.p1"

    echo "Fetching page 2..."
    curl -s -H "Authorization: Bearer ${API_KEY}" \
      "${BASE_URL}/knowledge-items?page=2&per_page=100" > "${TEMP_FILE}.p2"

    echo ""
    echo "Extracting Netzwächter-related items..."

    # Extract items with "netzwaechter refactored" or "projects" tags
    # This is a manual process - you'll need to inspect the JSON
    echo ""
    echo -e "${YELLOW}NOTE: Automatic linking requires custom implementation${NC}"
    echo "The API may not support bulk project association."
    echo "You may need to:"
    echo "  1. Review knowledge items in the UI"
    echo "  2. Manually associate them with the project"
    echo "  3. OR use the Archon CLI if available"
    echo ""
    echo "Files saved to:"
    echo "  - ${TEMP_FILE}.p1"
    echo "  - ${TEMP_FILE}.p2"
    echo ""
fi

# Phase 3: Delete Duplicate Knowledge Items
echo -e "${YELLOW}=== PHASE 3: Delete Duplicate Knowledge Items ===${NC}"
echo ""
echo "Priority duplicates to delete (by ID):"
echo ""
echo "1. EXACT DUPLICATES (same content, different ingestion times):"
echo ""

# Accessibility - keep newer one
echo "   ACCESSIBILITY.md:"
echo "   DELETE: file_ACCESSIBILITY_md_c17ff256 (2025-10-14)"
echo "   KEEP:   file_ACCESSIBILITY_md_b49cf4f1 (2025-10-15)"
echo ""
echo "   curl -X DELETE -H 'Authorization: Bearer ${API_KEY}' \\"
echo "     ${BASE_URL}/knowledge-items/file_ACCESSIBILITY_md_c17ff256"
echo ""

# Component Patterns - both same date, pick one
echo "   COMPONENT_PATTERNS.md:"
echo "   DELETE: file_COMPONENT_PATTERNS_md_b35f28a5"
echo "   KEEP:   file_COMPONENT_PATTERNS_md_383cef4c"
echo ""
echo "   curl -X DELETE -H 'Authorization: Bearer ${API_KEY}' \\"
echo "     ${BASE_URL}/knowledge-items/file_COMPONENT_PATTERNS_md_b35f28a5"
echo ""

# TypeScript React - both same date
echo "   TYPESCRIPT_REACT.md:"
echo "   DELETE: file_TYPESCRIPT_REACT_md_b9ce3f76"
echo "   KEEP:   (first instance from page 1)"
echo ""

# API Security
echo "   API_SECURITY.md:"
echo "   DELETE: (one instance - check IDs in JSON)"
echo ""

# Backend Testing
echo "   BACKEND_TESTING.md:"
echo "   DELETE: (one instance - check IDs in JSON)"
echo ""

# Validation
echo "   VALIDATION.md:"
echo "   DELETE: (one instance - check IDs in JSON)"
echo ""

echo "2. UNTAGGED ITEMS TO DELETE:"
echo ""
echo "   MIGRATION_READY_REPORT.md (older):"
echo "   DELETE: file_MIGRATION_READY_REPORT_md_de6cd9a3 (2025-10-14)"
echo "   KEEP:   file_MIGRATION_READY_REPORT_md_abeb052b (2025-10-15)"
echo ""
echo "   curl -X DELETE -H 'Authorization: Bearer ${API_KEY}' \\"
echo "     ${BASE_URL}/knowledge-items/file_MIGRATION_READY_REPORT_md_de6cd9a3"
echo ""

echo "3. README.md DUPLICATES:"
echo "   Review the 17 README instances and delete:"
echo "   - Untagged/orphaned versions (2 instances)"
echo "   - Keep project-specific versions"
echo "   - Keep one global version per topic area"
echo ""

read -p "Display delete commands for exact duplicates? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cat << 'EOF'

# Delete exact duplicates (execute one by one, verify each):

curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_ACCESSIBILITY_md_c17ff256

curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_COMPONENT_PATTERNS_md_b35f28a5

curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_MIGRATION_READY_REPORT_md_de6cd9a3

# IMPORTANT: For README.md duplicates, manually review in the UI first
# to ensure you're keeping the right versions

EOF
fi

# Phase 4: Fix Tagging
echo ""
echo -e "${YELLOW}=== PHASE 4: Fix Tagging Issues ===${NC}"
echo ""
echo "Items that need retagging:"
echo ""
echo "1. NETZWAECHTER_PATTERNS_ANALYSIS.md"
echo "   Current tags: global, 02 nodejs backend"
echo "   Should be: projects, netzwaechter refactored, 02 nodejs backend"
echo ""
echo "2. Untagged items (5 total):"
echo "   - 2x README.md (need to identify topic area)"
echo "   - MIGRATION_READY_REPORT.md (after deleting duplicate)"
echo "     Suggested tags: knowledge organization, archive"
echo ""
echo "Tagging requires PATCH requests to update metadata."
echo "Check API documentation for exact endpoint and payload format."
echo ""

# Summary
echo ""
echo "=============================================================="
echo -e "${GREEN}Cleanup Script Summary${NC}"
echo "=============================================================="
echo ""
echo "Phase 1: Delete duplicate project"
echo "  Status: Ready to execute"
echo ""
echo "Phase 2: Link knowledge items to project"
echo "  Status: Requires manual implementation or CLI tool"
echo ""
echo "Phase 3: Delete duplicate knowledge items"
echo "  Status: Commands provided, execute carefully"
echo "  Impact: ~8-10 duplicates for immediate deletion"
echo ""
echo "Phase 4: Fix tagging issues"
echo "  Status: Requires PATCH API calls (manual or scripted)"
echo "  Impact: ~5-10 items need retagging"
echo ""
echo "RECOMMENDATIONS:"
echo "  1. Execute Phase 1 first (delete duplicate project)"
echo "  2. Take a backup before Phase 3 if possible"
echo "  3. Execute deletions one at a time with verification"
echo "  4. Document any issues encountered"
echo "  5. Run audit again after cleanup to verify"
echo ""
echo "For detailed analysis, see: KNOWLEDGE_BASE_AUDIT.md"
echo "=============================================================="
echo ""
