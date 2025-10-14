# UI Component Inventory - shadcn/ui & Radix Components

**Created:** 2025-10-13
**Last Updated:** 2025-10-13

## Overview
The application uses shadcn/ui components built on top of Radix UI primitives. All components are located in `src/components/ui/` and are fully customizable with Tailwind CSS.

## Core UI Components

### 1. Alert (`alert.tsx`)
**Purpose**: Display important messages and notifications
**Radix Base**: Custom component with Radix styling patterns
**Variants**:
- Default
- Destructive

**Usage**:
```tsx
<Alert>
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>System maintenance scheduled</AlertDescription>
</Alert>
```

**Used In**:
- Error messages
- System notifications
- Warning dialogs

---

### 2. Avatar (`avatar.tsx`)
**Purpose**: Display user profile images with fallbacks
**Radix Base**: @radix-ui/react-avatar
**Features**:
- Image loading with fallback
- Initials fallback
- Size variants

**Usage**:
```tsx
<Avatar>
  <AvatarImage src={user.profileImageUrl} />
  <AvatarFallback>{user.initials}</AvatarFallback>
</Avatar>
```

**Used In**:
- Sidebar user profile (Layout.tsx)
- User management tables
- Header user menu
- LayoutStrawa sidebar

---

### 3. Badge (`badge.tsx`)
**Purpose**: Display status indicators and labels
**Variants**:
- Default
- Secondary
- Destructive
- Outline

**Usage**:
```tsx
<Badge variant="destructive">Critical</Badge>
<Badge className="bg-green-600 text-white">A+</Badge>
```

**Used In**:
- Efficiency class indicators (Dashboard)
- Status labels (Logbook)
- Temperature warnings (NetworkMonitor)
- User role badges

---

### 4. Button (`button.tsx`)
**Purpose**: Primary interactive element
**Variants**:
- Default
- Destructive
- Outline
- Secondary
- Ghost
- Link

**Sizes**: sm, md (default), lg, icon

**Usage**:
```tsx
<Button variant="outline" size="sm">
  <PlusIcon className="h-4 w-4 mr-2" />
  Add User
</Button>
```

**Used In**:
- Forms (all feature modules)
- Navigation actions
- Dialog triggers
- Table actions
- Modal controls

---

### 5. Calendar (`calendar.tsx`)
**Purpose**: Date picker component
**Radix Base**: @radix-ui/react-calendar
**Features**:
- Month navigation
- Date range selection
- Disabled dates support
- Localization ready

**Used In**:
- Logbook date filters
- Report date ranges
- Time range selectors

---

### 6. Card (`card.tsx`)
**Purpose**: Container component for grouped content
**Components**:
- Card (wrapper)
- CardHeader
- CardTitle
- CardDescription
- CardContent
- CardFooter

**Usage**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>KPI Dashboard</CardTitle>
    <CardDescription>Real-time metrics</CardDescription>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
</Card>
```

**Used In**:
- Dashboard KPI cards
- Settings panels
- Feature containers
- Statistics displays
- Almost every page layout

---

### 7. Checkbox (`checkbox.tsx`)
**Purpose**: Boolean input control
**Radix Base**: @radix-ui/react-checkbox

**Usage**:
```tsx
<Checkbox
  checked={isEnabled}
  onCheckedChange={setIsEnabled}
/>
```

**Used In**:
- User profile permissions
- Settings toggles
- Multi-select tables
- Filter options

---

### 8. Collapsible (`collapsible.tsx`)
**Purpose**: Expandable/collapsible content sections
**Radix Base**: @radix-ui/react-collapsible

**Usage**:
```tsx
<Collapsible>
  <CollapsibleTrigger>Show Details</CollapsibleTrigger>
  <CollapsibleContent>{/* Hidden content */}</CollapsibleContent>
</Collapsible>
```

**Used In**:
- Settings sections (SystemSettings)
- Portal configuration cards
- Advanced options

---

### 9. Dialog (`dialog.tsx`)
**Purpose**: Modal dialogs and overlays
**Radix Base**: @radix-ui/react-dialog
**Components**:
- Dialog (wrapper)
- DialogTrigger
- DialogContent
- DialogHeader
- DialogTitle
- DialogDescription
- DialogFooter

**Usage**:
```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm Action</DialogTitle>
      <DialogDescription>Are you sure?</DialogDescription>
    </DialogHeader>
    {/* Form content */}
    <DialogFooter>
      <Button variant="outline" onClick={close}>Cancel</Button>
      <Button onClick={confirm}>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

**Used In**:
- User forms (UserManagement)
- Object group management
- Confirmation dialogs
- Export dialogs
- Settings modals
- User settings modal (LayoutStrawa)

**Known Issue**: Dialog overlay transparency fixed in index.css (line 931-947)

---

### 10. Form (`form.tsx`)
**Purpose**: Form state management wrapper
**Radix Base**: @radix-ui/react-form + react-hook-form
**Components**:
- Form (wrapper)
- FormField
- FormItem
- FormLabel
- FormControl
- FormDescription
- FormMessage

**Usage**:
```tsx
<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField
      control={form.control}
      name="username"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Username</FormLabel>
          <FormControl>
            <Input {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  </form>
</Form>
```

**Used In**:
- All form components
- User creation/editing
- Settings configuration
- Login forms

---

### 11. Input (`input.tsx`)
**Purpose**: Text input field
**Features**:
- Type variants (text, email, password, etc.)
- Disabled state
- Error states
- Full width support

**Usage**:
```tsx
<Input
  type="email"
  placeholder="user@example.com"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
/>
```

**Used In**:
- All forms
- Search filters
- Configuration editors
- Login forms

---

### 12. Label (`label.tsx`)
**Purpose**: Form field labels
**Radix Base**: @radix-ui/react-label
**Features**:
- Accessibility support
- Proper for/id associations

**Used In**:
- All form fields
- Checkbox labels
- Settings panels

---

### 13. Popover (`popover.tsx`)
**Purpose**: Floating content container
**Radix Base**: @radix-ui/react-popover
**Components**:
- Popover (wrapper)
- PopoverTrigger
- PopoverContent

**Usage**:
```tsx
<Popover>
  <PopoverTrigger asChild>
    <Button variant="outline">Options</Button>
  </PopoverTrigger>
  <PopoverContent>
    {/* Popover content */}
  </PopoverContent>
</Popover>
```

**Used In**:
- Calendar pickers
- Select dropdowns
- Context menus
- Filter panels

---

### 14. Progress (`progress.tsx`)
**Purpose**: Progress bar indicator
**Radix Base**: @radix-ui/react-progress

**Usage**:
```tsx
<Progress value={progress} max={100} />
```

**Used In**:
- Loading states
- File upload progress
- Task completion indicators

---

### 15. Radio Group (`radio-group.tsx`)
**Purpose**: Single selection from multiple options
**Radix Base**: @radix-ui/react-radio-group
**Components**:
- RadioGroup (wrapper)
- RadioGroupItem

**Usage**:
```tsx
<RadioGroup value={selected} onValueChange={setSelected}>
  <RadioGroupItem value="option1" />
  <RadioGroupItem value="option2" />
</RadioGroup>
```

**Used In**:
- Settings selections
- Dashboard type selectors
- Filter options

---

### 16. Select (`select.tsx`)
**Purpose**: Dropdown selection component
**Radix Base**: @radix-ui/react-select
**Components**:
- Select (wrapper)
- SelectTrigger
- SelectValue
- SelectContent
- SelectItem
- SelectGroup
- SelectLabel

**Usage**:
```tsx
<Select value={value} onValueChange={setValue}>
  <SelectTrigger>
    <SelectValue placeholder="Select option" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
  </SelectContent>
</Select>
```

**Used In**:
- Dashboard filters (efficiency, building type)
- User role selection
- Mandate selection
- Object group filters
- Time range selectors

---

### 17. Separator (`separator.tsx`)
**Purpose**: Visual divider between content sections
**Radix Base**: @radix-ui/react-separator

**Usage**:
```tsx
<Separator orientation="horizontal" />
<Separator orientation="vertical" />
```

**Used In**:
- Form sections
- Sidebar divisions
- Content grouping

---

### 18. Switch (`switch.tsx`)
**Purpose**: Toggle switch for boolean values
**Radix Base**: @radix-ui/react-switch

**Usage**:
```tsx
<Switch
  checked={isEnabled}
  onCheckedChange={setIsEnabled}
/>
```

**Used In**:
- User profile permissions (sidebar toggles)
- Settings toggles
- Feature flags
- Boolean configuration options

---

### 19. Table (`table.tsx`)
**Purpose**: Data table structure
**Components**:
- Table (wrapper)
- TableHeader
- TableBody
- TableFooter
- TableRow
- TableHead
- TableCell
- TableCaption

**Usage**:
```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Item 1</TableCell>
      <TableCell>Active</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

**Used In**:
- Dashboard portfolio table
- User management tables
- Object lists
- Logbook entries/tasks
- Temperature analysis tables

**Styling Inconsistency**: Some tables use custom grid layouts instead of native table elements

---

### 20. Tabs (`tabs.tsx`)
**Purpose**: Tabbed content navigation
**Radix Base**: @radix-ui/react-tabs
**Components**:
- Tabs (wrapper)
- TabsList
- TabsTrigger
- TabsContent

**Usage**:
```tsx
<Tabs defaultValue="tab1">
  <TabsList>
    <TabsTrigger value="tab1">Tab 1</TabsTrigger>
    <TabsTrigger value="tab2">Tab 2</TabsTrigger>
  </TabsList>
  <TabsContent value="tab1">{/* Content 1 */}</TabsContent>
  <TabsContent value="tab2">{/* Content 2 */}</TabsContent>
</Tabs>
```

**Used In**:
- UserManagement (Users, Mandates, Object Groups, Profiles, UserLog)
- Logbook (Tasks, Entries)
- Settings pages
- Dashboard views

**Known Issue**: Tab styling inconsistencies - see UI_INCONSISTENCIES.md

---

### 21. Textarea (`textarea.tsx`)
**Purpose**: Multi-line text input

**Usage**:
```tsx
<Textarea
  placeholder="Enter description..."
  rows={4}
  value={description}
  onChange={(e) => setDescription(e.target.value)}
/>
```

**Used In**:
- Logbook entry forms
- Comment sections
- JSON configuration editors
- Notes fields

---

### 22. Toast/Toaster (`toast.tsx`, `toaster.tsx`)
**Purpose**: Notification system
**Radix Base**: @radix-ui/react-toast
**Components**:
- Toaster (provider)
- Toast
- ToastAction
- ToastTitle
- ToastDescription

**Usage**:
```tsx
// In App.tsx
<Toaster />

// In components
toast({
  title: "Success",
  description: "Operation completed successfully",
  variant: "default" // or "destructive"
});
```

**Used In**:
- Success/error notifications
- API response feedback
- Form submission results
- Logout confirmation

**Known Issue**: Toast opacity fixed in index.css (line 949-967)

---

### 23. Toggle (`toggle.tsx`)
**Purpose**: Toggle button component
**Radix Base**: @radix-ui/react-toggle
**Variants**:
- Default
- Outline

**Used In**:
- Toolbar buttons
- View mode switches
- Filter toggles

---

### 24. Tooltip (`tooltip.tsx`)
**Purpose**: Contextual help and information
**Radix Base**: @radix-ui/react-tooltip
**Components**:
- TooltipProvider (global wrapper)
- Tooltip (wrapper)
- TooltipTrigger
- TooltipContent

**Usage**:
```tsx
<Tooltip>
  <TooltipTrigger asChild>
    <Button variant="ghost">
      <InfoIcon className="h-4 w-4" />
    </Button>
  </TooltipTrigger>
  <TooltipContent>
    <p>Additional information</p>
  </TooltipContent>
</Tooltip>
```

**Used In**:
- Icon buttons (sidebar navigation)
- Help text
- Truncated text expansion
- Feature explanations

---

## Custom Shared Components

### 1. Layout (`components/Layout.tsx`)
**Purpose**: Main application layout with sidebar
**Features**:
- Collapsible sidebar
- Navigation menu with permissions
- User profile section
- Mobile responsive
- Print-optimized

**Used In**: Cockpit mode routes

---

### 2. DatabaseStatusHeader (`components/DatabaseStatusHeader.tsx`)
**Purpose**: Shows current database connection status
**Features**:
- Connection indicator
- Database name display
- Error states

**Used In**: All authenticated routes

---

### 3. ExportDialog (`components/ExportDialog.tsx`)
**Purpose**: Data export functionality
**Features**:
- CSV/Excel export
- Email delivery option
- Filter preservation

**Used In**:
- Dashboard portfolio table
- Temperature analysis
- Logbook exports

---

### 4. SystemSchemaView (`components/SystemSchemaView.tsx`)
**Purpose**: Database schema visualization
**Used In**: Admin/development features

---

### 5. FallbackDatabaseAccess (`components/FallbackDatabaseAccess.tsx`)
**Purpose**: Alternative database connection UI
**Used In**: Database connection failures

---

### 6. CurrentDatabaseConnection (`components/CurrentDatabaseConnection.tsx`)
**Purpose**: Database connection switcher
**Used In**: System settings

---

## Component Testing

All components have corresponding test files in `__tests__/` directories:
- Button.test.tsx
- Dialog.test.tsx
- Input.test.tsx
- Card.test.tsx
- Switch.test.tsx
- etc.

Tests use:
- Vitest as test runner
- React Testing Library
- User event simulation

## Component Variants Summary

### Color Variants
- **Primary**: Blue (#2563eb) - Main actions
- **Secondary**: Gray - Supporting actions
- **Destructive**: Red - Dangerous actions
- **Success**: Green - Positive feedback
- **Warning**: Orange/Yellow - Caution
- **Muted**: Light gray - Subtle elements

### Size Variants
- **sm**: Small/compact
- **md**: Medium/default
- **lg**: Large
- **icon**: Icon-only buttons

### State Variants
- Default
- Hover
- Active/Selected
- Disabled
- Loading
- Error

## Accessibility Features

All components include:
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support
- Color contrast compliance
- Focus indicators

## Missing Components

Components that might be needed but don't exist yet:
1. Skeleton loader (uses custom div with animate-pulse)
2. Data table component (uses custom table layouts)
3. Combobox (select with search)
4. Command palette
5. Drawer (uses Dialog instead)
6. Breadcrumb navigation
7. Pagination component
8. Empty state component
9. Loading spinner component
10. Badge notification dot

## Component Usage Statistics

**Most Used Components**:
1. Button (100+ instances)
2. Card (50+ instances)
3. Dialog (20+ instances)
4. Table (15+ instances)
5. Select (20+ instances)
6. Input (40+ instances)
7. Tabs (10+ instances)

**Least Used Components**:
1. Toggle
2. Separator
3. Progress
4. Collapsible
