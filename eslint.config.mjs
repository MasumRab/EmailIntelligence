import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import reactRefreshPlugin from 'eslint-plugin-react-refresh';
import globals from 'globals';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    ignores: [
      "server/**",
      "tests/**",
      "dist/**",
      "build/**",
      "node_modules/**",
      "**/*.config.*",
      "test_data/**",
      "src/**",
      "scripts/**",
      "setup/**",
      "modules/**",
      "implement/**",
      "deployment/**",
      "docs/**",
      "config/**"
    ],
  },
  {
    files: ['client/src/**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2021,
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    plugins: {
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
      'react-refresh': reactRefreshPlugin,
    },
    rules: {
      ...reactPlugin.configs.recommended.rules,
      ...reactHooksPlugin.configs.recommended.rules,
      'react-refresh/only-export-components': 'off',
      'react-hooks/rules-of-hooks': 'off',
      'react-hooks/exhaustive-deps': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      'prefer-const': 'off',
      'no-var': 'off',
      'react/react-in-jsx-scope': 'off',
      'react/no-unescaped-entities': 'off',
      'react/prop-types': 'off'
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
  },
);
