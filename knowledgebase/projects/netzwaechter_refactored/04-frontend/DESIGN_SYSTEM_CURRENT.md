# Design System - Current Implementation

**Created:** 2025-10-13
**Last Updated:** 2025-10-13

## Color System

### CSS Custom Properties (index.css lines 348-428)

#### Light Mode Colors
```css
:root {
  /* Primary Semantic Colors */
  --background: 0 0% 100%;              /* White */
  --foreground: 220 13% 10%;            /* Very dark blue-gray */

  /* Component Colors */
  --card: 0 0% 100%;                    /* White */
  --card-foreground: 220 13% 10%;
  --popover: 0 0% 100%;                 /* White */
  --popover-foreground: 220 13% 10%;

  /* Interaction Colors */
  --primary: 217 91% 60%;               /* Blue #4A90E2 */
  --primary-foreground: 0 0% 100%;      /* White */
  --secondary: 210 40% 96%;             /* Very light blue-gray */
  --secondary-foreground: 220 13% 15%;

  /* State Colors */
  --accent: 25 85% 55%;                 /* Orange (heating) */
  --accent-foreground: 0 0% 100%;
  --destructive: 0 84% 60%;             /* Red */
  --destructive-foreground: 0 0% 100%;
  --warning: 36 92% 50%;                /* Yellow-orange */
  --warning-foreground: 0 0% 0%;

  /* UI Elements */
  --muted: 210 20% 96%;                 /* Light gray */
  --muted-foreground: 215 16% 27%;      /* Dark gray */
  --border: 220 13% 90%;                /* Light gray border */
  --input: 220 13% 90%;                 /* Same as border */
  --ring: 217 91% 60%;                  /* Focus ring (primary) */
  --radius: 0.5rem;                     /* 8px border radius */

  /* Custom Grays */
  --gray-10: 0 0% 95.7%;                /* Almost white */
  --gray-20: 0 0% 87.8%;                /* Very light gray */
  --gray-50: 0 0% 55.3%;                /* Medium gray */
  --gray-80: 0 0% 22.4%;                /* Dark gray */
  --sidebar-bg: 210 20% 12%;            /* Dark blue sidebar */

  /* Semantic Colors */
  --error: 0 84% 60%;                   /* Red */
  --success: 160 84% 37%;               /* Green */

  /* Heating System Specific */
  --heating-orange: 25 85% 55%;
  --heating-red: 10 75% 50%;
  --energy-green: 120 60% 45%;
  --efficiency-blue: 210 75% 50%;

  /* Strawa Brand Colors */
  --strawa-blue: #0064A7;
  --strawa-gray: #f2f2f2;
}
```

#### Dark Mode Colors
```css
.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --muted: 240 3.7% 15.9%;
  --muted-foreground: 240 5% 64.9%;
  /* ... other dark mode overrides */
  --strawa-blue: #0064A7;               /* Same in dark mode */
  --strawa-gray: #2a2a2a;
}
```

### Tailwind Extended Colors (tailwind.config.js)

```javascript
colors: {
  // shadcn/ui semantic colors (using CSS vars)
  background: "hsl(var(--background))",
  foreground: "hsl(var(--foreground))",
  card: { ... },
  popover: { ... },
  primary: { ... },
  secondary: { ... },
  muted: { ... },
  accent: { ... },
  destructive: { ... },

  // Strawa brand colors
  'strawa-blue': '#0064A7',
  'strawa-gray': '#f2f2f2',

  // Custom gray scale
  'gray-10': 'hsl(0, 0%, 95.7%)',
  'gray-20': 'hsl(0, 0%, 87.8%)',
  'gray-50': 'hsl(0, 0%, 55.3%)',
  'gray-80': 'hsl(0, 0%, 22.4%)',

  // Heating system specific colors
  'heating-orange': 'hsl(25, 85%, 55%)',
  'heating-red': 'hsl(10, 75%, 50%)',
  'energy-green': 'hsl(120, 60%, 45%)',
  'efficiency-blue': 'hsl(210, 75%, 50%)',

  // Custom orange shade
  'orange-150': '#fde0bf',

  // Chart colors
  chart: {
    "1": "hsl(var(--chart-1))",
    "2": "hsl(var(--chart-2))",
    "3": "hsl(var(--chart-3))",
    "4": "hsl(var(--chart-4))",
    "5": "hsl(var(--chart-5))",
  }
}
```

### Color Usage Patterns

#### Status Colors
```typescript
// Efficiency classes (Dashboard.tsx)
const getEfficiencyClassColor = (effClass: string) => ({
  "A+": "bg-green-600 text-white",
  "A": "bg-green-500 text-white",
  "B": "bg-lime-400 text-black",
  "C": "bg-yellow-400 text-black",
  "D": "bg-orange-400 text-white",
  "E": "bg-orange-500 text-white",
  "F": "bg-red-500 text-white",
  "G": "bg-red-600 text-white",
  "H": "bg-red-800 text-white"
});
```

#### Temperature Status Colors
```css
/* Temperature analysis (index.css) */
.temp-value-critical {
  color: #dc2626 !important;           /* Red text */
}
.temp-value-warning {
  color: #ea580c !important;           /* Orange text */
}
.temp-value-normal {
  color: #16a34a !important;           /* Green text */
}
```

### Color Inconsistencies

1. **Multiple Gray Scales**:
   - Tailwind default grays (gray-50, gray-100, etc.)
   - Custom gray-10, gray-20, gray-50, gray-80
   - Semantic muted colors
   - All used interchangeably

2. **Blue Variations**:
   - Primary blue: `#4A90E2` (from CSS var)
   - Strawa blue: `#0064A7`
   - Efficiency blue: `hsl(210, 75%, 50%)`
   - Sidebar blue: `hsl(210, 20%, 12%)`
   - Used inconsistently across features

3. **Brand Colors**:
   - Strawa blue used in LayoutStrawa
   - Primary blue used elsewhere
   - No clear brand hierarchy

## Typography

### Font Family
```css
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont,
               'Segoe UI', 'Roboto', sans-serif;
}
```

### Font Sizes
No custom scale defined - using Tailwind defaults:
- `text-xs`: 0.75rem (12px)
- `text-sm`: 0.875rem (14px)
- `text-base`: 1rem (16px)
- `text-lg`: 1.125rem (18px)
- `text-xl`: 1.25rem (20px)
- `text-2xl`: 1.5rem (24px)

### Font Weights
Using Tailwind defaults:
- `font-normal`: 400
- `font-medium`: 500
- `font-semibold`: 600
- `font-bold`: 700

### Typography Patterns

#### Headings
```tsx
// Page titles
<h1 className="text-2xl font-semibold text-gray-80">
  KPI Dashboard
</h1>

// Section titles
<h2 className="text-xl font-semibold text-strawa-blue">
  Section Title
</h2>

// Card titles
<CardTitle className="text-lg font-semibold">
  Card Title
</CardTitle>
```

#### Body Text
```tsx
// Primary text
<p className="text-sm text-gray-80">
  Standard body text
</p>

// Secondary text
<p className="text-xs text-gray-50">
  Secondary information
</p>

// Muted text
<p className="text-sm text-muted-foreground">
  Muted description
</p>
```

#### Monospace (Temperature Values)
```tsx
<span className="font-mono text-xs">
  75.5°C
</span>
```

### Typography Inconsistencies

1. **Heading Hierarchy**:
   - No consistent h1-h6 usage
   - Size/weight combinations vary by page
   - Some pages use CardTitle, others use h2

2. **Label Sizes**:
   - Table headers: `text-xs`
   - Form labels: `text-sm` (default)
   - Card labels: varies

3. **Button Text**:
   - Usually `text-sm`
   - Some use `text-base`
   - Icon-only buttons: no text size

## Spacing System

### Using Tailwind Default Scale
```
0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10,
11, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
60, 64, 72, 80, 96
```

### Common Spacing Patterns

#### Card Padding
```tsx
// Standard card content
<CardContent className="p-6">

// Compact card
<CardContent className="p-3">

// No padding (full-width content)
<CardContent className="p-0">
```

#### Grid Gaps
```tsx
// KPI cards
<div className="grid gap-3">

// Dual column layout
<div className="flex gap-6">

// Table spacing
<div className="space-y-2">
```

#### Component Margins
```tsx
// Section spacing
<div className="mb-6">

// Small spacing
<div className="mt-2">

// Large spacing
<div className="mt-6">
```

### Spacing Inconsistencies

1. **Card Padding**:
   - Dashboard: `p-3` (compact)
   - Settings: `p-6` (standard)
   - UserManagement: `p-0` → `p-6` in content
   - No consistent pattern

2. **Grid Gaps**:
   - Dashboard cards: `gap-2` or `gap-3`
   - Feature layouts: `gap-6`
   - No semantic reasoning

3. **Page Padding**:
   - Some pages: `p-6`
   - LayoutStrawa content: `p-6 pt-[0px] pb-[0px] pl-[0px] pr-[0px]` (confusing override)
   - UserManagement: `p-6 pl-[10px] pr-[10px] pt-[10px] pb-[10px]`

## Border Radius

### Configuration (tailwind.config.js)
```javascript
borderRadius: {
  lg: "var(--radius)",              // 0.5rem = 8px
  md: "calc(var(--radius) - 2px)",  // 6px
  sm: "calc(var(--radius) - 4px)",  // 4px
}
```

### Usage Patterns
- Cards: `rounded-lg` (8px)
- Buttons: `rounded-md` (6px)
- Badges: `rounded` (4px) or `rounded-full`
- Inputs: `rounded-md` (6px)
- Dialogs: `rounded-lg` (8px)

### Border Radius Inconsistencies
- Some buttons use `rounded-lg`
- Some cards use `rounded-md`
- Dashboard type buttons: `border-radius: 6px` (inline style)
- No strict adherence to semantic usage

## Borders

### Border Widths
```javascript
borderWidth: {
  '0.5': '0.5px',  // Custom thin border
  // Default: 1, 2, 4, 8
}
```

### Border Colors
- Default: `border-gray-200` or `border`
- Strawa: `border-strawa-blue`
- Error: `border-red-500`
- Primary: `border-primary`

### Border Inconsistencies

1. **Table Borders**:
   - Portfolio table: No borders on cells
   - Temperature table: Borders explicitly removed via CSS
   - Some tables: Full borders

2. **Container Borders**:
   - Cards usually have borders
   - Some cards: `border-none` with shadow
   - Inconsistent application

## Shadows

### Using Tailwind Defaults
```
shadow-sm, shadow, shadow-md, shadow-lg, shadow-xl, shadow-2xl
```

### Common Usage
- Cards: `shadow-sm`
- Elevated buttons: `shadow-md`
- Dialogs: `shadow-xl`
- Hover states: `hover:shadow-md`

### Shadow Inconsistencies
- Most cards don't use shadows
- Buttons use shadow inconsistently
- No elevation system defined

## Icons

### Icon Libraries
1. **Lucide React** (primary)
   - Size: Usually `h-4 w-4` or `h-5 w-5`
   - Used in buttons, navigation, status indicators

2. **Heroicons** (secondary)
   - Size: Usually `h-4 w-4` or `h-5 w-5`
   - Used in Dashboard and some features

### Icon Patterns
```tsx
// Button with icon
<Button>
  <PlusIcon className="h-4 w-4 mr-2" />
  Add Item
</Button>

// Icon-only button
<Button size="icon">
  <Settings className="h-4 w-4" />
</Button>

// Navigation icon
<item.icon className="w-5 h-5" />
```

### Icon Inconsistencies
- Two icon libraries used (Lucide + Heroicons)
- Inconsistent sizing (some h-3, some h-4, some h-5, some h-6)
- No icon component wrapper for consistent styling

## Animation

### Tailwind Animations
```javascript
plugins: [
  require("tailwindcss-animate")
]
```

### Custom Animations (index.css)

#### 1. Pulse Critical
```css
@keyframes pulse-red {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(220, 38, 38, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
}
.pulse-critical { animation: pulse-red 2s infinite; }
```
Used for critical map markers.

#### 2. Fade In
```css
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in { animation: fade-in 0.5s ease-out forwards; }
```
Used for page transitions.

#### 3. Typewriter Effect
```css
@keyframes typewriter-word {
  0% { opacity: 0; }
  100% { opacity: 1; }
}
.animate-typewriter {
  animation-name: typewriter-word;
  animation-duration: 0.6s;
  animation-timing-function: ease-out;
  animation-fill-mode: forwards;
}
```
Used in LayoutStrawa "Wir leben Effizienz" slogan.

### Animation Inconsistencies
- Only a few custom animations defined
- No consistent transition timing
- Some components use inline transitions
- Loading states use default `animate-spin`

## Responsive Design

### Breakpoints (Tailwind defaults)
```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Common Responsive Patterns

#### Grid Layouts
```tsx
// KPI cards
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">

// Two-column
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
```

#### Sidebar Behavior
```tsx
// Desktop: expanded, Mobile: collapsed
const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
useEffect(() => {
  const isMobile = window.innerWidth < 768;
  setSidebarCollapsed(isMobile);
}, []);
```

#### Text Sizing
```tsx
// Responsive heading
<h1 className="text-xl md:text-2xl lg:text-3xl">
```

### Responsive Inconsistencies
- Sidebar: Some pages have responsive sidebars, others don't
- Tables: Most tables don't adapt well to mobile
- Forms: No mobile-optimized layouts
- Grid breakpoints vary by page

## Z-Index Scale

### Current Usage (no defined scale)
- Dialogs: `z-[10000]` (inline style in LayoutStrawa)
- Dialog overlay: `z-50` (from shadcn)
- Dialog content: `z-51` (from index.css override)
- Sidebar toggle: `z-10`, `z-20`, `z-30` (varies)
- Mobile overlay: `z-20`

### Z-Index Problems
- No semantic z-index scale
- Hardcoded values like `10000`
- Risk of z-index wars
- No documentation of layers

## Theme System

### Dark Mode Support
- Dark mode classes defined in index.css
- `dark:` variant used sparingly
- No dark mode toggle implemented
- Most components only styled for light mode

### Current Theme Approach
1. CSS variables for semantic colors
2. Tailwind classes for utilities
3. Inline styles for specific cases (bad practice)
4. Component-level style overrides (in many places)

## Design Tokens Summary

### Well-Defined
- Base colors (CSS variables)
- Tailwind spacing scale
- Border radius system
- Icon sizes (mostly)

### Poorly Defined
- Typography scale (using defaults)
- Z-index layering
- Shadow elevation
- Animation timing
- Responsive patterns

### Missing
- Named shadow levels
- Transition duration tokens
- Layout width constraints
- Container max-widths
- Grid column definitions

## Custom CSS Utilities (index.css @layer utilities)

```css
.text-gray-10, .bg-gray-10
.text-gray-20, .bg-gray-20
.text-gray-50, .bg-gray-50
.text-gray-80, .bg-gray-80
.bg-sidebar
.text-error, .bg-error
.text-warning, .bg-warning
.text-success, .bg-success
.border-gray-20
.hover\:bg-gray-600:hover
.text-heating-orange, .bg-heating-orange
.text-energy-green, .bg-energy-green
.text-efficiency-blue, .bg-efficiency-blue
.bg-strawa-gray, .bg-strawa-blue
.border-strawa-blue, .text-strawa-blue
.text-balance

/* Grafana-specific utilities */
.grafana-container, .grafana-iframe
.grafana-split-container, .grafana-panel-*
.grafana-tab-*, .grafana-counter-button-*
.grafana-object-selection, .grafana-status-badge
```

Many utilities are feature-specific and should be componentized.
