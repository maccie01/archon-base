# Layout Patterns & Responsive Design

**Created:** 2025-10-13
**Last Updated:** 2025-10-13

## Overview
The Netzwächter application uses two distinct layout systems based on UI mode, with different navigation and structure patterns.

## Layout Modes

### 1. Strawa Layout (Default)
**File**: `src/features/auth/pages/LayoutStrawa.tsx`
**Trigger**: All URLs without `?ui=cockpit` parameter
**Target Audience**: End users, standard operations

#### Structure
```
┌─────────────────────────────────────────┐
│ Collapsible Sidebar                     │
│ - Strawa Branding                       │
│ - "Wir leben Effizienz"                 │
│ - Navigation Items                      │
│ - Admin Section (conditional)           │
│ - User Profile                          │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ Header                                  │
│ - Dynamic Title | Subtitle              │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ Main Content Area                       │
│ - Rendered component based on active    │
│   menu item                             │
│ - Padding: p-6 pt-[0px] pb-[0px]       │
│   pl-[0px] pr-[0px] (override pattern)  │
└─────────────────────────────────────────┘
```

#### Navigation Items
1. KPI Dashboard (activeMenuItem: 0)
2. Netzwächter (activeMenuItem: 1)
3. Objekt-Karte (activeMenuItem: 2)
4. Klassifizierung (activeMenuItem: 3)
5. Objekt Monitor (activeMenuItem: 4)
6. Logbuch (activeMenuItem: 8)
7. Meine Benutzer (activeMenuItem: 6) - conditional

#### Admin Section
- System-Setup (activeMenuItem: 5)
- Benutzerverwaltung (activeMenuItem: 7)
- Only visible for admin role

#### Sidebar Behavior
```typescript
// Strawa sidebar styling
width: sidebarCollapsed ? 'w-12' : 'w-60'
background: bg-strawa-blue (#0064A7)
border-strawa-blue
```

#### Header System
Dynamic header content changes based on active menu item:
```typescript
const getHeaderContent = () => {
  switch (activeMenuItem) {
    case 0: return {
      title: "KPI Dashboard | Kennzahlen-Übersicht",
      subtitle: "Zentrale Steuerung und Überwachung..."
    };
    case 1: return {
      title: "Netzwächter | Temperaturanalyse",
      subtitle: "Gruppierung / Untersuchung..."
    };
    // etc.
  }
};
```

---

### 2. Cockpit Layout
**File**: `src/components/Layout.tsx`
**Trigger**: URL with `?ui=cockpit` parameter
**Target Audience**: Advanced users, admin operations

#### Structure
```
┌────────┬─────────────────────────────────┐
│ Side-  │ Top Header                      │
│ bar    │ - Page Title                    │
│        │ - Bell Icon (notifications)     │
│ Logo   │ - User Avatar                   │
│ Nav    │ - Logout Button                 │
│ Items  ├─────────────────────────────────┤
│        │                                 │
│ User   │ Main Content                    │
│ Profile│ - Rendered route component      │
│        │ - Padding: varies by page       │
│        │                                 │
│        │                                 │
└────────┴─────────────────────────────────┘
```

#### Navigation Items (Permission-Based)
All items filtered by user profile permissions:
- KPI Dashboard (`showDashboard`)
- Objekt-Karte (`showMaps`)
- Netzwächter (`showNetworkMonitor`)
- Klassifizierung (`showEfficiencyStrategy`)
- Objektverwaltung (`showObjectManagement`)
- Logbuch (`showLogbook`)
- Admin Dashboard (`admin`, adminOnly)
- Objekt-Monitoring (`showGrafanaDashboards`)
- Energiedaten (`showEnergyData`)
- Geräteverwaltung (`showDeviceManagement`)
- System-Setup (`showSystemSetup`)
- API-Verwaltung (`admin`, adminOnly)
- Benutzerverwaltung (`showUserManagement`, adminOnly)
- Meine Benutzer (`showUser`)
- API-Test (`admin`, adminOnly)
- API-Tests (`admin`, adminOnly)

#### Sidebar Behavior
```typescript
// Cockpit sidebar styling
width: sidebarCollapsed ? 'w-16' : 'w-60'
background: bg-sidebar (hsl(215, 85%, 15%))
darker blue/navy

// Mobile responsive
useEffect(() => {
  const isMobile = window.innerWidth < 768;
  setSidebarCollapsed(isMobile);
}, []);
```

#### Header System
Static header with dynamic title from navigation items:
```typescript
const currentItem = navigationItems.find(item => item.href === location);
const title = currentItem?.label || "KPI Dashboard Wohnungswirtschaft";

// Special case for /efficiency route
if (location === "/efficiency") {
  return "Klassifizierung | Effizienzstrategie";
}
```

---

## Common Layout Components

### DatabaseStatusHeader
**File**: `src/components/DatabaseStatusHeader.tsx`
**Purpose**: Shows database connection status
**Placement**: Above both layout types
**Features**:
- Connection indicator
- Database name
- Error states

---

## Page Layout Patterns

### Pattern 1: Full-Width Content
**Used By**: Maps, GrafanaDashboard
```tsx
<Maps />  // No container, full viewport
```

### Pattern 2: Padded Container
**Used By**: Dashboard, NetworkMonitor, SystemSettings
```tsx
<div className="p-6">
  <div className="max-w-full mx-auto">
    {content}
  </div>
</div>
```

### Pattern 3: Zero Padding (LayoutStrawa)
**Used By**: All LayoutStrawa routes
```tsx
<div className="p-6 pt-[0px] pb-[0px] pl-[0px] pr-[0px]">
  {/* Effectively: px-6 only */}
</div>
```

### Pattern 4: Custom Padding
**Used By**: UserManagement
```tsx
<div className="p-6 pl-[10px] pr-[10px] pt-[10px] pb-[10px]">
  {/* Effectively: p-[10px] px-6... confusing */}
</div>
```

---

## Card-Based Layouts

### Pattern 1: Single Card Container
```tsx
<div className="p-6">
  <Card>
    <CardHeader>
      <CardTitle>Title</CardTitle>
    </CardHeader>
    <CardContent>
      {/* Main content */}
    </CardContent>
  </Card>
</div>
```
**Used By**: UserManagement, Logbook, ObjectManagement

### Pattern 2: Grid of Cards
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
  <Card>{/* KPI 1 */}</Card>
  <Card>{/* KPI 2 */}</Card>
  <Card>{/* KPI 3 */}</Card>
  <Card>{/* KPI 4 */}</Card>
</div>
```
**Used By**: Dashboard KPI section

### Pattern 3: Nested Card Layouts
```tsx
<Card>
  <CardHeader>...</CardHeader>
  <CardContent>
    <div className="grid gap-4">
      <Card>{/* Nested card */}</Card>
      <Card>{/* Nested card */}</Card>
    </div>
  </CardContent>
</Card>
```
**Used By**: SystemSettings, EfficiencyAnalysis

---

## Table Layouts

### Pattern 1: Fixed Header + Scrollable Body
**File**: `Dashboard.tsx` (Portfolio table)
```tsx
<Card className="flex-1 flex flex-col min-h-0">
  <CardHeader>{/* Filters */}</CardHeader>
  <CardContent className="flex-1 flex flex-col p-0 min-h-0">
    {/* Fixed header */}
    <div className="bg-blue-100 flex-shrink-0">
      <div className="grid ... h-10">
        {/* Column headers */}
      </div>
    </div>
    {/* Scrollable body */}
    <div className="flex-1 overflow-y-auto">
      {objects.map(obj => (
        <div className="grid ... h-10">
          {/* Row content */}
        </div>
      ))}
    </div>
  </CardContent>
</Card>
```

**Grid Layout**:
```css
style={{ gridTemplateColumns: '1fr 120px 160px 140px 140px 90px 90px 60px' }}
```

### Pattern 2: Native HTML Table
**File**: Various feature tables
```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Column 1</TableHead>
      <TableHead>Column 2</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {items.map(item => (
      <TableRow key={item.id}>
        <TableCell>{item.data1}</TableCell>
        <TableCell>{item.data2}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Pattern 3: Custom Grid Table (No borders)
**File**: `NetworkMonitor.tsx`, `TemperatureAnalysis.tsx`
```tsx
<div className="temp-analysis-table">
  {/* Custom CSS removes all borders */}
</div>
```

---

## Tab-Based Layouts

### Pattern 1: Full-Width Tabs (UserManagement)
```tsx
<Card>
  <CardHeader className="p-0">
    <Tabs defaultValue="users" className="w-full">
      <TabsList className="... w-full">
        <TabsTrigger value="users">Benutzer</TabsTrigger>
        <TabsTrigger value="mandates">Mandanten</TabsTrigger>
        <TabsTrigger value="objectgroups">Objektgruppen</TabsTrigger>
        <TabsTrigger value="profiles">Profile</TabsTrigger>
        <TabsTrigger value="userlog">UserLog</TabsTrigger>
      </TabsList>
      <TabsContent value="users" className="mt-0 p-0">
        <UserTable />
      </TabsContent>
      {/* Other tabs */}
    </Tabs>
  </CardHeader>
</Card>
```

**Styling Issues**:
```tsx
<style>{`
  /* Inline style overrides for tab appearance */
  button[data-state="active"] {
    background-color: #ffffff !important;
  }
`}</style>
```

### Pattern 2: Logbook Tabs
```tsx
<Tabs defaultValue="tasks">
  <TabsList>
    <TabsTrigger value="tasks">
      <ListTodo className="h-4 w-4 mr-2" />
      Aufgaben
    </TabsTrigger>
    <TabsTrigger value="entries">
      <FileText className="h-4 w-4 mr-2" />
      Einträge
    </TabsTrigger>
  </TabsList>
  <TabsContent value="tasks">...</TabsContent>
  <TabsContent value="entries">...</TabsContent>
</Tabs>
```

---

## Form Layouts

### Pattern 1: Stacked Form (Dialog)
```tsx
<Dialog>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Create User</DialogTitle>
    </DialogHeader>
    <Form>
      <FormField name="field1">...</FormField>
      <FormField name="field2">...</FormField>
      <FormField name="field3">...</FormField>
    </Form>
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button type="submit">Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Pattern 2: Two-Column Form
```tsx
<Form>
  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
    <FormField name="firstName">...</FormField>
    <FormField name="lastName">...</FormField>
  </div>
  <FormField name="email">...</FormField>
</Form>
```

### Pattern 3: Settings Form (Collapsible Sections)
```tsx
<Card>
  <Collapsible>
    <CollapsibleTrigger>
      <h3>Database Settings</h3>
    </CollapsibleTrigger>
    <CollapsibleContent>
      <Form>
        {/* Settings fields */}
      </Form>
    </CollapsibleContent>
  </Collapsible>
</Card>
```

---

## Grid Layouts

### Common Grid Patterns

#### 1. KPI Cards (4 columns)
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</div>
```

#### 2. Two-Column Layout (Sidebar + Main)
```tsx
<div className="flex gap-6">
  {/* Left sidebar */}
  <div className="max-w-[300px] min-w-[250px]">
    <EfficiencyDistributionCard />
  </div>

  {/* Main content */}
  <div className="flex-1">
    <Card>
      {/* Table */}
    </Card>
  </div>
</div>
```

#### 3. Dashboard + Stats Layout
```tsx
<div className="p-6 h-screen flex flex-col">
  {/* KPI Dashboard iframe */}
  <Card className="mb-6">{/* Iframe */}</Card>

  {/* KPI cards */}
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2">
    {/* Cards */}
  </div>

  {/* Two-column: Distribution + Table */}
  <div className="flex gap-6 mt-6 flex-1 min-h-0">
    {/* Left + Right */}
  </div>
</div>
```

---

## Responsive Breakpoints

### Tailwind Breakpoints Used
```
sm: 640px  (rarely used)
md: 768px  (most common)
lg: 1024px (common for grids)
xl: 1280px (rarely used)
2xl: 1536px (not used)
```

### Mobile Sidebar Behavior

#### Strawa Layout
```typescript
// Starts collapsed on small screens
const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

// No mobile check - always renders same
```

#### Cockpit Layout
```typescript
// Desktop: expanded, Mobile: collapsed
useEffect(() => {
  const isMobile = window.innerWidth < 768;
  setSidebarCollapsed(isMobile);
}, []);

// Mobile overlay
{!sidebarCollapsed && isMobile && (
  <div
    className="fixed inset-0 bg-black bg-opacity-50 z-20"
    onClick={() => setSidebarCollapsed(true)}
  />
)}
```

### Mobile Table Behavior
Most tables do NOT adapt well to mobile:
- Fixed column widths
- Horizontal scroll
- No card/list view alternative
- Headers remain visible

---

## Flexbox Layouts

### Pattern 1: Flex Column (Full Height)
```tsx
<div className="p-6 h-screen flex flex-col">
  {/* Header section */}
  <div className="mb-6">{/* Fixed height */}</div>

  {/* Scrollable content */}
  <div className="flex-1 overflow-auto">
    {/* Main content */}
  </div>
</div>
```

### Pattern 2: Flex Row (Sidebar + Content)
```tsx
<div className="flex h-screen overflow-hidden">
  {/* Sidebar */}
  <div className={`${sidebarCollapsed ? 'w-16' : 'w-60'} flex flex-col`}>
    {/* Sidebar content */}
  </div>

  {/* Main content */}
  <div className="flex-1 flex flex-col overflow-hidden">
    <header>{/* Header */}</header>
    <main className="flex-1 overflow-auto">{/* Content */}</main>
  </div>
</div>
```

### Pattern 3: Flex Gap for Spacing
```tsx
<div className="flex items-center space-x-4">
  <Icon />
  <div>
    <h3>Title</h3>
    <p>Description</p>
  </div>
  <Button>Action</Button>
</div>
```

---

## Container Patterns

### Pattern 1: Full Width
```tsx
<div className="w-full">
  {/* No max-width constraint */}
</div>
```

### Pattern 2: Centered Container
```tsx
<div className="max-w-full mx-auto">
  {/* Centers content but allows full width */}
</div>
```

### Pattern 3: Constrained Width
```tsx
<div className="max-w-[300px] min-w-[250px]">
  {/* Fixed width sidebar/card */}
</div>
```

---

## Scroll Behavior

### Pattern 1: Page-Level Scroll
```tsx
<main className="flex-1 overflow-auto">
  <div className="p-6">
    {/* Content scrolls within main */}
  </div>
</main>
```

### Pattern 2: Card-Level Scroll
```tsx
<Card className="h-full flex flex-col">
  <CardHeader>{/* Fixed */}</CardHeader>
  <CardContent className="flex-1 overflow-y-auto">
    {/* Scrollable content */}
  </CardContent>
</Card>
```

### Pattern 3: Table Scroll
```tsx
<div className="flex-1 overflow-y-auto">
  {/* Table rows scroll, header fixed */}
</div>
```

---

## Print Layouts

### Print CSS (index.css lines 731-799)
```css
@media print {
  /* Hide sidebar */
  .print-hide-sidebar { display: none !important; }

  /* Full width content */
  .print-full-width { width: 100% !important; }

  /* Hide buttons */
  .print-hide { display: none !important; }

  /* Optimize headers */
  .print-header {
    margin-bottom: 20px !important;
    border-bottom: 1px solid #e5e7eb !important;
  }
}
```

### Print-Specific Patterns
```tsx
<div className="print-hide-sidebar">
  {/* Sidebar won't print */}
</div>

<div className="print-full-width">
  {/* Content expands to full width when printing */}
</div>

<Button className="print-hide">
  {/* Button hidden in print */}
</Button>
```

---

## Layout Inconsistencies

### 1. Padding Overrides
Multiple pages use confusing padding patterns:
```tsx
// Why override with [0px]?
<div className="p-6 pt-[0px] pb-[0px] pl-[0px] pr-[0px]">

// Why mix units?
<div className="p-6 pl-[10px] pr-[10px] pt-[10px] pb-[10px]">
```

### 2. Grid vs Flex
- Some layouts use CSS Grid
- Others use Flexbox
- No consistent pattern for when to use which

### 3. Table Layouts
- Dashboard: Custom grid layout
- UserManagement: Native HTML table
- NetworkMonitor: Custom CSS with border removal
- No consistent table pattern

### 4. Container Widths
- No defined container system
- Some pages full width
- Others use max-w-full (which is... full width)
- No breakpoint-based containers

### 5. Scroll Containers
- Different scroll patterns per page
- Some use overflow-auto
- Others use overflow-y-auto
- Inconsistent min-h-0 usage

### 6. Mobile Responsiveness
- Sidebar behavior differs by layout
- Most tables don't adapt to mobile
- No mobile-first design approach
- Inconsistent breakpoint usage

---

## Layout Best Practices (Missing)

**What's Missing**:
1. Consistent container system
2. Defined breakpoint strategy
3. Mobile-first design
4. Responsive table patterns
5. Consistent scroll patterns
6. Standard page templates
7. Grid system documentation
8. Layout component library
