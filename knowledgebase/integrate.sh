#!/bin/bash
# Knowledge Base Integration Script
# Created: 2025-10-14
# Purpose: Automate integration of research results into global knowledge base

set -e  # Exit on error
set -u  # Exit on undefined variable

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base paths
KB_ROOT="/Users/janschubert/tools/archon/knowledgebase"
RESULTS_DIR="${KB_ROOT}/research_prompts.md/results"
GLOBAL_DIR="${KB_ROOT}/global"
BACKUP_DIR="${KB_ROOT}/backups"

# Logging
LOG_FILE="${KB_ROOT}/integration_$(date +%Y%m%d_%H%M%S).log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

# Phase 1: Pre-Integration Preparation
phase_1_backup() {
    log "=== Phase 1: Creating Backup ==="

    mkdir -p "$BACKUP_DIR"

    BACKUP_FILE="${BACKUP_DIR}/backup_$(date +%Y%m%d_%H%M%S).tar.gz"

    log "Creating backup: $BACKUP_FILE"
    cd "$KB_ROOT"
    tar -czf "$BACKUP_FILE" global/

    if [ -f "$BACKUP_FILE" ]; then
        BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        success "Backup created: $BACKUP_FILE (${BACKUP_SIZE})"
    else
        error "Backup creation failed"
    fi
}

# Phase 2: Security Domain Integration
phase_2_security() {
    log "=== Phase 2: Security Domain Integration ==="

    local security_files=(
        "01_JWT_PATTERNS.md:JWT_PATTERNS.md"
        "02_CORS_CONFIGURATION.md:CORS_CONFIGURATION.md"
        "03_RATE_LIMITING.md:RATE_LIMITING.md"
        "04_CSRF_PROTECTION.md:CSRF_PROTECTION.md"
        "05_XSS_PREVENTION.md:XSS_PREVENTION.md"
        "06_SQL_INJECTION_PREVENTION.md:SQL_INJECTION_PREVENTION.md"
        "07_INPUT_VALIDATION.md:INPUT_VALIDATION.md"
        "08_SECURITY_HEADERS.md:SECURITY_HEADERS.md"
        "09_API_SECURITY.md:API_SECURITY.md"
        "10_SECRETS_MANAGEMENT.md:SECRETS_MANAGEMENT.md"
        "11_SSL_TLS.md:SSL_TLS.md"
        "12_SECURITY_TESTING.md:SECURITY_TESTING.md"
        "13_OAUTH2_OPENID.md:OAUTH2_OPENID.md"
        "14_MFA_PATTERNS.md:MFA_PATTERNS.md"
    )

    local count=0
    for file_mapping in "${security_files[@]}"; do
        IFS=':' read -r source target <<< "$file_mapping"

        SOURCE_PATH="${RESULTS_DIR}/security/${source}"
        TARGET_PATH="${GLOBAL_DIR}/04-security-auth/${target}"

        if [ ! -f "$SOURCE_PATH" ]; then
            warning "Source file not found: $SOURCE_PATH"
            continue
        fi

        # Check if target is empty
        if [ ! -s "$TARGET_PATH" ]; then
            log "Copying $source -> $target (target was empty)"
            cp "$SOURCE_PATH" "$TARGET_PATH"
            ((count++))
        else
            warning "Target $target already has content, skipping automatic copy"
        fi
    done

    success "Security domain: $count files integrated"
}

# Phase 3: Validate Security Integration
phase_3_validate_security() {
    log "=== Phase 3: Validating Security Integration ==="

    local issues=0

    # Check for HTML artifacts
    log "Checking for HTML artifacts..."
    if grep -l "<div\|<span\|<button" "${GLOBAL_DIR}/04-security-auth"/*.md 2>/dev/null; then
        warning "HTML artifacts found in security files (manual cleanup may be needed)"
        ((issues++))
    fi

    # Check for unclosed code blocks
    log "Checking for unclosed code blocks..."
    for f in "${GLOBAL_DIR}/04-security-auth"/*.md; do
        if [ -f "$f" ]; then
            count=$(grep -c '```' "$f" || echo "0")
            if [ $((count % 2)) -ne 0 ]; then
                warning "Unclosed code block in $(basename "$f")"
                ((issues++))
            fi
        fi
    done

    # Check that previously empty files now have content
    log "Checking file sizes..."
    local empty_count=0
    for f in "${GLOBAL_DIR}/04-security-auth"/{JWT_PATTERNS,CORS_CONFIGURATION,RATE_LIMITING,CSRF_PROTECTION,XSS_PREVENTION,SQL_INJECTION_PREVENTION,INPUT_VALIDATION,SECURITY_HEADERS,API_SECURITY,SECRETS_MANAGEMENT,SSL_TLS,SECURITY_TESTING,OAUTH2_OPENID,MFA_PATTERNS}.md; do
        if [ ! -s "$f" ]; then
            warning "File is still empty: $(basename "$f")"
            ((empty_count++))
            ((issues++))
        fi
    done

    if [ $issues -eq 0 ]; then
        success "Security validation passed"
    else
        warning "Security validation found $issues issues (see log for details)"
    fi
}

# Phase 4: Testing Domain Integration
phase_4_testing() {
    log "=== Phase 4: Testing Domain Integration ==="

    local testing_files=(
        "01_VITEST_PATTERNS.md:VITEST_PATTERNS.md"
        "02_E2E_TESTING.md:E2E_TESTING.md"
        "03_MOCKING_PATTERNS.md:MOCKING_PATTERNS.md"
    )

    local count=0
    for file_mapping in "${testing_files[@]}"; do
        IFS=':' read -r source target <<< "$file_mapping"

        SOURCE_PATH="${RESULTS_DIR}/testing/${source}"
        TARGET_PATH="${GLOBAL_DIR}/05-testing-quality/${target}"

        if [ ! -f "$SOURCE_PATH" ]; then
            warning "Source file not found: $SOURCE_PATH"
            continue
        fi

        # For testing, we'll create .backup and inform user
        if [ -f "$TARGET_PATH" ] && [ -s "$TARGET_PATH" ]; then
            log "Creating backup of $target before replacement"
            cp "$TARGET_PATH" "${TARGET_PATH}.backup"
        fi

        log "Copying $source -> $target"
        cp "$SOURCE_PATH" "$TARGET_PATH"
        ((count++))
    done

    success "Testing domain: $count files integrated"
}

# Phase 5: Generate Report
phase_5_report() {
    log "=== Phase 5: Generating Integration Report ==="

    REPORT_FILE="${KB_ROOT}/integration_report_$(date +%Y%m%d_%H%M%S).md"

    cat > "$REPORT_FILE" << EOF
# Integration Report

Generated: $(date)

## Summary

### Security Domain
- Files integrated: $(find "${GLOBAL_DIR}/04-security-auth" -name "*.md" -type f -size +1k | wc -l | tr -d ' ')
- Empty files remaining: $(find "${GLOBAL_DIR}/04-security-auth" -name "*.md" -type f -size 0 | wc -l | tr -d ' ')

### Testing Domain
- Files integrated: 3
- Backups created: $(ls -1 "${GLOBAL_DIR}/05-testing-quality"/*.backup 2>/dev/null | wc -l | tr -d ' ')

## File Sizes

### Security Files
EOF

    # Add security file sizes
    for f in "${GLOBAL_DIR}/04-security-auth"/*.md; do
        if [ -f "$f" ]; then
            size=$(wc -l < "$f" | tr -d ' ')
            echo "- $(basename "$f"): $size lines" >> "$REPORT_FILE"
        fi
    done

    cat >> "$REPORT_FILE" << EOF

### Testing Files
EOF

    # Add testing file sizes
    for f in "${GLOBAL_DIR}/05-testing-quality"/{VITEST_PATTERNS,E2E_TESTING,MOCKING_PATTERNS}.md; do
        if [ -f "$f" ]; then
            size=$(wc -l < "$f" | tr -d ' ')
            echo "- $(basename "$f"): $size lines" >> "$REPORT_FILE"
        fi
    done

    cat >> "$REPORT_FILE" << EOF

## Next Steps

1. Review HTML artifacts in security files (especially JWT_PATTERNS.md)
2. Manually integrate frontend domain files (requires merging)
3. Manually integrate database domain files (requires careful merging)
4. Update cross-references and index files
5. Run quality assurance checks

## Full Log

See: $LOG_FILE
EOF

    success "Report generated: $REPORT_FILE"
}

# Main execution
main() {
    log "Starting Knowledge Base Integration"
    log "Log file: $LOG_FILE"

    # Verify we're in the right directory
    if [ ! -d "$GLOBAL_DIR" ] || [ ! -d "$RESULTS_DIR" ]; then
        error "Required directories not found. Are you in the right location?"
    fi

    # Execute phases
    phase_1_backup
    phase_2_security
    phase_3_validate_security
    phase_4_testing
    phase_5_report

    success "Integration complete! Review report and logs."
    echo ""
    echo "Report: Check $(basename "$REPORT_FILE")"
    echo "Log: Check $(basename "$LOG_FILE")"
    echo ""
    echo "IMPORTANT: Frontend and Database domains require manual integration."
    echo "See INTEGRATION_PLAN.md for detailed instructions."
}

# Run main function
main "$@"
