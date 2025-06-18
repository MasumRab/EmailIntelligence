/// <reference types="vitest" />
import { defineConfig as defineViteConfig } from "vite";
import { defineConfig as defineTestConfig, mergeConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";
import runtimeErrorOverlay from "@replit/vite-plugin-runtime-error-modal";
import tsconfigPaths from 'vite-tsconfig-paths';

const viteConfig = defineViteConfig({
  plugins: [
    tsconfigPaths(),
    react(),
    runtimeErrorOverlay(),
    ...(process.env.NODE_ENV !== "production" &&
    process.env.REPL_ID !== undefined
      ? [
          await import("@replit/vite-plugin-cartographer").then((m) =>
            m.cartographer(),
          ),
        ]
      : []),
  ],
  resolve: {
    alias: {
      "@": path.resolve('.', "client", "src"),
      // "@shared": path.resolve('.', "shared"), // Removed, to be handled by vite-tsconfig-paths
      "@assets": path.resolve('.', "attached_assets"),
    },
  },
  root: path.resolve('.', "client"),
  build: {
    outDir: path.resolve('.', "dist/public"),
    emptyOutDir: true,
  },
  server: {
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
    include: ['server/**/*.test.ts'], // Adjust if your tests are elsewhere
    // setupFiles: './server/tests/setup.ts', // Optional: if you have a setup file
    plugins: [tsconfigPaths()], // Add tsconfigPaths to Vitest plugins
    // alias: { // Removed
    //   '@shared': path.resolve(__dirname, './shared'),
    // You might need to replicate other aliases from viteConfig.resolve.alias if tests need them
    // For example:
    // "@": path.resolve(__dirname, './client/src'),
    // },
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
    },
  },
});

export default mergeConfig(viteConfig, testConfig);
