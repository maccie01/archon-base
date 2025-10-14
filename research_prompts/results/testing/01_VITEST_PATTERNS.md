# Research Result: Vitest Testing Patterns


# Vitest Testing Patterns

Created: 2025-10-13
Last Updated: 2025-10-14

## 1. Vitest Configuration

Create a `vitest.config.ts` at project root:

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['node_modules/', 'test/']
    }
  }
});
```

## 2. Unit Test Structure

```typescript
import { describe, it, expect } from 'vitest';
import { sum } from '../src/utils/math';

describe('sum utility', () => {
  it('adds positive numbers', () => {
    expect(sum(1, 2)).toBe(3);
  });

  it('adds negative numbers', () => {
    expect(sum(-1, -2)).toBe(-3);
  });
});
```

## 3. Test Hooks

```typescript
let counter = 0;

describe('hook usage', () => {
  beforeAll(() => {
    // runs once before all tests
    counter = 5;
  });

  beforeEach(() => {
    // runs before each test
    counter += 1;
  });

  afterEach(() => {
    // runs after each test
    counter -= 1;
  });

  afterAll(() => {
    // cleanup
    counter = 0;
  });

  it('test A', () => {
    expect(counter).toBe(6);
  });

  it('test B', () => {
    expect(counter).toBe(6);
  });
});
```

## 4. Mocking Functions and Modules

```typescript
import { vi } from 'vitest';
import * as api from '../src/api';
import { fetchData } from '../src/services/dataService';

vi.mock('../src/api', () => ({
  apiFetch: vi.fn()
}));

describe('fetchData', () => {
  it('returns data when apiFetch resolves', async () => {
    const mockData = { id: 1 };
    (api.apiFetch as jest.Mock).mockResolvedValue(mockData);

    const result = await fetchData('/endpoint');
    expect(result).toEqual(mockData);
    expect(api.apiFetch).toHaveBeenCalledWith('/endpoint');
  });

  it('throws error on fetch failure', async () => {
    (api.apiFetch as jest.Mock).mockRejectedValue(new Error('fail'));
    await expect(fetchData('/bad')).rejects.toThrow('fail');
  });
});
```

## 5. Async Testing

```typescript
import { it, expect } from 'vitest';
import { delay } from '../src/utils/async';

it('resolves after delay', async () => {
  const start = Date.now();
  await delay(100);
  const elapsed = Date.now() - start;
  expect(elapsed).toBeGreaterThanOrEqual(100);
});
```

## 6. Snapshot Testing

```typescript
import { expect, it } from 'vitest';
import { render } from '@testing-library/react';
import Button from '../src/components/Button';

it('matches snapshot', () => {
  const { container } = render(<Button label="Click" />);
  expect(container.innerHTML).toMatchSnapshot();
});
```

## 7. Coverage Configuration

See `vitest.config.ts` coverage section. Run:

```
vitest run --coverage
```

Coverage report in `coverage/` directory.

## 8. Component Testing with React Testing Library

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Counter from '../src/components/Counter';

describe('<Counter />', () => {
  it('renders initial count', () => {
    render(<Counter initial={0} />);
    expect(screen.getByText('Count: 0')).toBeDefined();
  });

  it('increments on click', async () => {
    render(<Counter initial={5} />);
    fireEvent.click(screen.getByText('Increment'));
    expect(screen.getByText('Count: 6')).toBeDefined();
  });
});
```

## 9. Testing Hooks

```typescript
import { renderHook, act } from '@testing-library/react-hooks';
import { useCounter } from '../src/hooks/useCounter';
import { describe, it, expect } from 'vitest';

describe('useCounter hook', () => {
  it('initializes count', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0));
    act(() => {
      result.current.increment();
    });
    expect(result.current.count).toBe(1);
  });
});
```

## 10. Testing Error Scenarios

```typescript
import { describe, it, expect } from 'vitest';
import { parseJson } from '../src/utils/json';

describe('parseJson', () => {
  it('throws on invalid JSON', () => {
    expect(() => parseJson('invalid')).toThrow();
  });
});
```

## 11. Service Layer Unit Tests

```typescript
// services/userService.test.ts
import { getUser } from '../../src/services/userService';
import { vi } from 'vitest';
import * as repo from '../../src/repositories/userRepository';

describe('getUser', () => {
  it('returns transformed user', async () => {
    const dbUser = { id: 1, name: 'Alice' };
    vi.spyOn(repo, 'findUser').mockResolvedValue(dbUser);
    const result = await getUser(1);
    expect(result).toEqual({ id: 1, displayName: 'Alice' });
  });
});
```

## 12. Repository Tests

```typescript
// repositories/userRepository.test.ts
import { describe, it, expect } from 'vitest';
import { findUser } from '../../src/repositories/userRepository';

describe('findUser', () => {
  it('resolves existing user', async () => {
    const user = await findUser(1);
    expect(user).toHaveProperty('id', 1);
  });
});
```

## 13. Mock Implementations

```typescript
vi.mock('axios', () => ({
  get: vi.fn().mockResolvedValue({ data: { text: 'hello' } })
}));
```

## 14. CI/CD Integration (GitHub Actions)

```yaml
# .github/workflows/test.yml
name: Test
on: [push,pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v2
        with:
          name: coverage-report
          path: coverage/
```

---

*Tags: shared, testing, vitest-patterns*
