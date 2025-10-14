---
description: Perform UI/UX quality review on frontend changes with accessibility, responsive design, and visual consistency checks
---

# Design Review Workflow

Conduct comprehensive UI/UX design review on frontend changes to ensure accessibility, responsiveness, and design system compliance.

## Usage

```bash
# Review all uncommitted UI changes
/design-review

# Review specific components
/design-review src/components/Button.tsx src/components/Modal.tsx

# Review a feature branch
/design-review main...feature/new-dashboard
```

## Step 1: Identify UI Changes

Determine what frontend code has changed:

```bash
# Find all changed frontend files
git diff --name-only | grep -E "\.(tsx|jsx|css|scss)$"

# Or if reviewing specific files/commit
git diff <ref> --name-only | grep -E "\.(tsx|jsx|css|scss)$"

# Get the actual diff
git diff <ref> -- <frontend-files>
```

Store the list of changed UI files and their diffs.

## Step 2: Analyze Components and Patterns

Identify what UI elements are being added/modified:

```bash
# Look for new components
grep -r "export.*function\|export.*const.*=.*=>Grep" <changed-files>

# Find interactive elements
grep -r "onClick\|onSubmit\|button\|input\|form" <changed-files>

# Check for styling
grep -r "className\|style={{" <changed-files>

# Look for accessibility attributes
grep -r "aria-\|role=\|alt=" <changed-files>

# Find responsive utilities
grep -r "sm:\|md:\|lg:\|@media" <changed-files>
```

Create a summary of what UI elements are changing.

## Step 3: Search Design Documentation

Use Archon MCP tools to find design context:

```bash
# Search for design system docs
rag_search_knowledge_base(query="design system", match_count=5)

# Find UI component patterns
rag_search_code_examples(query="<component-type>", match_count=3)

# Look for accessibility standards
rag_search_knowledge_base(query="accessibility WCAG", match_count=3)

# Search for UI guidelines
rag_search_knowledge_base(query="UI standards", match_count=5)

# Get available sources
rag_get_available_sources()
# Look for "Design Guidelines", "Component Library", "Style Guide", etc.
```

Store design system rules and component patterns.

## Step 4: Invoke Design Reviewer Agent

Use the Task tool to invoke the design-reviewer specialist agent:

```xml
<use_task_tool>
{
  "subagent_type": "design-reviewer",
  "prompt": "Perform comprehensive UI/UX design review on the following frontend changes:

**Changes Summary:**
[Describe what UI elements changed - new components, modified styles, etc.]

**Changed Files:**
<changed-files>

**Git Diff:**
```
[Paste the relevant UI diff here]
```

**Component Analysis:**
[Include what types of components are changing - buttons, forms, modals, etc.]

**Design System Context:**
[Include design system rules, component patterns from knowledge base]

**Technology Stack:**
[React, Vue, Tailwind, etc.]

Review the changes across all 7 phases:
1. Interaction & User Flow
2. Responsiveness (desktop 1440px, tablet 768px, mobile 375px)
3. Visual Polish (spacing, typography, colors)
4. Accessibility (WCAG 2.1 AA compliance)
5. Robustness (empty states, error handling, loading states)
6. Code Health (component reuse, design tokens)
7. Content & Console (clear labels, no errors)

Provide structured feedback with severity levels:
- Blocker: Critical issues requiring immediate fix
- High: Significant issues to fix before merge
- Medium: Improvements for follow-up
- Nitpick: Minor aesthetic details
",
  "description": "Perform UI/UX design review"
}
</use_task_tool>
```

## Step 5: Manual Testing Guidance

If the code is running locally, provide testing instructions:

```markdown
## Manual Testing Checklist

To complete this design review, please test the following:

### Keyboard Navigation
1. Press Tab key to navigate through interactive elements
2. Verify visible focus states on all focusable elements
3. Press Enter/Space on buttons and links
4. Ensure no keyboard traps (can always Tab away)
5. Check Escape key closes modals/dropdowns

### Responsive Testing
1. **Desktop (1440px)**: Open browser DevTools (F12)
   - Set viewport to 1440x900
   - Verify layout looks good
   - Check no horizontal scroll

2. **Tablet (768px)**:
   - Set viewport to 768x1024
   - Verify layout adapts gracefully
   - Check touch targets are adequate

3. **Mobile (375px)**:
   - Set viewport to 375x667
   - Verify fully functional
   - Check touch targets ≥44x44px
   - Test horizontal orientation

### Accessibility
1. **Color Contrast**:
   - Open DevTools → Inspect element
   - Check contrast ratio (minimum 4.5:1)

2. **Screen Reader** (optional but recommended):
   - Mac: Enable VoiceOver (Cmd+F5)
   - Windows: Use NVDA (free)
   - Navigate through page and verify announcements

3. **Images**: Check all images have alt text

4. **Forms**: Verify all inputs have labels

### Browser Console
1. Open browser console (F12 → Console tab)
2. Check for no errors (red text)
3. Check for no React/accessibility warnings

After testing, report back with findings.
```

## Step 6: Present Design Review Results

Present the design review results with clear prioritization:

1. **Summary**: Overall assessment and readiness
2. **What Works Well**: Positive observations
3. **Blockers**: Must fix before merge
4. **High Priority**: Should fix before merge
5. **Medium Priority**: Consider for follow-up
6. **Nitpicks**: Optional polish
7. **Checklists**: Accessibility, Responsive, Design System compliance

## Step 7: Optional - Create Design Tasks

If issues found, offer to create tracked tasks:

```bash
# Ask user
"Found [N] design issues. Would you like me to create Archon tasks for the critical ones?"

# If yes, create tasks:
# For each blocker/high issue:
manage_task(
  action="create",
  project_id="<project-id>",
  title="[Design] <issue-title>",
  description="**Component**: <component-name>
**Category**: <Accessibility/Responsive/Visual>
**Severity**: <Blocker/High>

**Issue**: <description>

**User Impact**: <how-this-affects-users>

**Fix**: <recommendation>

**WCAG Reference**: <if applicable>",
  status="todo",
  tags=["design", "ui-ux", "<severity>", "<category>"]
)
```

## Important Notes

- **Accessibility is not optional**: WCAG 2.1 AA is the baseline standard
- **Test across viewports**: Desktop, tablet, and mobile are all critical
- **Keyboard navigation**: All functionality must be keyboard accessible
- **Evidence-based**: Point to specific files and lines
- **User impact focus**: Explain how issues affect real users
- **Design system compliance**: Follow established patterns

## Example Output Format

```markdown
# Design Review: New Dashboard Components

## Summary
- **Components Reviewed**: 4 (DashboardCard, MetricWidget, FilterPanel, ActionButton)
- **Change Type**: New feature
- **Overall Assessment**: Needs changes before merge
- **Tested Viewports**: Desktop, Tablet, Mobile

## What Works Well ✅
- Excellent use of design system components
- Clear visual hierarchy with proper heading structure
- Smooth animations and micro-interactions
- Good empty state handling
- Consistent spacing throughout

## Blockers (MUST FIX) 🚨

### 1. Missing Keyboard Navigation for Filter Panel

- **Component**: `src/components/FilterPanel.tsx:45`
- **Category**: Accessibility
- **Issue**: Custom dropdown not keyboard accessible - cannot select options with keyboard
- **User Impact**: Keyboard users cannot filter data, blocking core functionality
- **WCAG Reference**: WCAG 2.1 AA 2.1.1 (Keyboard)
- **Recommendation**: Use Radix UI Select component which has built-in keyboard support:
  ```tsx
  import * as Select from '@radix-ui/react-select';

  <Select.Root>
    <Select.Trigger>...</Select.Trigger>
    <Select.Content>
      <Select.Item value="option1">Option 1</Select.Item>
    </Select.Content>
  </Select.Root>
  ```
- **Evidence**: Lines 45-89 implement custom dropdown without keyboard handlers

---

### 2. Insufficient Color Contrast on Metric Values

- **Component**: `src/components/MetricWidget.tsx:23`
- **Category**: Accessibility
- **Issue**: Gray text on light background has 3.2:1 contrast ratio (needs 4.5:1)
- **User Impact**: Users with visual impairments cannot read metric values
- **WCAG Reference**: WCAG 2.1 AA 1.4.3 (Contrast Minimum)
- **Recommendation**: Use darker gray from design system:
  ```tsx
  // Change from
  className="text-gray-400"

  // To
  className="text-gray-700"  // Meets 4.5:1 contrast
  ```
- **Evidence**: Line 23, DevTools shows 3.2:1 contrast ratio

## High Priority (SHOULD FIX) ⚠️

### 1. Mobile Layout Breaking at 375px Width

- **Component**: `src/components/DashboardCard.tsx:67`
- **Category**: Responsiveness
- **Issue**: Card content overflows horizontally on mobile viewport
- **User Impact**: Mobile users see horizontal scroll, poor UX
- **Recommendation**: Make card padding responsive:
  ```tsx
  // Change fixed padding
  className="p-6"

  // To responsive padding
  className="p-4 md:p-6"  // Less padding on mobile
  ```

## Medium Priority (CONSIDER) 💡

### 1. Loading State Could Be More Polished

- **Component**: `src/components/MetricWidget.tsx:150`
- **Category**: Visual Polish
- **Issue**: Simple spinner without skeleton loading
- **Recommendation**: Consider skeleton loading for better perceived performance

## Nitpicks (OPTIONAL) 🎨

- Nit: Card border radius is 8px, but buttons use 6px - consider consistency
- Nit: Hover transition slightly slow (300ms) - design system uses 200ms

## Accessibility Checklist
- [ ] Keyboard navigation (FAILED - Filter Panel not accessible)
- [x] Focus states visible on all interactive elements
- [x] Alt text present on all images
- [x] Form inputs have associated labels
- [ ] Color contrast meets WCAG 2.1 AA (FAILED - Metric values too light)
- [x] Semantic HTML used (headings, landmarks)
- [x] No keyboard traps

## Responsive Checklist
- [x] Desktop (1440px): Layout intact
- [x] Tablet (768px): Adapts gracefully
- [ ] Mobile (375px): FAILED - Card overflow
- [x] No horizontal scroll on desktop/tablet
- [x] Touch targets ≥44x44px on mobile
- [x] Text readable at all sizes

## Design System Checklist
- [x] Spacing consistent (8px increments)
- [x] Typography from design system scale
- [x] Colors from design system palette
- [x] Components from component library
- [ ] Border radii consistent (MINOR - card vs button mismatch)
- [x] Shadows/elevations appropriate

## Next Steps

1. **BEFORE MERGE**:
   - Fix keyboard navigation in Filter Panel (use Radix UI)
   - Fix color contrast in MetricWidget (use darker gray)
   - Fix mobile overflow in DashboardCard (responsive padding)

2. **FOLLOW-UP**:
   - Consider skeleton loading states
   - Standardize border radius across all components

3. **TESTING**: After fixes, retest with checklist above
```

## Integration with Development Workflow

After design review:

1. **Fix blockers and high-priority issues**: Address accessibility and responsive problems
2. **Retest manually**: Verify fixes with keyboard, different viewports
3. **Re-run design review** (optional): Confirm issues resolved
4. **Create follow-up tasks**: Track medium-priority improvements
5. **Update design system docs**: Document new patterns if applicable

## Remember

- **Accessibility first**: WCAG compliance is mandatory, not optional
- **Test, don't guess**: Verify issues by actually testing
- **Users matter**: Focus on real user impact
- **Design systems exist for a reason**: Follow established patterns
- **Mobile is not an afterthought**: Test mobile viewport thoroughly
- **Keyboard users exist**: All functionality must work with keyboard
