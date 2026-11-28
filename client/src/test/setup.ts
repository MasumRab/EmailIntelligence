/**
 * Vitest setup for the client.
 *
 * `vite.config.ts` pointed `setupFiles` at `./backend/tests/setup.ts`, which has never
 * existed, so `vitest run` failed before collecting a single test. This file is the
 * real one.
 */
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// Testing Library does not unmount between tests under Vitest's globals, so a component
// left mounted in one file would be found by the queries in the next.
afterEach(() => {
  cleanup();
});
