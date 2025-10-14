# Design Decisions - Knowledge Organization System

**Date**: 2025-10-14
**Status**: Approved - Ready for Implementation

---

## Approved Decisions

### 1. Folder Sharing ✅
**Decision**: 1A - **No, folders are per-project only**

**Rationale**: Simplifies implementation, avoids complexity of shared folder management, keeps project contexts isolated.

**Implementation Impact**: No changes needed to current design.

---

### 2. Folder Hierarchy ✅
**Decision**: 2A - **Phase 2 - Single-level first**

**Rationale**: Keeps initial implementation simple, allows validation of folder usage patterns before adding complexity, avoids over-engineering.

**Implementation Impact**:
- No parent_id column needed in Phase 1
- Can be added later if needed
- Database design supports future extension

---

### 3. Tag Hierarchy ✅
**Decision**: 3A - **No, flat tags with categories**

**Rationale**: Categories already provide organization, hierarchical tags add complexity without clear benefit for current use cases.

**Implementation Impact**:
- Current tag table design is final
- No parent-child relationships needed
- Simpler UI implementation

---

### 4. Moving Sources Between Projects ✅
**Decision**: 4A - **Yes, via UI**

**Rationale**: Provides flexibility for users to reorganize knowledge as projects evolve, UX improvement without significant complexity.

**Implementation Impact**:
- Add UI actions for changing project_id
- Add API endpoint: `PUT /api/knowledge/{source_id}/scope`
- Update frontend service with move operation

---

### 5. Auto-Tagging Behavior ✅
**Decision**: 5A - **Auto-suggest with user review**

**Rationale**: Balances automation with user control, ensures tag quality, allows users to learn tagging patterns.

**Implementation Impact**:
- AutoTaggingService returns suggestions (not automatic application)
- AddKnowledgeDialog shows suggested tags
- User can accept/modify/reject before save
- API: `POST /api/knowledge/suggest-tags` (body: url, title, summary)

---

### 6. Default Scope When Adding Knowledge ✅
**Decision**: 6A - **Prompt user with context-aware default**

**Rationale**: Respects user intent, prevents accidental scoping, provides smart default while allowing override.

**Implementation Impact**:
- AddKnowledgeDialog detects project context
- Shows "Link to {project_name}?" when in project context
- Pre-selects "Yes" but allows user to change
- Global scope remains default when no project context

---

## Implementation Notes

### Phase 1 Simplifications

Based on approved decisions, Phase 1 can proceed with:
- Single-level folders (no nesting)
- Flat tags with categories (no hierarchy)
- Per-project folders (no sharing)
- Auto-suggest tagging (not automatic)
- Context-aware scope prompting

### Future Enhancements (Post-V1)

These features are explicitly **NOT** in scope for initial implementation:
- ❌ Nested folders
- ❌ Hierarchical tags
- ❌ Shared folders across projects
- ❌ Automatic tagging without review
- ❌ Forced project linking

---

## Updated Implementation Priorities

### Must Have for Phase 1
1. ✅ Database schema with approved design
2. ✅ Single-level folder support
3. ✅ Flat tag system with categories
4. ✅ Scope selection in UI
5. ✅ Auto-suggest tagging API
6. ✅ Context-aware defaults

### Nice to Have for Phase 1
- Bulk operations (link/unlink multiple sources)
- Tag usage analytics
- Folder color customization
- Source recommendation based on project type

### Deferred to Phase 2
- Nested folder support
- Tag hierarchy
- Shared folder templates
- Advanced auto-tagging (ML-based)

---

**Approved By**: User
**Approved Date**: 2025-10-14
**Ready for Implementation**: ✅ YES
