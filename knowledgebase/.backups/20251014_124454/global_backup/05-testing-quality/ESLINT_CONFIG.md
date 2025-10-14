# ESLint Configuration Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: ESLint documentation, TypeScript-ESLint, React ESLint best practices

## Overview

ESLint is a pluggable linting utility for JavaScript and TypeScript. It helps identify and fix code quality issues, enforce coding standards, and prevent bugs.

## Core Principles

1. **Consistency** - Uniform code style
2. **Error Prevention** - Catch bugs early
3. **Best Practices** - Enforce proven patterns
4. **Team Standards** - Shared coding rules
5. **Automatic Fixing** - Auto-fix when possible

## Installation

```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

## Basic Configuration

### ESLint Config (.eslintrc.json)
```json
{
  "root": true,
  "env": {
    "browser": true,
    "es2022": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "plugins": ["@typescript-eslint"],
  "rules": {
    // TODO: Add recommended rules
  }
}
```

## Recommended Rule Sets

### TypeScript Rules
```json
{
  "extends": [
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": ["error", {
      "argsIgnorePattern": "^_"
    }]
  }
}
```

### React Rules
```json
{
  "extends": [
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

### Security Rules
```json
{
  "plugins": ["security"],
  "extends": ["plugin:security/recommended"]
}
```

## Common Rules to Configure

```json
{
  "rules": {
    // Error prevention
    "no-console": "warn",
    "no-debugger": "error",
    "no-unused-vars": "off",

    // Best practices
    "eqeqeq": ["error", "always"],
    "no-var": "error",
    "prefer-const": "error",
    "prefer-arrow-callback": "error",

    // Code style (use Prettier instead)
    "semi": "off",
    "quotes": "off"
  }
}
```

## Project-Specific Configurations

### Frontend (React)
```json
// TODO: Add complete React ESLint config
```

### Backend (Node.js)
```json
// TODO: Add complete Node.js ESLint config
```

### Monorepo
```json
// TODO: Add monorepo ESLint config with overrides
```

## Integration with Tools

### VS Code
```json
// .vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "typescript",
    "javascriptreact",
    "typescriptreact"
  ]
}
```

### Pre-commit Hook
```bash
# TODO: Add husky + lint-staged config
```

### CI/CD
```yaml
# TODO: Add GitHub Actions ESLint check
```

## Ignoring Files

### .eslintignore
```
node_modules/
dist/
build/
coverage/
*.config.js
*.min.js
```

## Performance Optimization

```json
{
  "parserOptions": {
    "project": "./tsconfig.json",
    "EXPERIMENTAL_useProjectService": true
  }
}
```

## Custom Rules

```javascript
// TODO: Add custom ESLint rule example
```

## Common Configurations by Framework

### Next.js
```json
{
  "extends": ["next/core-web-vitals"]
}
```

### Vite + React
```json
// TODO: Add Vite React config
```

## Troubleshooting

### Parsing Errors
- Check TypeScript version compatibility
- Verify tsconfig.json path
- Check for syntax errors

### Performance Issues
- Enable project service
- Use cache
- Exclude large directories

## Best Practices

1. Start with recommended configs
2. Add rules gradually
3. Document custom rules
4. Use auto-fix capabilities
5. Integrate with CI/CD
6. Keep config consistent across team
7. Use overrides for specific files
8. Combine with Prettier
9. Review and update regularly
10. Use plugins wisely

## Additional Resources

- [CODE_QUALITY.md](./CODE_QUALITY.md) - Overall quality practices
- [PRETTIER_CONFIG.md](./PRETTIER_CONFIG.md) - Formatting config
- [TYPESCRIPT_CONFIG.md](./TYPESCRIPT_CONFIG.md) - TypeScript setup
- [ESLint Documentation](https://eslint.org/)
