## 2025-04-15 - React Component Render Optimizations

**Learning:** When looking for performance improvements, simple things like checking `package.json` for validation commands (`check`, `build`) before running them saves time. Also, frontend validation currently fails out-of-the-box due to pre-existing missing alias definitions (`@components`) and a missing `vite-tsconfig-paths` dependency in `vite.config.ts`, but this should not block localized component optimizations if those optimizations are syntactically and logically sound.

**Action:** Continue ignoring pre-existing TS alias/build errors when making isolated component-level performance improvements, but document them.
