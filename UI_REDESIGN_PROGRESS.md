# Archon UI Redesign: Neon/Tron to Apple-Inspired Pastel Theme

## Progress Report

**Date:** 2025-10-14
**Status:** In Progress (Phase 1 Complete - Foundation Updates)

---

## Overview

This document tracks the comprehensive UI redesign from the neon/Tron-themed aesthetic to a clean, Apple-inspired minimalist design with pastel colors. The index.css file has been updated with new color variables, but 93+ component files still reference old cyan/neon colors.

---

## ✅ Completed Changes

### 1. Custom CSS Files (100% Complete)

#### `/archon-ui-main/src/styles/card-animations.css`
- ✅ Renamed `.card-neon-line` to `.card-accent-line`
- ✅ Renamed `.card-neon-line-pulse` to `.card-accent-line-pulse`
- ✅ Updated `neon-pulse` animation to `accent-pulse` with reduced intensity (removed brightness filter, opacity-only animation)

#### `/archon-ui-main/src/styles/luminous-button.css`
- ✅ Renamed `pulse-glow` to `pulse-subtle`
- ✅ Reduced animation scale from 1.05 to 1.02
- ✅ Reduced opacity range from 0.6-0.8 to 0.7-0.9

#### `/archon-ui-main/src/styles/toggle.css`
- ✅ Removed all glow effects (drop-shadow filters removed from icons)
- ✅ Removed `box-shadow` glows from all toggle variants
- ✅ Renamed `toggleGlow` animation to `togglePulse` with subtle opacity changes
- ✅ Updated color variants to use pastel RGB values:
  - Purple: 183, 148, 244 (was 168, 85, 247)
  - Green: 130, 201, 169 (was 16, 185, 129)
  - Pink: 240, 171, 210 (was 236, 72, 153)
  - Blue: 115, 169, 240 (was 59, 130, 246)
  - Orange: 255, 180, 138 (was 249, 115, 22)
- ✅ Reduced background opacity from 0.2 to 0.15
- ✅ Reduced border opacity from 0.5 to 0.4

### 2. UI Primitive Components (Partial - 40% Complete)

#### `/archon-ui-main/src/features/ui/primitives/button.tsx`
- ✅ Changed variant name from `"cyan"` to `"primary"`
- ✅ Updated border radius from `rounded-md` to `rounded-xl` (0.75rem)
- ✅ Reduced transition duration from 300ms to 200ms
- ✅ Changed focus ring from `ring-cyan-500` to `ring-primary`
- ✅ **Default variant:** Simplified to use `bg-primary` with `shadow-sm hover:shadow-md`
- ✅ **Destructive variant:** Simplified to use `bg-destructive` with subtle shadows
- ✅ **Outline variant:** Uses `border-border` and `hover:bg-muted`
- ✅ **Ghost variant:** Uses `text-foreground` and `hover:bg-muted`
- ✅ **Link variant:** Uses `text-primary` with underline
- ✅ **Primary variant:** Pastel blue gradient with `blue-pastel` color
- ✅ **Knowledge variant:** Pastel purple gradient with `purple-pastel` color
- ✅ Removed all neon glow shadows (`shadow-[0_0_*px_rgba(...)]`)

#### `/archon-ui-main/src/features/ui/primitives/styles.ts`
- ✅ Updated file header comment from "Tron-inspired" to "Apple-inspired minimalist"
- ✅ Updated `glassmorphism.border`:
  - Changed `focus` from cyan glow to `focus:ring-2 focus:ring-primary/20`
  - Changed `hover` from cyan glow to `hover:border-primary/50`
  - Replaced color-specific borders with semantic tokens
- ✅ Updated `glassmorphism.interactive`:
  - Changed hover from `hover:bg-cyan-500/10` to `hover:bg-muted`
  - Changed active from `active:bg-cyan-500/20` to `active:bg-muted/80`
  - Changed selected state to use `bg-primary/10` and `text-primary`
- ✅ Updated `glassmorphism.shadow`:
  - Removed all neon glow definitions
  - Replaced `shadow.glow` object with `shadow.accent` using subtle `shadow-sm` with pastel colors
  - Simplified shadow levels (sm, md, lg, elevated)
- ✅ Updated `glassmorphism.priority`:
  - Changed `glow` property to `shadow: "shadow-sm"`
  - Updated colors to use pastel variants (`orange-pastel`, `blue-pastel`)
  - Simplified hover states
- ✅ Updated `glassCard.base`:
  - Changed border radius from `rounded-lg` to `rounded-xl`
  - Reduced transition duration from 300ms to 200ms

### 3. Color Palette (Already in index.css)

The following pastel colors are defined and ready to use:

**Light Mode:**
- Primary: `hsl(213 94% 68%)` - soft blue
- Background: `hsl(0 0% 99%)` - nearly white
- Foreground: `hsl(0 0% 13%)` - dark gray
- Border: `hsl(214 32% 91%)` - light blue-gray
- Muted: `hsl(210 40% 96.5%)` - very light blue

**Dark Mode:**
- Primary: `hsl(213 94% 68%)` - soft blue
- Background: `hsl(220 13% 9%)` - dark blue-gray
- Foreground: `hsl(0 0% 95%)` - light gray
- Border: `hsl(220 13% 20%)` - medium dark

**Pastel Accents (Custom):**
- Purple: `hsl(250 60% 75%)`
- Green: `hsl(142 52% 70%)`
- Pink: `hsl(330 60% 80%)`
- Blue: `hsl(213 94% 68%)`
- Orange: `hsl(25 95% 70%)`
- Teal: `hsl(180 55% 70%)`

---

## 🚧 Remaining Work

### 3. Complete styles.ts Updates (CRITICAL - High Priority)

The following sections in `/archon-ui-main/src/features/ui/primitives/styles.ts` still contain extensive neon glow definitions that need to be removed or converted to subtle shadows:

#### `glassCard.variants` (Lines 246-288)
Contains 7 color variants (none, purple, blue, green, cyan, orange, pink, red) with heavy glow shadows:
- Current: `shadow-[0_0_40px_15px_rgba(...)]` and `hover:shadow-[0_0_50px_20px_rgba(...)]`
- **Needed:** Replace with `shadow-sm` or remove entirely, use border colors instead

#### `glassCard.outerGlowSizes` (Lines 290-334)
Contains glow size variants (sm, md, lg, xl) for each color:
- Current: `shadow-[0_0_20px_rgba(...)]` to `shadow-[0_0_100px_rgba(...)]`
- **Needed:** Replace with standard Tailwind shadows (shadow-sm, shadow-md, shadow-lg)

#### `glassCard.innerGlowSizes` (Lines 336-380)
Contains inner glow variants:
- Current: `shadow-[inset_0_0_15px_rgba(...)]` to `shadow-[inset_0_0_120px_rgba(...)]`
- **Needed:** Remove or replace with subtle inset borders

#### `glassCard.outerGlowHover` (Lines 382-426)
Hover state glows:
- **Needed:** Replace with simple `hover:shadow-md` or remove

#### `glassCard.innerGlowHover` (Lines 428-471)
Inner glow hover states:
- **Needed:** Remove or use subtle opacity changes

#### `glassCard.edgeColors` (Lines 146-190)
Edge-lit card color definitions using 500-weight colors:
- **Needed:** Update to use pastel color variants

#### `glassCard.tints` (Lines 192-244)
Colored glass tints using 400/500-weight colors:
- **Needed:** Update to use pastel variants

#### `glassCard.edgeLit` (Lines 482-566)
Edge-lighting effects with glow shadows:
- Current: `before:shadow-[0_0_15px_4px_rgba(...,0.8)]`
- **Needed:** Remove or significantly reduce glow intensity

### 4. Legacy Component Updates (93 Files Total)

Based on grep search, the following categories need updates:

#### High Priority - Core UI Components (20 files)
- `/components/ui/NeonButton.tsx` - Heavily neon-themed, needs complete redesign
- `/components/ui/PowerButton.tsx`
- `/components/ui/Card.tsx`
- `/components/ui/Button.tsx`
- `/components/ui/Badge.tsx`
- `/components/ui/Input.tsx`
- `/components/ui/Select.tsx`
- `/components/ui/Checkbox.tsx`
- `/components/ui/ThemeToggle.tsx`
- `/components/ui/GlassCrawlDepthSelector.tsx`
- `/components/ui/CollapsibleSettingsCard.tsx`

#### Medium Priority - Feature Components (30 files)

**Knowledge Feature:**
- `/features/knowledge/components/KnowledgeCard.tsx`
- `/features/knowledge/components/KnowledgeTabs.tsx`
- `/features/knowledge/components/TagsIndexView.tsx`
- `/features/knowledge/components/AddKnowledgeDialog.tsx`
- `/features/knowledge/components/KnowledgeCardType.tsx`
- `/features/knowledge/components/KnowledgeCardTitle.tsx`
- `/features/knowledge/components/KnowledgeCardTags.tsx`
- `/features/knowledge/components/KnowledgeTable.tsx`
- `/features/knowledge/components/KnowledgeList.tsx`
- `/features/knowledge/components/KnowledgeHeader.tsx`
- `/features/knowledge/components/KnowledgeTypeSelector.tsx`
- `/features/knowledge/components/LevelSelector.tsx`
- `/features/knowledge/views/KnowledgeView.tsx`
- `/features/knowledge/inspector/components/InspectorSidebar.tsx`
- `/features/knowledge/inspector/components/InspectorHeader.tsx`
- `/features/knowledge/inspector/components/ContentViewer.tsx`

**Project Feature:**
- `/features/projects/components/ProjectCard.tsx`
- `/features/projects/components/ProjectHeader.tsx`
- `/features/projects/components/ProjectCardActions.tsx`
- `/features/projects/components/NewProjectModal.tsx`
- `/features/projects/views/ProjectsView.tsx`

**Task Feature:**
- `/features/projects/tasks/components/TaskCard.tsx`
- `/features/projects/tasks/components/TaskCardActions.tsx`
- `/features/projects/tasks/components/TaskAssignee.tsx`
- `/features/projects/tasks/components/TaskEditModal.tsx`
- `/features/projects/tasks/components/TaskPriorityComponent.tsx`
- `/features/projects/tasks/components/KanbanColumn.tsx`
- `/features/projects/tasks/components/EditableTableCell.tsx`
- `/features/projects/tasks/views/TableView.tsx`
- `/features/projects/tasks/utils/task-styles.tsx`
- `/features/projects/tasks/TasksTab.tsx`

**Document Feature:**
- `/features/projects/documents/components/DocumentCard.tsx`
- `/features/projects/documents/components/DocumentViewer.tsx`
- `/features/projects/documents/components/AddDocumentModal.tsx`
- `/features/projects/documents/DocsTab.tsx`

#### Lower Priority - Supporting Components (25 files)

**Progress & MCP:**
- `/features/progress/components/CrawlingProgress.tsx`
- `/features/progress/components/KnowledgeCardProgress.tsx`
- `/features/mcp/components/McpStatusBar.tsx`
- `/features/mcp/components/McpConfigSection.tsx`
- `/features/mcp/components/McpClientList.tsx`
- `/features/mcp/views/McpView.tsx`

**Layout & Navigation:**
- `/components/layout/Navigation.tsx`
- `/components/layout/MainLayout.tsx`
- `/components/DisconnectScreenOverlay.tsx`
- `/components/animations/Animations.tsx`
- `/components/animations/DisconnectScreenAnimations.tsx`

**Settings:**
- `/components/settings/RAGSettings.tsx`
- `/components/settings/OllamaModelSelectionModal.tsx`
- `/components/settings/FeaturesSection.tsx`
- `/components/settings/CodeExtractionSettings.tsx`
- `/components/settings/ButtonPlayground.tsx`
- `/pages/SettingsPage.tsx`

**Misc:**
- `/components/common/DeleteConfirmModal.tsx`
- `/components/code/CodeViewerModal.tsx`
- `/components/agent-chat/ArchonChatPanel.tsx`

#### Lowest Priority - Style Guide & Examples (18 files)
- All files in `/features/style-guide/` directory
- These demonstrate old patterns and should be updated last

### 5. Primitive Components Remaining

The following primitive components in `/features/ui/primitives/` still need review and updates:

- `tooltip.tsx` - Check for cyan colors
- `toast.tsx` - Check for cyan colors
- `tabs.tsx` - Check for cyan colors
- `switch.tsx` - Check for cyan colors
- `select.tsx` - Check for cyan colors
- `radio-group.tsx` - Check for cyan colors
- `pill.tsx` - Check for cyan colors
- `pill-navigation.tsx` - Check for cyan colors
- `inspector-dialog.tsx` - Check for cyan colors
- `input.tsx` - Check for cyan colors
- `grouped-card.tsx` - Check for cyan colors
- `dropdown-menu.tsx` - Check for cyan colors
- `dialog.tsx` - Check for cyan colors
- `data-card.tsx` - Check for cyan colors
- `combobox.tsx` - Check for cyan colors
- `checkbox.tsx` - Check for cyan colors
- `card.tsx` - Verify glow color references
- `alert-dialog.tsx` - Check for cyan colors
- `OptimisticIndicator.tsx` - Check for cyan colors
- `selectable-card.tsx` - Check for cyan colors
- `toggle-group.tsx` - Check for cyan colors

---

## 🎯 Recommended Action Plan

### Phase 1: Foundation (COMPLETED ✅)
1. ✅ Update custom CSS files
2. ✅ Update button.tsx primitive
3. ✅ Partial update to styles.ts

### Phase 2: Complete Core Styles (NEXT - HIGH PRIORITY)
1. ⚠️ Complete `styles.ts` glow removal:
   - Replace all `glassCard.variants` glow shadows with `shadow-sm` or remove
   - Replace `outerGlowSizes` with standard Tailwind shadows
   - Remove or simplify `innerGlowSizes`
   - Simplify hover effects
   - Update `edgeColors` and `tints` to use pastel variants
   - Simplify `edgeLit` effects

2. Update remaining UI primitives (20 files)

### Phase 3: Feature Components (MEDIUM PRIORITY)
1. Update knowledge feature components (16 files)
2. Update project/task/document components (19 files)
3. Update progress/MCP components (6 files)

### Phase 4: Supporting Components
1. Update layout & navigation (5 files)
2. Update settings components (6 files)
3. Update misc components (4 files)

### Phase 5: Style Guide & Examples
1. Update all style guide showcase files (18 files)

---

## 🔍 Search Patterns Used

The following grep patterns were used to identify files needing updates:

```bash
# Neon/cyan color references
grep -r "cyan|neon|#0ff|#0ea5e9|#06b6d4|rgb(6, 182, 212)" --include="*.tsx" --include="*.ts"

# Glow shadow effects
grep -r "shadow-\[0_0_|shadow-\[0_4px_20px|glow|neon-glow" --include="*.tsx" --include="*.ts" --include="*.css"
```

---

## 📋 Component Update Checklist

For each component file, apply the following changes:

### Color Replacements
- [ ] Replace `cyan-*` with `primary` or pastel blue (`blue-pastel`)
- [ ] Replace `purple-500/400` with `purple-pastel`
- [ ] Replace `green-500/400` with `green-pastel`
- [ ] Replace `pink-500/400` with `pink-pastel`
- [ ] Replace `orange-500/400` with `orange-pastel`
- [ ] Replace hex colors (#0ea5e9, #06b6d4, #0ff) with semantic tokens

### Shadow Replacements
- [ ] Replace `shadow-[0_0_*px_rgba(...)]` with `shadow-sm`, `shadow-md`, or `shadow-lg`
- [ ] Remove glow animations (brightness filters, heavy blur)
- [ ] Replace `hover:shadow-[0_0_*px_...]` with `hover:shadow-md`

### Border & Radius Updates
- [ ] Update `rounded-md` to `rounded-xl` (0.75rem)
- [ ] Replace border glow classes with clean `border-border` or `border-primary`
- [ ] Simplify focus states to use `ring-2 ring-primary/20`

### Transition Updates
- [ ] Reduce transition durations from 300ms to 200ms
- [ ] Ensure smooth, subtle transitions (Apple-like)

### Glassmorphism Updates
- [ ] Reduce backdrop blur intensity where appropriate
- [ ] Lighten background opacity for cleaner glass effect
- [ ] Remove heavy gradient overlays

---

## 🎨 Design Principles for Updates

### Apple-Inspired Guidelines
1. **Clean, minimal borders** - Use subtle `border-border` instead of colored borders
2. **Subtle shadows** - Prefer `shadow-sm` and `shadow-md` over custom glows
3. **Pastel colors** - Use the predefined pastel variants, not bright neon colors
4. **Generous white space** - Don't overcrowd elements
5. **Soft rounded corners** - Consistent 0.75rem (rounded-xl)
6. **Smooth transitions** - 200-300ms duration, ease-out timing
7. **No heavy gradients** - Simple, clean color fills
8. **Subtle hover effects** - Slight shadow or background change, no glows

### Color Usage Guidelines
- **Primary actions:** Use `bg-primary` or pastel blue
- **Destructive actions:** Use `bg-destructive` (red)
- **Success:** Use pastel green
- **Warning:** Use pastel orange
- **Info:** Use pastel blue
- **Neutral:** Use `bg-muted` and `text-muted-foreground`

---

## 📊 Progress Summary

| Category | Files Found | Files Updated | Progress |
|----------|-------------|---------------|----------|
| Custom CSS | 3 | 3 | 100% ✅ |
| UI Primitives | 25 | 2 | 8% 🚧 |
| Legacy Components | 11 | 0 | 0% ⏳ |
| Knowledge Feature | 16 | 0 | 0% ⏳ |
| Project Feature | 23 | 0 | 0% ⏳ |
| Progress/MCP | 6 | 0 | 0% ⏳ |
| Layout/Settings | 11 | 0 | 0% ⏳ |
| Style Guide | 18 | 0 | 0% ⏳ |
| **TOTAL** | **93+** | **5** | **5%** |

---

## 🚨 Critical Dependencies

Before completing component updates, ensure:

1. ✅ `index.css` has all pastel color variables defined
2. ⚠️ `styles.ts` glow definitions removed (IN PROGRESS)
3. ⚠️ Tailwind config updated to recognize pastel color names (if using custom colors)
4. ✅ Border radius consistency (0.75rem = rounded-xl)

---

## 💡 Notes for Developers

### Testing Strategy
After updating each component:
1. Test in both light and dark modes
2. Verify hover/focus states work correctly
3. Check color contrast for accessibility
4. Ensure responsive design is maintained
5. Verify no dynamic Tailwind class construction

### Common Pitfalls
- **Don't** hardcode pastel colors inline - use Tailwind classes
- **Don't** mix old cyan colors with new pastel colors
- **Don't** keep heavy glow shadows - replace with subtle shadows
- **Do** maintain functional behavior - only change visual styling
- **Do** use semantic color tokens (`primary`, `destructive`, etc.) when possible

### Tailwind Configuration
If using custom pastel colors, add to `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'purple-pastel': 'hsl(250 60% 75%)',
      'green-pastel': 'hsl(142 52% 70%)',
      'pink-pastel': 'hsl(330 60% 80%)',
      'blue-pastel': 'hsl(213 94% 68%)',
      'orange-pastel': 'hsl(25 95% 70%)',
      'teal-pastel': 'hsl(180 55% 70%)',
    }
  }
}
```

---

## 📝 Change Log

### 2025-10-14
- ✅ Completed Phase 1: Custom CSS files updated
- ✅ Updated button.tsx primitive component
- ✅ Partial update to styles.ts (glassmorphism section)
- 📄 Created this progress tracking document

---

## 🤝 Contributing

When updating files:
1. Follow the checklist above
2. Update this document's progress table
3. Mark completed items with ✅
4. Note any issues or deviations in the Notes section
5. Test thoroughly before marking as complete

---

**Last Updated:** 2025-10-14
**Next Priority:** Complete styles.ts glow removal (Phase 2)
