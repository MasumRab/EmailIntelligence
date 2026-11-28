import path from "node:path";
import { defineConfig } from "vitest/config";

/**
 * Vitest configuration for the client app.
 *
 * A separate `vitest.config.ts` rather than a `test` block in a `vite.config.ts`: the client has
 * no vite config of its own (it relies on vite's defaults for `vite build`), and adding one to
 * hold test settings would silently change how the app itself is built.
 *
 * The aliases mirror `tsconfig.json`'s `paths`, so a test resolves `@/…` and `@shared/…` exactly
 * as the application code does — a test that resolves modules differently from the app can pass
 * while the app is broken.
 *
 * No `@vitejs/plugin-react`: it only adds Fast Refresh, which has no meaning under Vitest, and
 * the installed plugin version imports `vite/internal`, which vite 7 does not export. JSX still
 * compiles through esbuild using the `jsx: react-jsx` setting in `tsconfig.json`.
 */
export default defineConfig({
  resolve: {
    alias: {
      "@shared": path.resolve(__dirname, "../shared"),
      "@": path.resolve(__dirname, "src"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"],
    setupFiles: ["./src/test/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
    },
  },
});
