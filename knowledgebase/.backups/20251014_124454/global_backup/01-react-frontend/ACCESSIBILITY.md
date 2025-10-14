# React Accessibility (a11y) Patterns

Created: 2025-10-13
Last Research: 2025-10-13
Sources: React Aria docs, MDN ARIA docs, Web Research (Medium, UXPin, A11Y Collective)

## Overview

Accessibility ensures applications are usable by everyone, including people with disabilities. React applications should be built with ARIA attributes, keyboard navigation, and screen reader support from the start.

## Core Principles

1. **Semantic HTML First**: Use correct HTML elements before ARIA
2. **Keyboard Accessible**: All interactions must work with keyboard
3. **Screen Reader Friendly**: Provide meaningful labels and descriptions
4. **Focus Management**: Maintain logical focus order
5. **Color Independence**: Don't rely solely on color to convey information

## WCAG 2.1 Guidelines

### Level A (Minimum)
- Text alternatives for images
- Keyboard accessible
- Sufficient color contrast

### Level AA (Standard)
- 4.5:1 contrast ratio for normal text
- 3:1 for large text
- Resizable text up to 200%

### Level AAA (Enhanced)
- 7:1 contrast ratio
- Enhanced error suggestions

**Target**: Aim for AA compliance minimum, AAA where possible.

## Patterns

### Pattern 1: Semantic HTML

**When to use**: Always prefer semantic elements

**Example skeleton**:
```typescript
// TODO: Add example code
// ❌ Bad: Using divs for everything
<div onClick={handleClick}>Click me</div>
<div>Main content</div>

// ✅ Good: Using semantic elements
<button onClick={handleClick}>Click me</button>
<main>Main content</main>

// Semantic structure
<header>
  <nav>
    <ul>
      <li><a href="/home">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>Footer content</p>
</footer>
```

**Semantic Elements**:
- `<button>` for clickable actions
- `<a>` for navigation
- `<nav>` for navigation sections
- `<main>` for main content
- `<article>`, `<section>` for content grouping
- `<header>`, `<footer>` for page structure

**References**:
- [MDN - HTML Elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)

### Pattern 2: ARIA Roles and Attributes

**When to use**: When semantic HTML isn't sufficient

**Example skeleton**:
```typescript
// TODO: Add example code
// ARIA roles
<div role="alert">Error message</div>
<div role="dialog" aria-modal="true">Modal content</div>
<div role="navigation">Custom navigation</div>

// ARIA states
<button aria-expanded={isOpen} aria-controls="menu">
  Menu
</button>
<div id="menu" aria-hidden={!isOpen}>
  Menu items
</div>

// ARIA properties
<button aria-label="Close dialog">×</button>
<input aria-describedby="email-help" />
<span id="email-help">Enter your email address</span>

// ARIA live regions
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

**Common ARIA Attributes**:
- `aria-label`: Accessible name for element
- `aria-labelledby`: References label element
- `aria-describedby`: Additional description
- `aria-hidden`: Hide from screen readers
- `aria-expanded`: Expandable element state
- `aria-controls`: Elements controlled by this element
- `aria-live`: Dynamic content updates

**References**:
- [MDN - ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)

### Pattern 3: Form Accessibility

**When to use**: For all forms

**Example skeleton**:
```typescript
// TODO: Add example code
// Label association
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid={hasError}
  aria-describedby="email-error"
/>
{hasError && (
  <span id="email-error" role="alert">
    Please enter a valid email
  </span>
)}

// Fieldset for grouped inputs
<fieldset>
  <legend>Contact Information</legend>
  <label htmlFor="name">Name</label>
  <input id="name" />

  <label htmlFor="email">Email</label>
  <input id="email" type="email" />
</fieldset>

// Required field indication
<label htmlFor="username">
  Username <span aria-label="required">*</span>
</label>
<input id="username" required aria-required="true" />

// Error messages
{errors.username && (
  <div role="alert" aria-live="assertive">
    {errors.username.message}
  </div>
)}
```

**References**:
- [ARIA - Forms](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/forms)

### Pattern 4: Keyboard Navigation

**When to use**: For all interactive elements

**Example skeleton**:
```typescript
// TODO: Add example code
// Button keyboard support (built-in)
<button onClick={handleClick}>Click me</button>

// Custom interactive element needs keyboard support
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleClick()
    }
  }}
>
  Custom button
</div>

// Skip links
<a href="#main-content" className="skip-link">
  Skip to main content
</a>
<main id="main-content">...</main>

// Modal focus trap
import { useEffect, useRef } from 'react'

function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousActiveElement = useRef<HTMLElement>()

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement
      modalRef.current?.focus()
    } else {
      previousActiveElement.current?.focus()
    }
  }, [isOpen])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose()
    }
  }

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  )
}
```

**Keyboard Patterns**:
- **Tab**: Move to next focusable element
- **Shift + Tab**: Move to previous
- **Enter/Space**: Activate buttons
- **Escape**: Close modals/dropdowns
- **Arrow keys**: Navigate within widgets (menus, tabs)

**References**:
- [ARIA Keyboard Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)

### Pattern 5: Focus Management

**When to use**: For dynamic content, modals, route changes

**Example skeleton**:
```typescript
// TODO: Add example code
import { useEffect, useRef } from 'react'

// Focus heading on route change
function Page({ title }) {
  const headingRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    headingRef.current?.focus()
  }, [])

  return (
    <h1 ref={headingRef} tabIndex={-1}>
      {title}
    </h1>
  )
}

// Restore focus after modal closes
function useRestoreFocus() {
  const previousActiveElement = useRef<HTMLElement>()

  const saveFocus = () => {
    previousActiveElement.current = document.activeElement as HTMLElement
  }

  const restoreFocus = () => {
    previousActiveElement.current?.focus()
  }

  return { saveFocus, restoreFocus }
}

// Focus first error in form
const firstErrorField = Object.keys(errors)[0]
if (firstErrorField) {
  document.getElementById(firstErrorField)?.focus()
}
```

### Pattern 6: Screen Reader Announcements

**When to use**: For dynamic content changes

**Example skeleton**:
```typescript
// TODO: Add example code
// Live region for status updates
function StatusMessage({ message }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  )
}

// Alert for errors
function ErrorMessage({ error }) {
  return (
    <div
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      {error}
    </div>
  )
}

// Screen reader only text
<span className="sr-only">
  Loading... Please wait
</span>

// CSS for sr-only
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

**ARIA Live Regions**:
- `aria-live="polite"`: Announce when screen reader is idle
- `aria-live="assertive"`: Announce immediately
- `aria-atomic="true"`: Read entire region, not just changes

**References**:
- [ARIA Live Regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions)

### Pattern 7: Accessible Modals

**When to use**: For all dialogs and modals

**Example skeleton**:
```typescript
// TODO: Add example code
import { useEffect, useRef } from 'react'
import FocusTrap from 'focus-trap-react'

function AccessibleModal({ isOpen, onClose, title, children }) {
  const modalRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      // Prevent body scroll
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <FocusTrap>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        ref={modalRef}
        onKeyDown={(e) => {
          if (e.key === 'Escape') onClose()
        }}
      >
        <div className="modal-overlay" onClick={onClose} />
        <div className="modal-content">
          <h2 id="modal-title">{title}</h2>
          {children}
          <button onClick={onClose} aria-label="Close dialog">
            ×
          </button>
        </div>
      </div>
    </FocusTrap>
  )
}
```

**Modal Requirements**:
- Focus trap (keyboard focus stays in modal)
- Close on Escape key
- Return focus to trigger element on close
- `aria-modal="true"` and `role="dialog"`
- Labeled with `aria-labelledby` or `aria-label`

### Pattern 8: Accessible Components with React Aria

**When to use**: For complex accessible components

**Example skeleton**:
```typescript
// TODO: Add example code
import { useButton } from 'react-aria'
import { useRef } from 'react'

function Button(props) {
  const ref = useRef()
  const { buttonProps } = useButton(props, ref)

  return (
    <button {...buttonProps} ref={ref}>
      {props.children}
    </button>
  )
}

// Complex components made accessible
import { useMenu, useMenuItem } from 'react-aria'

// React Aria handles:
// - Keyboard navigation
// - ARIA attributes
// - Focus management
// - Screen reader announcements
```

**References**:
- [React Aria Documentation](https://react-spectrum.adobe.com/react-aria/)

## Testing Accessibility

### Manual Testing

**Keyboard Navigation**:
1. Unplug mouse
2. Navigate entire app with Tab, Enter, Escape, Arrow keys
3. Check focus indicators are visible
4. Ensure logical tab order

**Screen Reader Testing**:
- **macOS**: VoiceOver (Cmd + F5)
- **Windows**: NVDA (free) or JAWS
- **Test**: Navigate page, interact with components

### Automated Testing

```typescript
// TODO: Add example code
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

test('has no accessibility violations', async () => {
  const { container } = render(<MyComponent />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

**Tools**:
- **axe DevTools**: Browser extension
- **jest-axe**: Testing Library integration
- **Lighthouse**: Chrome DevTools audit
- **WAVE**: Web accessibility evaluation tool

## Common Patterns

### Accessible Button vs Link
```typescript
// Button: triggers action
<button onClick={handleAction}>Save</button>

// Link: navigates
<a href="/profile">View Profile</a>
```

### Image Alt Text
```typescript
// Decorative image
<img src="decoration.png" alt="" role="presentation" />

// Informative image
<img src="chart.png" alt="Sales increased 25% in Q4" />

// Background image with text
<div style={{ backgroundImage: 'url(hero.jpg)' }}>
  <h1>Welcome</h1>
  <span className="sr-only">Hero image of team collaboration</span>
</div>
```

### Color Contrast
```typescript
// Check contrast ratio
// Normal text: 4.5:1 minimum (AA), 7:1 (AAA)
// Large text: 3:1 minimum (AA), 4.5:1 (AAA)

// Example: Accessible colors
color: #333; // on white background (11.7:1)
background: #0066cc; // with white text (4.54:1)
```

## Common Mistakes

1. **Div/Span Buttons**: Using non-semantic elements for buttons
2. **Missing Labels**: Inputs without associated labels
3. **Poor Color Contrast**: Text too light on background
4. **Keyboard Traps**: User can't escape modal or dropdown
5. **Missing Alt Text**: Images without descriptions
6. **Removing Focus Outlines**: Making focus invisible
7. **ARIA Overuse**: Adding ARIA when semantic HTML works
8. **Unlabeled Icons**: Icon buttons without accessible names

## Accessible Component Libraries

### Headless UI Libraries (Recommended)
- **Radix UI**: Comprehensive, unstyled, accessible
- **React Aria**: Adobe's accessible components
- **Headless UI**: Tailwind's accessible components
- **Ariakit**: Toolkit for building accessible interfaces

### Why Headless?
- Full accessibility built-in
- Customizable styling
- Keyboard navigation
- Screen reader support
- Focus management

## Tools and Resources

### Testing Tools
- **axe DevTools**: Browser extension
- **Lighthouse**: Chrome DevTools
- **WAVE**: Accessibility checker
- **Color Contrast Analyzers**: Various browser extensions

### Screen Readers
- **NVDA** (Windows, free)
- **JAWS** (Windows, paid)
- **VoiceOver** (macOS/iOS, built-in)
- **TalkBack** (Android, built-in)

### Learning Resources
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [React Aria Accessibility](https://react-spectrum.adobe.com/react-aria/accessibility.html)

## Additional Resources

- [React Docs - Accessibility](https://react.dev/learn/accessibility)
- [React Aria Documentation](https://react-spectrum.adobe.com/react-aria/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [MDN ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
- [Mastering Modal Accessibility](https://www.a11y-collective.com/blog/modal-accessibility/)
- [React Accessibility Best Practices (Medium)](https://medium.com/@ignatovich.dm/accessibility-in-react-best-practices-for-building-inclusive-web-apps-906d1cbedd27)

## Next Steps

- Review [TESTING_REACT.md](./TESTING_REACT.md) for accessibility testing
- See [COMPONENT_PATTERNS.md](./COMPONENT_PATTERNS.md) for accessible component patterns
- Check [ANTIPATTERNS.md](./ANTIPATTERNS.md) for accessibility anti-patterns
