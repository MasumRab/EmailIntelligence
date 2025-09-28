import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node', // Explicitly set node environment for backend tests
    include: ['./**/*.test.ts'], // Corrected pattern relative to this config file's location (server/)
    jest: true, // Enable Jest global object compatibility
    // Optionally, set a root for the test runner if paths are still an issue
    // root: path.resolve(__dirname, '.'), // Project root
    // setupFiles: ['./server/tests/setup.ts'], // If you have a test setup file for server tests
  },
  // Need to resolve aliases if server code uses them, similar to vite.config.ts
  resolve: {
    alias: {
      '@shared': path.resolve(__dirname, '../shared'), // Corrected path
      // Add other aliases used by server-side code if necessary
      // e.g., '@server': path.resolve(__dirname, '.') // Server directory itself
    },
  },
});
