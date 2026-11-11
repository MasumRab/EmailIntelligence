# E2E Test Runbook

This document serves as the runbook for setting up and executing the Playwright End-to-End (E2E) test suite for the client application.

## Prerequisites and Install Ladder

The Playwright browser requires both the browser executable and specific OS-level shared libraries.

1.  **Install project dependencies:**
    ```bash
    cd client
    npm ci
    ```

2.  **Install Playwright browser and dependencies:**
    Running `npx playwright install` alone only downloads the browser. If the OS shared libraries are missing, launches will fail with `Host system is missing dependencies to run browsers`.

    *   **With root access:**
        ```bash
        npx playwright install --with-deps chromium
        ```

    *   **Without root access (Manual OS Package Installation):**
        Install the explicit package list required for Chromium.
        ```bash
        # Note: libasound2 was renamed to libasound2t64 on Ubuntu 24.04.
        sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libpango-1.0-0 libcairo2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libasound2t64 # not verified in this sandbox
        ```
        Then download the browser:
        ```bash
        npx playwright install chromium # not verified in this sandbox
        ```

### Environment Status (Optional)

The file `$HOME/.jules_env_status` is an OPTIONAL signal that exists only when the environment setup script is installed. It is not a precondition for running Playwright, and its absence is not evidence that Playwright is broken. Do not rely on it as a blocker.

## The Launch Probe

To verify that the Playwright browser can successfully launch, use the following probe script.

**Important:** The probe MUST be a `.cjs` file inside `client/`. The `client/package.json` specifies `"type": "module"`, so a standard `.js` file using `require` will throw `require is not defined in ES module scope`. Additionally, placing the probe in `/tmp` will prevent it from resolving `client/node_modules`.

Create `client/.jules-probe.cjs`:

```javascript
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const p = await b.newPage(); await p.setContent('<title>ok</title>');
  console.log((await p.title()) === 'ok' ? 'LAUNCH_OK' : 'LAUNCH_BAD'); await b.close();
})().catch(e => { console.log('LAUNCH_FAIL ' + e.message.split(String.fromCharCode(10))[0]); process.exit(3); });
```

Run the probe:
```bash
cd client && node .jules-probe.cjs
```
A completed browser download is not a launch; only `LAUNCH_OK` output proves the sandbox can run tests. Read the failure output (e.g., missing library names) to diagnose environment issues.

## Running the Suite

The E2E tests are executed from the `client/` directory.

```bash
cd client
npm run e2e # not verified in this sandbox
```

**Common commands and flags:**
*   Run a single file: `npx playwright test e2e/specific.spec.ts`
*   Run visually (headed): `--headed`
*   Change reporter: `--reporter=list`
*   Enable tracing: `--trace on`

Example running a single file with flags:
```bash
npx playwright test e2e/example.spec.ts --headed --reporter=list --trace on # not verified in this sandbox
```

To view the generated report:
```bash
npx playwright show-report # not verified in this sandbox
```

## Coverage and Boundaries

The E2E suite verifies the client application's behavior. State the boundary plainly:
*   **No Gemini key**
*   **No database**
*   **No backend dependency** unless a spec explicitly says otherwise.

Network requests to the backend are typically mocked or intercepted to ensure tests are fast, reliable, and isolated from backend state.

## Relation to Vitest

*   **Vitest Suite (`npm test`):** Unit tests stay in `client/src/test`. They test small, isolated pieces of code (functions, hooks, components).
*   **Playwright Suite (`npm run e2e`):** E2E tests stay in `client/e2e`. They test the integrated application in a real browser.

Neither replaces the other; they are distinct layers of testing.
