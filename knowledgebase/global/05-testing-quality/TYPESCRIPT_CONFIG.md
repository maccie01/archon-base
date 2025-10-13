# TypeScript Configuration Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: TypeScript documentation, strict mode best practices

## Overview

TypeScript adds static typing to JavaScript, catching errors at compile time. Proper configuration is essential for maximizing type safety and developer experience.

## Core Principles

1. **Strictness** - Enable strict mode for maximum safety
2. **Incremental** - Use project references for large codebases
3. **Modern** - Target modern ES versions
4. **Modular** - ESM for tree-shaking
5. **Fast** - Optimize for build speed

## Basic Configuration

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Strict Mode Options

### Enable All Strict Checks
```json
{
  "compilerOptions": {
    "strict": true,
    // Strict mode includes:
    // "noImplicitAny": true,
    // "strictNullChecks": true,
    // "strictFunctionTypes": true,
    // "strictBindCallApply": true,
    // "strictPropertyInitialization": true,
    // "noImplicitThis": true,
    // "alwaysStrict": true
  }
}
```

### Additional Strict Options
```json
{
  "compilerOptions": {
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Frontend Configuration (React + Vite)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Backend Configuration (Node.js)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "types": ["node"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Monorepo Configuration

### Root tsconfig.json
```json
{
  "files": [],
  "references": [
    { "path": "./apps/frontend" },
    { "path": "./apps/backend" },
    { "path": "./packages/shared-types" }
  ]
}
```

### Package tsconfig.json
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "outDir": "./dist"
  },
  "include": ["src"],
  "references": [
    { "path": "../shared-types" }
  ]
}
```

## Path Mapping

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@shared/*": ["../../packages/shared-types/*"]
    }
  }
}
```

## Module Resolution

### Bundler (Vite, Webpack)
```json
{
  "compilerOptions": {
    "moduleResolution": "bundler"
  }
}
```

### Node.js ESM
```json
{
  "compilerOptions": {
    "moduleResolution": "node16"
  }
}
```

## Type Checking Strategies

### Strict Incremental Adoption
```json
// TODO: Add incremental strict mode adoption strategy
```

### Per-File Overrides
```typescript
// @ts-nocheck - Disable checking for entire file
// @ts-ignore - Ignore next line
// @ts-expect-error - Expect error on next line
```

## Performance Optimization

```json
{
  "compilerOptions": {
    "incremental": true,
    "skipLibCheck": true,
    "skipDefaultLibCheck": true
  }
}
```

## Testing Configuration

```json
// tsconfig.test.json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "types": ["vitest/globals", "node"]
  },
  "include": ["src/**/*.test.ts", "src/**/*.spec.ts"]
}
```

## Build Configuration

```json
// tsconfig.build.json
{
  "extends": "./tsconfig.json",
  "exclude": [
    "node_modules",
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
```

## Common Issues and Solutions

### Issue: Can't import JSON
```json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

### Issue: Path aliases not working
```json
// Ensure bundler knows about paths
// Vite: vite.config.ts resolve.alias
// Vitest: vitest.config.ts resolve.alias
```

### Issue: Type errors in node_modules
```json
{
  "compilerOptions": {
    "skipLibCheck": true
  }
}
```

## Best Practices

1. **Enable Strict Mode** - Catch more errors
2. **Use Path Aliases** - Cleaner imports
3. **Skip Lib Check** - Faster compilation
4. **Project References** - Monorepo optimization
5. **Incremental Builds** - Faster rebuilds
6. **Separate Configs** - Build, test, development
7. **Type-Only Imports** - Better tree-shaking
8. **Composite Projects** - Dependency tracking
9. **Source Maps** - Better debugging
10. **Declaration Files** - Library distribution

## Type-Safe Patterns

### Strict Null Checks
```typescript
// TODO: Add null safety examples
```

### Type Guards
```typescript
// TODO: Add type guard patterns
```

### Discriminated Unions
```typescript
// TODO: Add discriminated union patterns
```

## Additional Resources

- [CODE_QUALITY.md](./CODE_QUALITY.md) - Quality practices
- [ESLINT_CONFIG.md](./ESLINT_CONFIG.md) - Linting config
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
