# Build Configuration Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Vite, Webpack, bundler best practices

## Overview

Build configuration determines how your application is bundled, optimized, and prepared for deployment. Modern bundlers like Vite offer fast builds and excellent developer experience.

## Core Principles

1. **Fast Builds** - Optimize for speed
2. **Code Splitting** - Smaller bundles
3. **Tree Shaking** - Remove unused code
4. **Source Maps** - Debug production
5. **Environment-Specific** - Different builds per env

## Vite Configuration

### Basic vite.config.ts
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components')
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'esbuild',
    target: 'esnext'
  },
  server: {
    port: 5173,
    open: true
  }
})
```

### Environment-Specific Config
```typescript
// TODO: Add environment-specific Vite config
// Development, staging, production
```

## Optimization

### Code Splitting
```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom'],
        utils: ['lodash', 'date-fns']
      }
    }
  }
}
```

### Tree Shaking
Enabled by default in production builds.

### Compression
```typescript
// TODO: Add compression plugin
// gzip, brotli
```

## Path Aliases

```typescript
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
    '@components': path.resolve(__dirname, './src/components'),
    '@utils': path.resolve(__dirname, './src/utils'),
    '@shared': path.resolve(__dirname, '../../packages/shared-types')
  }
}
```

## Environment Variables

### Vite
```typescript
// .env
VITE_API_URL=http://localhost:3000
VITE_APP_VERSION=1.0.0

// Usage
const apiUrl = import.meta.env.VITE_API_URL
```

## Build Scripts

### package.json
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "build:prod": "tsc && vite build --mode production",
    "preview": "vite preview",
    "analyze": "vite-bundle-visualizer"
  }
}
```

## Backend Build (TypeScript)

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true
  }
}
```

### Build Script
```json
{
  "scripts": {
    "build": "tsc",
    "build:watch": "tsc --watch"
  }
}
```

## Best Practices

1. Use modern bundler (Vite)
2. Enable source maps for debugging
3. Split code by route/feature
4. Tree shake unused code
5. Compress assets
6. Use path aliases
7. Optimize images
8. Cache dependencies
9. Analyze bundle size
10. Test production builds

## Additional Resources

- [DEPLOYMENT_CONFIG.md](./DEPLOYMENT_CONFIG.md) - Deployment setup
- [MONOREPO_PATTERNS.md](./MONOREPO_PATTERNS.md) - Monorepo builds
- [Vite Documentation](https://vitejs.dev/)
