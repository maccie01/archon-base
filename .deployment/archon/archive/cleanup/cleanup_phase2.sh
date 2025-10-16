#!/bin/bash

# Phase 2 Cleanup: Delete Exact Duplicates
# Date: 2025-10-15
# Server: 91.98.156.158:8181

API_KEY="ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
BASE_URL="http://91.98.156.158:8181/api/knowledge-items"

# Report file
REPORT_FILE="CLEANUP_PHASE2_REPORT.md"

# Initialize report
cat > "$REPORT_FILE" << 'REPORT_HEADER'
# Phase 2 Cleanup Report: Exact Duplicate Deletion

Date: 2025-10-15
Server: 91.98.156.158:8181
API Endpoint: /api/knowledge-items

## Executive Summary

This report documents the deletion of exact duplicate knowledge items identified in the knowledge base audit.

## Deletion Strategy

For each duplicate pair:
1. Keep the most recent version (or properly tagged version)
2. Delete the older/untagged duplicate
3. Verify deletion with API
4. Log success/failure

## Deletion Results

REPORT_HEADER

# Counter for successes and failures
SUCCESS_COUNT=0
FAILURE_COUNT=0
TOTAL_ATTEMPTS=0

# Function to delete a knowledge item
delete_item() {
    local item_id="$1"
    local item_name="$2"
    local reason="$3"
    
    TOTAL_ATTEMPTS=$((TOTAL_ATTEMPTS + 1))
    
    echo "" >> "$REPORT_FILE"
    echo "### $TOTAL_ATTEMPTS. $item_name" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "- **ID**: \`$item_id\`" >> "$REPORT_FILE"
    echo "- **Reason**: $reason" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    # Attempt deletion
    echo "Deleting: $item_name ($item_id)..."
    RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE \
        -H "Authorization: Bearer $API_KEY" \
        "$BASE_URL/$item_id" 2>&1)
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "204" ]; then
        echo "  ✓ SUCCESS"
        echo "**Status**: SUCCESS (HTTP $HTTP_CODE)" >> "$REPORT_FILE"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "  ✗ FAILED (HTTP $HTTP_CODE)"
        echo "**Status**: FAILED (HTTP $HTTP_CODE)" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "**Error Response**:" >> "$REPORT_FILE"
        echo "\`\`\`" >> "$REPORT_FILE"
        echo "$BODY" >> "$REPORT_FILE"
        echo "\`\`\`" >> "$REPORT_FILE"
        FAILURE_COUNT=$((FAILURE_COUNT + 1))
    fi
    
    # Small delay between requests
    sleep 0.5
}

# Start deletions
echo "Starting Phase 2 cleanup: Exact Duplicate Deletion"
echo "Report will be saved to: $REPORT_FILE"
echo ""

# 1. ACCESSIBILITY.md - Delete older duplicate
delete_item "file_ACCESSIBILITY_md_c17ff256" "ACCESSIBILITY.md" "Older duplicate (created 2025-10-14), keeping newer version (2025-10-15)"

# 2. COMPONENT_PATTERNS.md - Delete one of same-day duplicates
delete_item "file_COMPONENT_PATTERNS_md_383cef4c" "COMPONENT_PATTERNS.md" "Duplicate with identical tags (global, 01 react frontend)"

# 3. TYPESCRIPT_REACT.md - Delete one of same-day duplicates
delete_item "file_TYPESCRIPT_REACT_md_b9ce3f76" "TYPESCRIPT_REACT.md" "Duplicate with identical tags (global, 01 react frontend)"

# 4. VALIDATION.md - Delete duplicate
delete_item "file_VALIDATION_md_a516c64f" "VALIDATION.md" "Duplicate with identical tags (global, 02 nodejs backend)"

# 5. API_SECURITY.md - Delete duplicate
delete_item "file_API_SECURITY_md_5869634c" "API_SECURITY.md" "Duplicate with identical tags (global, 04 security auth)"

# 6. BACKEND_TESTING.md - Delete duplicate
delete_item "file_BACKEND_TESTING_md_7de5c725" "BACKEND_TESTING.md" "Duplicate with identical tags (global, 05 testing quality)"

# 7. MIGRATION_READY_REPORT.md - Delete older untagged duplicate
delete_item "file_MIGRATION_READY_REPORT_md_de6cd9a3" "MIGRATION_READY_REPORT.md" "Older untagged duplicate (created 2025-10-14)"

# 8. README.md - Delete first untagged orphan
delete_item "file_README_md_11eb7727" "README.md (untagged #1)" "Untagged orphan with no project association"

# 9. README.md - Delete second untagged orphan
delete_item "file_README_md_81ba5866" "README.md (untagged #2)" "Untagged orphan with no project association"

# Generate summary
echo "" >> "$REPORT_FILE"
echo "## Summary" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "- **Total deletion attempts**: $TOTAL_ATTEMPTS" >> "$REPORT_FILE"
echo "- **Successful deletions**: $SUCCESS_COUNT" >> "$REPORT_FILE"
echo "- **Failed deletions**: $FAILURE_COUNT" >> "$REPORT_FILE"
echo "- **Success rate**: $(awk "BEGIN {printf \"%.1f\", ($SUCCESS_COUNT/$TOTAL_ATTEMPTS)*100}")%" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $FAILURE_COUNT -eq 0 ]; then
    echo "## Conclusion" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "All exact duplicate knowledge items have been successfully deleted. The knowledge base is now cleaner with $SUCCESS_COUNT fewer duplicate items." >> "$REPORT_FILE"
else
    echo "## Issues Encountered" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "$FAILURE_COUNT deletion(s) failed. Review the error responses above and retry manually if necessary." >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "## Next Steps" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "1. Review this report for any failed deletions" >> "$REPORT_FILE"
echo "2. Verify remaining knowledge items with: \`curl -H 'Authorization: Bearer ak_...' http://91.98.156.158:8181/api/knowledge-items | jq '.[] | {id, title, tags}'\`" >> "$REPORT_FILE"
echo "3. Proceed to Phase 3: Review cross-domain duplicates (ANTIPATTERNS.md, etc.)" >> "$REPORT_FILE"
echo "4. Consider addressing README.md duplicates with domain-specific content" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "Report completed: $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "Script: cleanup_phase2.sh" >> "$REPORT_FILE"

echo ""
echo "=================================================="
echo "Cleanup Complete!"
echo "=================================================="
echo "Total attempts: $TOTAL_ATTEMPTS"
echo "Successful: $SUCCESS_COUNT"
echo "Failed: $FAILURE_COUNT"
echo ""
echo "Full report saved to: $REPORT_FILE"
