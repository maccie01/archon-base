# Prettier Configuration Best Practices

Created: 2025-10-13
Last Research: 2025-10-13
Sources: Prettier documentation, code formatting standards

## Overview

Prettier is an opinionated code formatter that enforces consistent code style. It integrates with editors and CI pipelines to automatically format code.

## Core Principles

1. **Opinionated** - Minimal configuration options
2. **Automatic** - Format on save or commit
3. **Consistent** - Same output always
4. **Language Support** - JavaScript, TypeScript, CSS, HTML, JSON, Markdown
5. **Integration** - Works with ESLint

## Installation

```bash
npm install -D prettier
```

## Configuration

### .prettierrc.json
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### Recommended Settings
```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "always"
}
```

## Ignoring Files

### .prettierignore
```
node_modules/
dist/
build/
coverage/
*.min.js
package-lock.json
pnpm-lock.yaml
```

## Integration with ESLint

### Installation
```bash
npm install -D eslint-config-prettier eslint-plugin-prettier
```

### ESLint Config
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

## Editor Integration

### VS Code
```json
// .vscode/settings.json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Pre-commit Hook

```bash
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

### package.json
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["prettier --write", "eslint --fix"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

## Scripts

### package.json
```json
{
  "scripts": {
    "format": "prettier --write \"**/*.{js,jsx,ts,tsx,json,md,css}\"",
    "format:check": "prettier --check \"**/*.{js,jsx,ts,tsx,json,md,css}\""
  }
}
```

## CI Integration

```yaml
# TODO: Add GitHub Actions Prettier check
```

## Best Practices

1. Use default settings when possible
2. Format on save in editor
3. Enforce in pre-commit hooks
4. Check in CI pipeline
5. Format entire codebase initially
6. Keep config minimal
7. Combine with ESLint
8. Document any custom rules
9. Use prettierignore appropriately
10. Update regularly

## Additional Resources

- [CODE_QUALITY.md](./CODE_QUALITY.md) - Quality practices
- [ESLINT_CONFIG.md](./ESLINT_CONFIG.md) - ESLint setup
- [Prettier Documentation](https://prettier.io/)
