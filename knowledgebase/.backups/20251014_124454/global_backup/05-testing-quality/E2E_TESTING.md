# End-to-End Testing Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Playwright docs, Cypress best practices, E2E testing patterns

## Overview

End-to-end (E2E) tests verify complete user workflows across your application, testing the system as a whole including frontend, backend, and integrations.

## Core Principles

1. **Test Critical User Journeys** - Focus on high-value paths
2. **Minimize E2E Tests** - They're slow and expensive
3. **Test in Production-Like Environment** - Realistic conditions
4. **Avoid Test Interdependence** - Each test should be isolated
5. **Make Tests Resilient** - Handle timing and async issues

## When to Use E2E Tests

### Use E2E Tests For:
- Critical user journeys (login, checkout, signup)
- Multi-page workflows
- Integration between systems
- Real browser behavior
- Production smoke tests

### Don't Use E2E Tests For:
- Unit-testable logic
- Component variations
- Edge cases (test at lower levels)
- Rapid feedback during development

## Playwright vs Cypress

### Playwright
**Strengths:**
- Multi-browser support (Chromium, Firefox, WebKit)
- Fast parallel execution
- Auto-waiting built-in
- Network interception
- Multiple contexts/tabs
- Better for cross-browser testing

**Use When:**
- Need multi-browser support
- Want parallel test execution
- Testing complex scenarios

### Cypress
**Strengths:**
- Excellent developer experience
- Time-travel debugging
- Real-time reloading
- Rich ecosystem
- Visual testing built-in

**Use When:**
- Primarily testing Chrome
- Want best DX
- Need visual regression testing

## Playwright Patterns

### Basic Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }]
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
})
```

### Basic Test Structure
```typescript
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('/login')

  await page.fill('input[name="email"]', 'user@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await expect(page).toHaveURL('/dashboard')
  await expect(page.locator('h1')).toContainText('Welcome')
})
```

### Page Object Model
```typescript
// TODO: Add complete POM pattern
// Create page classes, reusable selectors, actions
```

### Fixtures
```typescript
// TODO: Add custom fixtures example
// Authenticated user, test data, database state
```

### API Testing with Playwright
```typescript
// TODO: Add API testing example
// Using request context, authentication
```

## Cypress Patterns

### Basic Configuration
```typescript
// TODO: Add Cypress config
// Base URL, viewport, test files, plugins
```

### Basic Test
```typescript
// TODO: Add Cypress test example
```

### Custom Commands
```typescript
// TODO: Add custom Cypress commands
```

## Test Patterns

### Pattern 1: Authentication Flow
```typescript
// TODO: Add login/logout test
// Register, login, session, logout
```

### Pattern 2: Form Submission
```typescript
// TODO: Add form test
// Fill, validate, submit, success message
```

### Pattern 3: Multi-Step Workflow
```typescript
// TODO: Add wizard/multi-step form
// Step navigation, data persistence
```

### Pattern 4: CRUD Operations
```typescript
// TODO: Add CRUD test
// Create, read, update, delete entity
```

## Locator Strategies

### Priority Order
1. User-facing attributes (text, label, placeholder)
2. Semantic selectors (role, alt text)
3. Test IDs (data-testid)
4. CSS selectors (last resort)

### Playwright Locators
```typescript
// By role
await page.getByRole('button', { name: 'Submit' })

// By text
await page.getByText('Welcome')

// By label
await page.getByLabel('Email')

// By placeholder
await page.getByPlaceholder('Enter email')

// By test ID
await page.getByTestId('submit-button')

// CSS selector (avoid if possible)
await page.locator('.submit-btn')
```

### Making Selectors Resilient
```typescript
// TODO: Add best practices for selectors
// Avoid: brittle CSS classes, IDs that change
// Prefer: semantic HTML, stable test IDs
```

## Handling Async Behavior

### Auto-Waiting (Playwright)
```typescript
// Playwright automatically waits for:
// - Element to be visible
// - Element to be stable (not animating)
// - Element to receive events
// - Element to be enabled

await page.click('button') // Auto-waits for button
```

### Explicit Waiting
```typescript
// Wait for element
await page.waitForSelector('.loaded')

// Wait for navigation
await page.waitForNavigation()

// Wait for network idle
await page.waitForLoadState('networkidle')

// Wait for custom condition
await page.waitForFunction(() => window.dataLoaded === true)
```

### Timeouts
```typescript
// TODO: Add timeout configuration
// Global timeout, test timeout, action timeout
```

## Test Data Management

### Test Data Setup
```typescript
// TODO: Add test data patterns
// Factories, fixtures, seeders
```

### Database Seeding
```typescript
// TODO: Add database setup/teardown
// Before/after hooks, isolated data
```

### API Mocking
```typescript
// Playwright route interception
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ users: [] })
  })
})
```

## Authentication

### Authenticated State
```typescript
// TODO: Add auth setup pattern
// Login once, save state, reuse in tests
```

### Using Storage State
```typescript
// Save auth state
await page.context().storageState({ path: 'auth.json' })

// Reuse auth state
const context = await browser.newContext({
  storageState: 'auth.json'
})
```

## Visual Testing

### Screenshot Comparison
```typescript
// TODO: Add visual regression testing
// Percy, Applitools, or built-in screenshots
```

### Accessibility Testing
```typescript
// TODO: Add axe-core integration
// Automated a11y testing
```

## Network Testing

### Intercepting Requests
```typescript
// TODO: Add network interception
// Mock APIs, modify responses, verify requests
```

### Testing Error States
```typescript
// TODO: Add error state testing
// Network failures, 500 errors, timeouts
```

## Mobile Testing

### Emulating Mobile Devices
```typescript
// TODO: Add mobile device emulation
// Viewport, user agent, touch events
```

## Parallel Execution

### Configuring Parallelism
```typescript
// TODO: Add parallel execution config
// Workers, sharding, CI parallelization
```

### Test Isolation
```typescript
// TODO: Add test isolation patterns
// Separate data, unique users, cleanup
```

## CI/CD Integration

### GitHub Actions
```yaml
# TODO: Add GitHub Actions workflow
# Install, build, test, upload artifacts
```

### Docker Integration
```yaml
# TODO: Add Docker setup
# Playwright container, services
```

## Debugging

### Debug Mode
```bash
# Playwright debug mode
npx playwright test --debug

# Headed mode
npx playwright test --headed

# UI mode
npx playwright test --ui
```

### Trace Viewer
```typescript
// TODO: Add trace viewer usage
// Recording, viewing, sharing traces
```

### Video Recording
```typescript
use: {
  video: 'on-first-retry',
}
```

## Flaky Test Management

### Causes of Flakiness
- Race conditions
- Network timing
- Animation interference
- Random test data
- Shared state

### Making Tests Stable
```typescript
// TODO: Add anti-flake patterns
// Proper waiting, retry logic, deterministic data
```

### Retry Logic
```typescript
// TODO: Add retry configuration
// Automatic retries, custom retry conditions
```

## Performance Testing

### Load Time Testing
```typescript
// TODO: Add performance metrics
// Page load, resource timing, Core Web Vitals
```

### Resource Monitoring
```typescript
// TODO: Add resource monitoring
// Network, memory, CPU during tests
```

## Best Practices

1. **Keep E2E Tests Minimal** - Test critical paths only
2. **Use Page Objects** - Encapsulate page interactions
3. **Independent Tests** - No test should depend on another
4. **Stable Selectors** - Use semantic, stable locators
5. **Explicit Waits** - Wait for specific conditions
6. **Realistic Data** - Use production-like test data
7. **Clean Up** - Reset state after tests
8. **Run in CI** - Automate execution
9. **Monitor Flakiness** - Track and fix flaky tests
10. **Parallel Execution** - Speed up test suite

## Common Mistakes

### 1. Too Many E2E Tests
```typescript
// Bad - testing everything at E2E level
// Good - pyramid: more unit, fewer E2E
```

### 2. Brittle Selectors
```typescript
// Bad
await page.click('.btn-primary.submit-form.active')

// Good
await page.getByRole('button', { name: 'Submit' })
```

### 3. Test Interdependence
```typescript
// Bad - test depends on previous test
test('edit user', async () => {
  // Assumes user exists from previous test
})

// Good - each test sets up own data
test('edit user', async () => {
  await createUser()
  await editUser()
})
```

## Reporting

### HTML Reports
```typescript
// TODO: Add HTML reporter config
```

### Custom Reporters
```typescript
// TODO: Add custom reporter example
// Slack, email, dashboard integration
```

## Tools and Plugins

### Playwright Plugins
- @axe-core/playwright - Accessibility testing
- playwright-video - Video recording
- playwright-lighthouse - Performance testing

### Cypress Plugins
- cypress-axe - Accessibility
- cypress-visual-regression - Visual testing
- cypress-file-upload - File uploads

## Additional Resources

- [TESTING_STRATEGY.md](./TESTING_STRATEGY.md) - Overall testing approach
- [INTEGRATION_TESTING.md](./INTEGRATION_TESTING.md) - Integration testing
- [Playwright Documentation](https://playwright.dev/)
- [Cypress Documentation](https://www.cypress.io/)
