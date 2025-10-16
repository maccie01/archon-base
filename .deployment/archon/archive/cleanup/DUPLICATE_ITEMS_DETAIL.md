# Duplicate Knowledge Items - Detailed Deletion Guide

Date: 2025-10-15
Total duplicate groups: 16

## Category 1: Exact Duplicates (Same Tags)

These are likely ingestion errors. Keep the most recent, delete others.

### ACCESSIBILITY.md

**Tags**: global, 01 react frontend

**KEEP**: file_ACCESSIBILITY_md_b49cf4f1 (created: 2025-10-15)

**DELETE**: file_ACCESSIBILITY_md_c17ff256 (created: 2025-10-14)
```bash
curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_ACCESSIBILITY_md_c17ff256
```

### API_SECURITY.md

**Tags**: global, 04 security auth

**KEEP**: file_API_SECURITY_md_c2068d78 (created: 2025-10-15)

**DELETE**: file_API_SECURITY_md_5869634c (created: 2025-10-15)
```bash
curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_API_SECURITY_md_5869634c
```

### BACKEND_TESTING.md

**Tags**: global, 05 testing quality

**KEEP**: file_BACKEND_TESTING_md_3c041367 (created: 2025-10-15)

**DELETE**: file_BACKEND_TESTING_md_7de5c725 (created: 2025-10-15)
```bash
curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_BACKEND_TESTING_md_7de5c725
```

### COMPONENT_PATTERNS.md

**Tags**: global, 01 react frontend

**KEEP**: file_COMPONENT_PATTERNS_md_b35f28a5 (created: 2025-10-15)

**DELETE**: file_COMPONENT_PATTERNS_md_383cef4c (created: 2025-10-15)
```bash
curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_COMPONENT_PATTERNS_md_383cef4c
```

### TYPESCRIPT_REACT.md

**Tags**: global, 01 react frontend

**KEEP**: file_TYPESCRIPT_REACT_md_c493c221 (created: 2025-10-15)

**DELETE**: file_TYPESCRIPT_REACT_md_b9ce3f76 (created: 2025-10-15)
```bash
curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_TYPESCRIPT_REACT_md_b9ce3f76
```

### VALIDATION.md

**Tags**: global, 02 nodejs backend

**KEEP**: file_VALIDATION_md_f92c4122 (created: 2025-10-15)

**DELETE**: file_VALIDATION_md_a516c64f (created: 2025-10-15)
```bash
curl -X DELETE -H 'Authorization: Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI' \
  http://localhost:8181/api/knowledge-items/file_VALIDATION_md_a516c64f
```


## Category 2: Cross-Domain Duplicates (Different Tags)

These may have domain-specific content. Review before deletion.

### ANTIPATTERNS.md

- **ID**: `file_ANTIPATTERNS_md_ec938548`
  **Tags**: global, 01 react frontend
  **Created**: 2025-10-14
  **Words**: 1,644

- **ID**: `file_ANTIPATTERNS_md_03c22868`
  **Tags**: global, 01 react frontend
  **Created**: 2025-10-15
  **Words**: 1,644

- **ID**: `file_ANTIPATTERNS_md_c2eb5e57`
  **Tags**: global, 02 nodejs backend
  **Created**: 2025-10-15
  **Words**: 652

- **ID**: `file_ANTIPATTERNS_md_7ab8f243`
  **Tags**: global, 03 database orm
  **Created**: 2025-10-15
  **Words**: 1,759

- **ID**: `file_ANTIPATTERNS_md_a58140ea`
  **Tags**: global, 04 security auth
  **Created**: 2025-10-15
  **Words**: 3,449

**Recommendation**: Review content to determine if truly duplicates.

### AUTHORIZATION.md

- **ID**: `file_AUTHORIZATION_md_06dc8291`
  **Tags**: global, 02 nodejs backend
  **Created**: 2025-10-15
  **Words**: 186

- **ID**: `file_AUTHORIZATION_md_a8b2b29a`
  **Tags**: projects, netzwaechter refactored, 03 authentication
  **Created**: 2025-10-15
  **Words**: 997

**Recommendation**: Review content to determine if truly duplicates.

### BUILD_CONFIGURATION.md

- **ID**: `file_BUILD_CONFIGURATION_md_eed405ee`
  **Tags**: global, 06 configuration
  **Created**: 2025-10-15
  **Words**: 367

- **ID**: `file_BUILD_CONFIGURATION_md_2deac3fa`
  **Tags**: projects, netzwaechter refactored, 06 configuration
  **Created**: 2025-10-15
  **Words**: 1,950

**Recommendation**: Review content to determine if truly duplicates.

### ENVIRONMENT_VARIABLES.md

- **ID**: `file_ENVIRONMENT_VARIABLES_md_2b59f936`
  **Tags**: global, 06 configuration
  **Created**: 2025-10-15
  **Words**: 1,062

- **ID**: `file_ENVIRONMENT_VARIABLES_md_7607c12d`
  **Tags**: projects, netzwaechter refactored, 06 configuration
  **Created**: 2025-10-15
  **Words**: 1,661

**Recommendation**: Review content to determine if truly duplicates.

### ERROR_HANDLING.md

- **ID**: `file_ERROR_HANDLING_md_9b81b659`
  **Tags**: global, 01 react frontend
  **Created**: 2025-10-15
  **Words**: 1,467

- **ID**: `file_ERROR_HANDLING_md_dee1136d`
  **Tags**: global, 02 nodejs backend
  **Created**: 2025-10-15
  **Words**: 298

**Recommendation**: Review content to determine if truly duplicates.

### QUICK_START.md

- **ID**: `file_QUICK_START_md_1924f9a7`
  **Tags**: knowledge organization
  **Created**: 2025-10-15
  **Words**: 566

- **ID**: `file_QUICK_START_md_fb59454a`
  **Tags**: projects, netzwaechter refactored, 08 deployment
  **Created**: 2025-10-15
  **Words**: 270

**Recommendation**: Review content to determine if truly duplicates.

### SECRETS_MANAGEMENT.md

- **ID**: `file_SECRETS_MANAGEMENT_md_94a284f5`
  **Tags**: global, 04 security auth
  **Created**: 2025-10-15
  **Words**: 4,751

- **ID**: `file_SECRETS_MANAGEMENT_md_2c0cb80c`
  **Tags**: global, 06 configuration
  **Created**: 2025-10-15
  **Words**: 516

**Recommendation**: Review content to determine if truly duplicates.

### SERVICE_LAYER.md

- **ID**: `file_SERVICE_LAYER_md_23ef856e`
  **Tags**: global, 02 nodejs backend
  **Created**: 2025-10-15
  **Words**: 596

- **ID**: `file_SERVICE_LAYER_md_9b64ec84`
  **Tags**: projects, netzwaechter refactored, 05 backend
  **Created**: 2025-10-15
  **Words**: 1,815

**Recommendation**: Review content to determine if truly duplicates.


## Category 3: README.md Duplicates

Special case with 17 instances. Organized by tags:

### global-01 react frontend (1 instances)

- `file_README_md_4f03ae3d` - Tags: [global, 01 react frontend]

### global-02 nodejs backend (1 instances)

- `file_README_md_54701ea9` - Tags: [global, 02 nodejs backend]

### global-03 database orm (1 instances)

- `file_README_md_54d9bd33` - Tags: [global, 03 database orm]

### global-04 security auth (1 instances)

- `file_README_md_0fe77ee6` - Tags: [global, 04 security auth]

### global-05 testing quality (1 instances)

- `file_README_md_711751b0` - Tags: [global, 05 testing quality]

### global-06 configuration (1 instances)

- `file_README_md_cf2fd75a` - Tags: [global, 06 configuration]

### global-only (1 instances)

- `file_README_md_9a7fd849` - Tags: [global]

### knowledge-org (1 instances)

- `file_README_md_a2d28326` - Tags: [knowledge organization]

### project-01 database (1 instances)

- `file_README_md_8ebff141` - Tags: [projects, netzwaechter refactored, 01 database]

### project-02 api endpoints (1 instances)

- `file_README_md_942981e3` - Tags: [projects, netzwaechter refactored, 02 api endpoints]

### project-04 frontend (1 instances)

- `file_README_md_6fa7af09` - Tags: [projects, netzwaechter refactored, 04 frontend]

### project-05 backend (1 instances)

- `file_README_md_f7b26ce4` - Tags: [projects, netzwaechter refactored, 05 backend]

### project-07 standards (1 instances)

- `file_README_md_b5bc770d` - Tags: [projects, netzwaechter refactored, 07 standards]

### project-08 deployment (1 instances)

- `file_README_md_c0b24873` - Tags: [projects, netzwaechter refactored, 08 deployment]

### project-general (1 instances)

- `file_README_md_9f87f54d` - Tags: [projects, netzwaechter refactored]

### untagged (2 instances)

- `file_README_md_11eb7727` - Tags: []
- `file_README_md_81ba5866` - Tags: []

**Recommendation for READMEs**:

1. **DELETE untagged** (2 instances)
2. **KEEP project-specific** versions (6 instances)
3. **KEEP one global per topic** (review for actual differences)
4. **KEEP knowledge-org** version


## Category 4: Untagged Duplicates

### MIGRATION_READY_REPORT.md

- **ID**: `file_MIGRATION_READY_REPORT_md_de6cd9a3`
  **Tags**: NONE
  **Created**: 2025-10-14

- **ID**: `file_MIGRATION_READY_REPORT_md_abeb052b`
  **Tags**: NONE
  **Created**: 2025-10-15

**Action**: Tag appropriately, then keep most recent.


## Summary

- **Exact duplicates to delete**: 6 items
- **Cross-domain duplicates to review**: 19 items
- **README.md instances**: 17 (recommend deleting 5-8)
- **Untagged duplicates**: 2 items

**Total potential deletions**: 20-30 items

