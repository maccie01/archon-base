# UI Inconsistencies & Problems

**Created:** 2025-10-13
**Last Updated:** 2025-10-13

## Critical Issues

### 1. Dialog Overlay Transparency Bug
**Location**: All Dialog components
**Problem**: Dialog overlays were transparent, showing content behind
**Current Fix**: Global CSS override in `index.css` (lines 931-947)

```css
/* HACK: Force ALL dialog overlays to be opaque */
[data-radix-dialog-overlay],
[data-radix-alert-dialog-overlay],
[data-radix-sheet-overlay] {
  background-color: rgba(0, 0, 0, 0.8) !important;
  backdrop-filter: blur(2px) !important;
}
```

**Why It's Bad**:
- Uses `!important` overrides
- Global CSS instead of component-level fix
- Treats symptom, not root cause
- May break future Radix UI updates

**Better Solution**: Fix Dialog component styling or use custom overlay component

---

### 2. Toast Opacity Bug
**Location**: All Toast notifications
**Problem**: Toast notifications were transparent/unreadable
**Current Fix**: Global CSS override in `index.css` (lines 949-967)

```css
/* HACK: Force toast notifications to be opaque */
[data-radix-toast-viewport] li[data-radix-collection-item] {
  background-color: white !important;
  opacity: 1 !important;
}
```

**Why It's Bad**:
- More `!important` hacks
- Global CSS targeting Radix internals
- Fragile selectors
- Will break with Radix updates

**Better Solution**: Fix Toast component base styles

---

## Tab Styling Inconsistencies

### Problem 1: UserManagement Tab Overrides
**Location**: `src/features/users/pages/UserManagement.tsx`
**Problem**: Inline `<style>` tags with massive CSS overrides (lines 142-202)

```tsx
<style>{`
  /* 60+ lines of CSS overrides with !important */
  div[role="tablist"] {
    background-color: #f3f4f6 !important;
  }
  button[data-state="active"] {
    background-color: #ffffff !important;
    color: #2563eb !important;
  }
  /* ... 50+ more lines */
`}</style>
```

**Why It's Bad**:
- Inline styles pollute component
- 200+ lines of component-level CSS
- Uses !important everywhere
- Duplicates global CSS
- Hard to maintain
- Doesn't follow design system

**Issues**:
1. Active tab: white background (#ffffff)
2. Inactive tab: gray background (#f3f4f6)
3. But global CSS says something else
4. Tab bar: gray background
5. Styling fights with index.css (lines 969-1043)

### Problem 2: Global Tab Styling
**Location**: `index.css` (lines 969-1043)
**Problem**: Complex global tab styling rules

```css
/* Modern Tab Navigation Styles - Strawa Design */
.modern-tab-nav { ... }
.modern-tab-button { ... }

/* UserManagement Tab Overrides - Stronger selectors */
button[data-state="active"][value="users"] { ... }
button[data-state="active"][value="mandates"] { ... }

/* Ensure tabs have proper Strawa styling */
[role="tablist"] { ... }
[role="tab"] { ... }
[role="tab"][data-state="active"] { ... }
```

**Why It's Bad**:
- Global CSS for component-specific styling
- Specificity wars
- Hard to understand what wins
- Strawa branding mixed with component styles
- No single source of truth

### Problem 3: Grafana Tab Styling
**Location**: `index.css` (lines 661-680)
**Problem**: Feature-specific tab styling in global CSS

```css
/* Grafana Tab Styling (like screenshot) */
.grafana-tab-container { ... }
.grafana-tab-base { ... }
.grafana-tab-active { ... }
.grafana-tab-inactive { ... }
```

**Why It's Bad**:
- Feature CSS in global file
- Not reusable
- Duplicates other tab styles
- Should be in Grafana feature

**Tab Styling Summary**:
- 3 different tab styling systems
- Active tabs vary by context:
  - UserManagement: white bg
  - Strawa tabs: gray bg
  - Grafana tabs: blue underline
- No consistent tab component
- Impossible to know which styles apply where

---

## Color Inconsistencies

### 1. Multiple Gray Scales
**Problem**: Three different gray systems used interchangeably

```typescript
// System 1: Custom grays
'gray-10': 'hsl(0, 0%, 95.7%)'
'gray-20': 'hsl(0, 0%, 87.8%)'
'gray-50': 'hsl(0, 0%, 55.3%)'
'gray-80': 'hsl(0, 0%, 22.4%)'

// System 2: Tailwind grays
gray-50, gray-100, gray-200, gray-300, gray-400,
gray-500, gray-600, gray-700, gray-800, gray-900

// System 3: Semantic colors
--muted: 210 20% 96%
--muted-foreground: 215 16% 27%
```

**Usage**:
- Dashboard: Uses gray-50, gray-80, gray-10
- UserManagement: Uses gray-200, gray-50, gray-100
- Forms: Uses muted, muted-foreground
- No consistent pattern

**Impact**:
- Same gray names, different values
- Hard to maintain consistency
- Unclear when to use which
- Visual inconsistency across pages

### 2. Multiple Blue Variations
**Problem**: 5 different blues with unclear usage

```typescript
// 1. Primary blue (design system)
--primary: 217 91% 60%  // #4A90E2

// 2. Strawa brand blue
'strawa-blue': '#0064A7'

// 3. Efficiency blue
'efficiency-blue': 'hsl(210, 75%, 50%)'

// 4. Sidebar blue
--sidebar-bg: 210 20% 12%  // Dark navy

// 5. Temperature blue
'text-blue-600', 'bg-blue-100', 'bg-blue-50'
```

**Usage**:
- LayoutStrawa: Uses strawa-blue (#0064A7)
- Layout (cockpit): Uses sidebar-bg (dark navy)
- Buttons: Use primary (lighter blue)
- Efficiency: Uses efficiency-blue
- Temperature values: Use text-blue-600

**Impact**:
- Brand inconsistency
- No clear blue hierarchy
- Users see different blues on every page
- Confusing which blue is "the" blue

### 3. Hardcoded Colors
**Problem**: Colors hardcoded directly in components

```tsx
// Dashboard.tsx
className="text-blue-600"
style={{ color: '#1e40af' }}

// NetworkMonitor.tsx
backgroundColor: '#dbeafe'

// UserManagement inline styles
background-color: #f3f4f6 !important;
color: #2563eb !important;
```

**Impact**:
- Can't change theme globally
- Hard to find all uses
- Doesn't use design system
- Breaks dark mode

---

## Spacing Inconsistencies

### 1. Padding Override Pattern
**Problem**: Bizarre padding overrides throughout

```tsx
// Pattern 1: LayoutStrawa content
<div className="p-6 pt-[0px] pb-[0px] pl-[0px] pr-[0px]">
  {/* Why not just px-6? */}
</div>

// Pattern 2: UserManagement
<div className="p-6 pl-[10px] pr-[10px] pt-[10px] pb-[10px]">
  {/* This overrides p-6 with smaller values... */}
</div>

// Pattern 3: Normal usage
<div className="p-6">
  {/* Clean and simple */}
</div>
```

**Why It's Bad**:
- Confusing override pattern
- Mixing units (rem vs px)
- `pt-[0px]` is verbose for `pt-0`
- Hard to understand intent
- Inconsistent across pages

**Impact**:
- Same "p-6" class looks different
- Hard to predict actual spacing
- Confusing for developers

### 2. Card Padding Variations
**Problem**: No consistent card padding pattern

```tsx
// Dashboard KPI cards
<CardContent className="p-3">

// Settings cards
<CardContent className="p-6">

// UserManagement card
<CardContent className="p-0">
  <div className="p-6">  {/* padding inside */}
  </div>
</CardContent>

// Logbook cards
<CardContent>  {/* default padding */}
```

**Impact**:
- Cards look different sizes
- No visual hierarchy
- Confusing spacing relationships

### 3. Grid Gaps
**Problem**: Inconsistent gap sizes with no pattern

```tsx
// Dashboard KPIs
<div className="grid gap-3">  // 12px

// Two-column layouts
<div className="flex gap-6">  // 24px

// Settings sections
<div className="grid gap-4">  // 16px

// Table spacing
<div className="space-y-2">  // 8px
```

**Impact**:
- No spacing scale adhered to
- Visual inconsistency
- No semantic reasoning

---

## Typography Inconsistencies

### 1. Heading Hierarchy
**Problem**: No consistent heading usage

```tsx
// Dashboard
<h1 className="text-2xl font-semibold text-gray-80">
  KPI Dashboard
</h1>

// NetworkMonitor - using CardTitle instead
<CardTitle>
  Netzwächter
</CardTitle>

// UserManagement - no h1, just CardTitle
<CardTitle>Benutzerverwaltung</CardTitle>

// Settings - direct div
<div className="text-xl font-bold">
  System-Setup
</div>
```

**Impact**:
- Accessibility issues (no h1 on some pages)
- Inconsistent visual hierarchy
- Screen readers confused
- Hard to style globally

### 2. Label Sizes
**Problem**: Form labels vary by context

```tsx
// Table headers
<div className="text-xs">Objekt</div>

// Form labels
<Label>Email</Label>  {/* text-sm default */}

// Card labels
<p className="text-xs font-medium text-gray-50">
  Kritische Anlagen
</p>

// Section labels
<div className="text-sm font-medium">
  Database Settings
</div>
```

**Impact**:
- No clear label hierarchy
- Hard to scan forms/tables
- Inconsistent emphasis

### 3. Font Weight Usage
**Problem**: Inconsistent weight patterns

```tsx
// Sometimes normal text is medium
<span className="font-medium">

// Sometimes bold is semibold
<h2 className="font-semibold">

// Object names use 500 weight
<td className="font-medium">

// Table headers use medium
<th className="font-medium">
```

**Impact**:
- No weight hierarchy
- Everything looks "kinda bold"
- Hard to establish emphasis

---

## Border Inconsistencies

### 1. Table Border Chaos
**Problem**: Each table has different border treatment

```tsx
// Dashboard Portfolio Table
// - Uses custom grid (not <table>)
// - No borders on cells
// - Blue header background
// - Border on container only

// NetworkMonitor Table
// - Uses temp-analysis-table class
// - CSS explicitly removes ALL borders (index.css line 118-133)
border: none !important;

// UserManagement Tables
// - Native HTML <table>
// - Has borders on rows
// - Header on white background

// Logbook Tables
// - Uses shadcn Table component
// - Default borders
// - Border on every cell
```

**Why It's Bad**:
- No consistency between tables
- Users see 4 different table styles
- Hard to know "correct" pattern
- CSS fights with itself

### 2. Card Borders
**Problem**: Inconsistent card border usage

```tsx
// Most cards have borders (default)
<Card>  {/* has border */}

// Some cards explicitly remove borders
<Card className="border-none shadow-sm">

// Some use shadows instead
<Card className="shadow-lg">

// Dashboard KPI cards
<Card>  {/* border + hover shadow */}
```

**Impact**:
- Visual inconsistency
- No elevation system
- Can't tell card importance

### 3. Container Borders
**Problem**: Temperature analysis has special border rules

```css
/* index.css lines 224-243 */
div[class*="bg-red-100"] {
  border: 0.5px solid #fecaca !important;
}
div[class*="bg-orange-100"] {
  border: 0.5px solid #fed7aa !important;
}
/* etc */
```

**Why It's Bad**:
- Global CSS for feature-specific styling
- Matches on class substring (fragile)
- Uses !important
- Affects ALL elements with those classes

---

## Button Inconsistencies

### 1. Button Variants
**Problem**: Same action uses different variants

```tsx
// "Create" action
<Button variant="default">Create User</Button>  // Settings
<Button>Add Entry</Button>  // Logbook (default)
<Button variant="outline">Add Task</Button>  // Logbook

// "Cancel" action
<Button variant="outline">Cancel</Button>  // Most dialogs
<Button variant="ghost">Cancel</Button>  // Some dialogs
<Button variant="secondary">Cancel</Button>  // SystemSettings

// "Delete" action
<Button variant="destructive">Delete</Button>  // Some places
<Button variant="outline" className="text-red-600">
  Delete
</Button>  // Other places
```

**Impact**:
- No predictable button hierarchy
- Users can't learn button meanings
- Inconsistent emphasis

### 2. Button Sizes
**Problem**: Inconsistent size usage

```tsx
// Header buttons
<Button size="sm">

// Dialog buttons
<Button>  {/* default = md */}

// Table action buttons
<Button size="sm">
<Button size="icon">  {/* sometimes */}

// Sidebar toggle
<button className="p-1.5">  {/* custom */}
```

**Impact**:
- Buttons look different sizes
- No size hierarchy
- Touch targets inconsistent

### 3. Button Icon Patterns
**Problem**: Icons placed inconsistently

```tsx
// Icon before text
<Button>
  <PlusIcon className="h-4 w-4 mr-2" />
  Add
</Button>

// Icon after text
<Button>
  Export
  <DownloadIcon className="h-4 w-4 ml-2" />
</Button>

// Icon only (different sizes)
<Button size="icon">
  <Settings className="h-4 w-4" />  {/* size-icon */}
</Button>
<button>
  <Settings className="h-5 w-5" />  {/* custom button */}
</button>
```

**Impact**:
- No icon placement convention
- Inconsistent icon sizes
- Hard to scan buttons

---

## Table Inconsistencies

### 1. Three Different Table Implementations

**Implementation 1: Custom Grid (Dashboard)**
```tsx
<div className="grid ... h-10" style={{ gridTemplateColumns: '...' }}>
  {/* Custom grid layout, no <table> */}
</div>
```
- Fixed column widths
- Blue header background
- No cell borders
- Fixed height rows

**Implementation 2: HTML Table + Border Removal (NetworkMonitor)**
```tsx
<table className="temp-analysis-table">
  {/* Native table with CSS to remove borders */}
</table>
```
```css
/* index.css */
.temp-analysis-table * {
  border: none !important;
}
```
- Native table structure
- All borders removed via CSS
- Custom cell styling
- Temperature color classes

**Implementation 3: shadcn Table Component (UserManagement, Logbook)**
```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>...</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>...</TableCell>
    </TableRow>
  </TableBody>
</Table>
```
- Uses shadcn/ui components
- Default borders on all cells
- Hover states
- Responsive (kinda)

**Why It's Bad**:
- Users see 3 completely different table styles
- No consistent interaction patterns
- Hard to maintain
- Can't reuse table components

### 2. Table Header Styling
**Problem**: Every table header looks different

```tsx
// Dashboard: Blue background
<div className="bg-blue-100">

// NetworkMonitor: White background (with override CSS)
<thead className="bg-white">

// UserManagement: Gray-200 background (forced to white via inline styles)
<TableRow className="bg-gray-200">  {/* overridden to white */}

// Logbook: Default (muted background)
<TableHeader>  {/* uses theme default */}
```

**Impact**:
- No visual consistency
- Can't tell it's the same app
- Confusing for users

### 3. Table Sorting
**Problem**: Only Dashboard has sorting, but no visual indicator system

```tsx
// Dashboard implements sorting
{sortConfig?.key === 'name' ? (
  sortConfig.direction === 'asc' ?
    <ArrowUpIcon className="h-3 w-3" /> :
    <ArrowDownIcon className="h-3 w-3" />
) : (
  <ArrowUpDownIcon className="h-3 w-3 opacity-40" />
)}

// Other tables: No sorting
// No shared sorting component
// No consistent sort indicator
```

**Impact**:
- Only one table is sortable
- No reusable sorting component
- Users expect sorting everywhere

---

## Form Inconsistencies

### 1. Input Field Styling
**Problem**: Inputs look different in different contexts

```tsx
// Standard form input
<Input type="text" placeholder="Enter name" />

// Search input with icon
<div className="relative">
  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2" />
  <Input className="pl-10" placeholder="Search..." />
</div>

// Settings input (full width)
<Input className="w-full" />

// Dialog input
<FormControl>
  <Input {...field} />
</FormControl>
```

**Impact**:
- Inconsistent input appearance
- Icon placement varies
- No input component wrapper

### 2. Label Placement
**Problem**: No consistent label pattern

```tsx
// Above input (standard)
<FormLabel>Email</FormLabel>
<FormControl>
  <Input />
</FormControl>

// Inline (checkbox)
<div className="flex items-center space-x-2">
  <Checkbox />
  <Label>Remember me</Label>
</div>

// To the left (settings)
<div className="grid grid-cols-2">
  <Label>Port</Label>
  <Input />
</div>
```

**Impact**:
- No consistent form layout
- Hard to scan forms
- Accessibility issues

### 3. Validation Messages
**Problem**: Error messages styled differently

```tsx
// FormMessage component (red text)
<FormMessage />

// Custom error (with alert icon)
<div className="text-red-600 text-sm flex items-center">
  <AlertTriangle className="h-4 w-4 mr-2" />
  Error message
</div>

// Toast notification
toast({
  variant: "destructive",
  title: "Error",
  description: "Something went wrong"
});
```

**Impact**:
- No consistent error pattern
- Users miss errors
- Accessibility issues

---

## Navigation Inconsistencies

### 1. Two Different Sidebars
**Problem**: Strawa sidebar vs Cockpit sidebar look completely different

**Strawa Sidebar**:
- Blue background (#0064A7)
- Logo + "Wir leben Effizienz"
- 8 navigation items (max)
- Admin section at bottom
- Collapsible width: 60px → 240px

**Cockpit Sidebar**:
- Dark navy background
- Logo + "heatcare"
- 15+ navigation items (permissions-based)
- User profile at bottom
- Collapsible width: 64px → 240px

**Impact**:
- Completely different UX based on URL parameter
- Users confused by mode switching
- No visual continuity
- Two codebases to maintain

### 2. Navigation Icons
**Problem**: Icons used inconsistently

```tsx
// Some items use Lucide icons
<BarChart3 className="h-5 w-5" />

// Some use Heroicons
<BuildingOfficeIcon className="h-5 w-5" />

// Some use custom SVG
<svg width="20" height="20" fill="none">...</svg>

// Size varies: h-4, h-5, h-6
```

**Impact**:
- Visual inconsistency
- Mixed icon libraries
- Size inconsistency

### 3. Active State Styling
**Problem**: Active navigation items look different per layout

```tsx
// Strawa: Gray background
className="bg-gray-200 text-[#21496E]"

// Cockpit: Primary blue background
className="bg-primary text-white"

// Different from tabs (white background)
// Different from buttons (primary background)
```

**Impact**:
- No consistent active state
- Users can't tell where they are
- Visual confusion

---

## Modal/Dialog Inconsistencies

### 1. Dialog Widths
**Problem**: Dialogs have inconsistent max-widths

```tsx
// User form dialog
<DialogContent className="sm:max-w-[425px]">

// User settings modal
<DialogContent className="sm:max-w-[400px]">

// Export dialog
<DialogContent className="max-w-2xl">

// Object group dialog
<DialogContent>  {/* default */}
```

**Impact**:
- Dialogs different sizes
- No semantic sizing
- Inconsistent UX

### 2. Dialog Headers
**Problem**: Header structure varies

```tsx
// With description
<DialogHeader>
  <DialogTitle>Create User</DialogTitle>
  <DialogDescription>
    Fill in the details below
  </DialogDescription>
</DialogHeader>

// Without description
<DialogHeader>
  <DialogTitle>Confirm</DialogTitle>
</DialogHeader>

// With custom styling
<DialogHeader className="pb-4">
  <DialogTitle className="text-xl">
    Settings
  </DialogTitle>
</DialogHeader>
```

**Impact**:
- Inconsistent dialog appearance
- No standard dialog pattern
- Some dialogs missing descriptions (accessibility)

### 3. Dialog Footer Buttons
**Problem**: Button order and variants differ

```tsx
// Pattern 1: Outline + Primary
<DialogFooter>
  <Button variant="outline" onClick={close}>Cancel</Button>
  <Button onClick={save}>Save</Button>
</DialogFooter>

// Pattern 2: Ghost + Default
<DialogFooter>
  <Button variant="ghost" onClick={close}>Cancel</Button>
  <Button variant="default" onClick={save}>Save</Button>
</DialogFooter>

// Pattern 3: Single button
<DialogFooter>
  <Button onClick={close}>Close</Button>
</DialogFooter>
```

**Impact**:
- No consistent dialog pattern
- Users can't predict button hierarchy
- Confusing which is primary action

---

## Icon Inconsistencies

### 1. Two Icon Libraries
**Problem**: Using both Lucide React and Heroicons

```tsx
// Lucide React (primary)
import { Settings, Users, BarChart3 } from "lucide-react";

// Heroicons (secondary)
import { BuildingOfficeIcon, BoltIcon } from "@heroicons/react/24/outline";
```

**Why Use Both?**:
- No clear reason
- Increases bundle size
- Visual style differences
- No consistent icon set

### 2. Icon Sizes
**Problem**: Same icon, different sizes across app

```tsx
// Dashboard KPI icons
<BoltIcon className="h-4 w-4" />

// Navigation icons
<Settings className="h-5 w-5" />

// Button icons
<PlusIcon className="h-4 w-4 mr-2" />

// Large display icons
<Shield className="h-16 w-16" />

// Sidebar icons (mobile)
<item.icon className="w-6 h-6" />  {/* Mobile */}
<item.icon className="w-5 h-5" />  {/* Desktop */}
```

**Impact**:
- No consistent icon sizing system
- Visual inconsistency
- Hard to establish hierarchy

### 3. Icon Colors
**Problem**: Icon colors inconsistent with context

```tsx
// Primary color
<Settings className="text-primary" />

// Contextual colors
<AlertTriangle className="text-red-600" />
<Check className="text-green-600" />

// Gray
<Settings className="text-gray-300" />

// Inherit
<PlusIcon className="h-4 w-4" />  {/* inherits text color */}
```

**Impact**:
- No icon color system
- Inconsistent emphasis
- Hard to maintain

---

## Animation Inconsistencies

### 1. Loading States
**Problem**: Different loading patterns

```tsx
// Spinner (Dashboard, loading KPIs)
<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />

// Skeleton (Dashboard, loading cards)
<Card className="animate-pulse">
  <div className="h-3 bg-gray-20 rounded w-1/2"></div>
</Card>

// Text (App.tsx main loading)
<p className="text-lg font-medium text-gray-700">Loading...</p>

// No indicator (some pages)
{/* Just shows empty state */}
```

**Impact**:
- No consistent loading UX
- Some pages look broken
- Users confused about state

### 2. Transition Timing
**Problem**: No consistent transition duration

```tsx
// Sidebar transition
className="transition-all duration-300"

// Tab transition
className="transition-colors duration-200"

// Button hover
className="transition-colors"  {/* default */}

// Hover effects
className="hover:opacity-80 cursor-pointer transition-opacity"
```

**Impact**:
- Inconsistent animation feel
- No timing system
- Some animations feel jerky

### 3. Hover States
**Problem**: Hover effects vary wildly

```tsx
// Card hover (Dashboard)
className="cursor-pointer hover:shadow-md transition-shadow"

// Row hover (Tables)
className="hover:bg-gray-5"  {/* Custom gray */}
className="hover:bg-gray-100"  {/* Tailwind gray */}
className="hover:bg-strawa-gray"  {/* Brand gray */}

// Button hover (default)
{/* Built into button component */}

// Link hover (Navigation)
className="hover:bg-gray-600"  {/* Sidebar */}
className="hover:bg-white/10"  {/* LayoutStrawa */}
```

**Impact**:
- No predictable hover pattern
- Inconsistent feedback
- Users can't tell what's clickable

---

## Responsive Design Problems

### 1. Tables Not Mobile-Friendly
**Problem**: All tables break on mobile

```tsx
// Dashboard Portfolio Table
<div style={{ gridTemplateColumns: '1fr 120px 160px 140px 140px 90px 90px 60px' }}>
  {/* Fixed widths, horizontal scroll on mobile */}
</div>

// No alternative mobile view
// No card/list alternative
// Headers stay visible (can't hide columns)
```

**Impact**:
- Terrible mobile experience
- Users can't use tables on phones
- Horizontal scroll hell

### 2. Inconsistent Breakpoints
**Problem**: Components use different breakpoints

```tsx
// Most components
<div className="grid-cols-1 md:grid-cols-2 lg:grid-cols-4">

// Some use sm
<div className="sm:max-w-[425px]">

// Some skip md and go straight to lg
<div className="grid-cols-1 lg:grid-cols-2">

// Sidebar breakpoint: 768px (md)
const isMobile = window.innerWidth < 768;
```

**Impact**:
- No consistent responsive pattern
- Layouts break at different points
- Confusing responsive behavior

### 3. Mobile Navigation
**Problem**: Sidebars don't work well on mobile

**Strawa Sidebar**:
- Always renders
- No mobile optimization
- Overlays content when open

**Cockpit Sidebar**:
- Collapses on mobile
- Fixed positioning when expanded
- Backdrop overlay
- Still takes up space when collapsed

**Impact**:
- Poor mobile UX
- Sidebar blocks content
- No mobile-first approach

---

## Component Duplication

### 1. Multiple Table Implementations
- Dashboard: Custom grid layout
- NetworkMonitor: Custom table with CSS overrides
- UserManagement: shadcn Table
- No shared table component

### 2. Multiple Tab Styles
- UserManagement: Inline styles
- LayoutStrawa: Strawa-branded tabs
- Grafana: Custom Grafana tabs
- No shared tab component

### 3. Multiple Button Patterns
- shadcn Button component
- Custom sidebar buttons
- Native `<button>` with custom classes
- No consistent usage

---

## CSS Architecture Problems

### 1. Too Many Global Styles
**Location**: `index.css` (1061 lines)

Contains:
- Component-specific styles (Grafana, tables, tabs)
- Feature-specific styles (temperature, network monitor)
- Print styles
- Theme colors
- Animations
- Utility classes
- HACK fixes with !important

**Why It's Bad**:
- Hard to maintain
- Unclear what's used where
- Specificity conflicts
- Can't tree-shake unused CSS

### 2. Inline Styles Abuse
**Examples**:
```tsx
// UserManagement (200+ lines of inline CSS)
<style>{`...`}</style>

// Dashboard (inline grid template)
style={{ gridTemplateColumns: '...' }}

// LayoutStrawa (z-index)
style={{ zIndex: 10000 }}

// Temperature colors
style={{ color: '#1e40af' }}
```

**Why It's Bad**:
- Can't reuse styles
- Hard to maintain
- Breaks consistency
- Can't theme

### 3. CSS Class Soup
**Example from UserManagement**:
```tsx
<TabsTrigger
  value="users"
  className="inline-flex items-center justify-center whitespace-nowrap rounded-none border-b-2 border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-500 ring-offset-background transition-all hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:border-primary data-[state=active]:text-primary data-[state=active]:bg-white data-[state=active]:shadow-none"
>
```

**Why It's Bad**:
- 25+ utility classes
- Unreadable
- Hard to maintain
- Should be extracted to component

---

## Accessibility Issues

### 1. Inconsistent Heading Hierarchy
- Some pages have h1
- Some pages skip straight to h2
- Some pages use only CardTitle
- Screen readers confused

### 2. Missing ARIA Labels
- Icon-only buttons sometimes missing labels
- Custom interactive elements missing roles
- Tables missing proper structure

### 3. Color Contrast
- Some gray text combinations fail WCAG AA
- Temperature colors may fail contrast
- Muted text too muted

### 4. Focus Indicators
- Some custom buttons missing focus styles
- Sidebar focus states unclear
- Tab focus not always visible

---

## Summary of Major Issues

### Critical (Fix Immediately)
1. Dialog overlay transparency hack
2. Toast opacity hack
3. Tables not mobile-responsive
4. Accessibility issues (heading hierarchy, ARIA)

### High Priority (Fix Soon)
1. Tab styling wars (3 systems)
2. Color inconsistencies (3 gray scales, 5 blues)
3. Table implementation chaos (3 different types)
4. Global CSS bloat (1061 lines)

### Medium Priority (Fix Eventually)
1. Button variant inconsistencies
2. Spacing override patterns
3. Typography hierarchy
4. Icon library duplication
5. Form layout inconsistencies
6. Navigation differences (2 sidebars)

### Low Priority (Nice to Have)
1. Animation timing consistency
2. Hover state variations
3. Border radius inconsistencies
4. Shadow elevation system
5. Z-index scale

---

## Root Causes

### Why These Issues Exist
1. **No Design System**: Components built without consistent patterns
2. **Two Layouts**: Strawa vs Cockpit split creates duplication
3. **Global CSS Abuse**: Too much styling in global file
4. **Component Inconsistency**: Multiple implementations of same component
5. **Inline Style Hacks**: Quick fixes without refactoring
6. **No Code Review**: Inconsistencies not caught
7. **No Documentation**: No style guide to follow
8. **Technical Debt**: Fixing symptoms instead of root causes

### How to Fix
1. Create unified design system
2. Componentize everything
3. Remove global CSS hacks
4. Consolidate duplicate components
5. Mobile-first redesign
6. Accessibility audit
7. Code review process
8. Living style guide
