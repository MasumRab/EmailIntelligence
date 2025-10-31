/// <reference types="vitest" />
import { defineConfig as defineViteConfig } from "vite";
import { defineConfig as defineTestConfig, mergeConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";
import tsconfigPaths from 'vite-tsconfig-paths';

const viteConfig = defineViteConfig({
  plugins: [
    tsconfigPaths(),
    react(),
  ],

  root: path.resolve('.', "client"),
  build: {
    outDir: path.resolve('.', "dist/public"),
    emptyOutDir: true,
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    fs: {
      strict: true,
      deny: ["**/.*"],
    },
  },
});

const testConfig = defineTestConfig({
  test: {
    root: '.', // Run Vitest from the project root
    globals: true,
    environment: 'node', // Or 'jsdom' if testing browser-like environment
    include: ['backend/**/*.test.ts'], // Adjust for backend tests
    setupFiles: './backend/tests/setup.ts', // Optional: if you have a setup file
    plugins: [tsconfigPaths()], // Add tsconfigPaths to Vitest plugins
    alias: {
      '@shared': path.resolve('.', 'shared'),
      '@': path.resolve('.', "client", "src"),
    },
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
    },
  },
});

export default mergeConfig(viteConfig, testConfig);