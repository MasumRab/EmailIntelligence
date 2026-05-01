// ESLint Configuration for EmailIntelligence (ESLint 9+ Flat Config)
// https://eslint.org/docs/latest/use/configure/configuration-files

import js from '@eslint/js';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import typescriptPlugin from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';
import reactRefreshPlugin from 'eslint-plugin-react-refresh';

export default [
  // Base configuration
  js.configs.recommended,

  // TypeScript files configuration
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    plugins: {
      '@typescript-eslint': typescriptPlugin,
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
      'react-refresh': reactRefreshPlugin,
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      // TypeScript rules
      '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',

      // React Hooks rules
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // React rules
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
      'react/react-in-jsx-scope': 'off',

      // General rules
      'prefer-const': 'warn',
      'no-var': 'error',
    },
  },

  // JavaScript files configuration (non-TypeScript)
  {
    files: ['**/*.js', '**/*.jsx', '**/*.mjs'],
    plugins: {
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
      'react-refresh': reactRefreshPlugin,
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
      'react/react-in-jsx-scope': 'off',
      'prefer-const': 'warn',
      'no-var': 'error',
    },
  },

  // Ignore patterns
  {
    ignores: [
      'node_modules/**',
      'dist/**',
      'build/**',
      'coverage/**',
      '*.min.js',
      '**/node_modules/**',
      '**/dist/**',
      '**/build/**',
    ],
  },
];