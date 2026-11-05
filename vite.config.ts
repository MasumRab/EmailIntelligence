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
  resolve: {
    alias: {
      "@": path.resolve('.', "client", "src"),
      "@assets": path.resolve('.', "attached_assets"),
    },
  },
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
    // The client is React + DOM; the previous 'node' environment made every component
    // test fail at the first document access. Override per-file with
    // `// @vitest-environment node` for the pure-logic tests.
    environment: 'jsdom',
    include: ['client/src/**/*.test.{ts,tsx}'],
    setupFiles: ['./client/src/test/setup.ts'],
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