# Playwright End-to-End Tests

This directory contains the Playwright End-to-End (E2E) testing harness for the client application.

## Prerequisites

Before running the E2E tests, ensure you have set up the environment and downloaded the necessary Playwright browsers and dependencies.

### Environment setup

If the environment setup script is installed, you can check its status using `$HOME/.jules_env_status`. This file is an OPTIONAL signal that exists only when the environment setup script is installed. It is not a precondition, and its absence is not evidence that Playwright is broken.

### Install Playwright Browsers and Dependencies

First, ensure you are in the `client` directory and install the necessary dependencies:

```bash
cd client
npm ci
```

Playwright requires specific OS shared libraries to launch browsers correctly. If you try to run `npx playwright install` by itself, it will download the browser but might fail later because the system lacks necessary dependencies, resulting in a failure like: `Host system is missing dependencies to run browsers`.

To install the browser alongside its required OS dependencies, run the following in order:

**If you have root access (e.g., inside a typical sandbox):**
```bash
npx playwright install --with-deps chromium
```

**If you do not have root access:**
You must ensure the system administrator has installed the required dependencies. The explicit package list for Ubuntu 24.04 includes:
`libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libpango-1.0-0 libcairo2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libasound2t64`

*Note: The `libasound2` package was renamed to `libasound2t64` on Ubuntu 24.04. Installing the old name will fail on this OS version.*

Once the OS packages are installed, you can install the browser:
```bash
npx playwright install chromium
```

## Running the E2E Tests

To run the full E2E test suite from the `client/` directory:

```bash
npm run e2e
```

### Running specific files and options

You can pass arguments to run a single file, run in headed mode, change the reporter, and enable tracing:

```bash
# Example: Run a single test file in headed mode with list reporter and tracing
npx playwright test e2e/example.spec.ts --headed --reporter=list --trace on
```

To view the generated HTML report:
```bash
npx playwright show-report
```

## Scope and Coverage

The E2E test suite covers the frontend client application running in a real browser.

**The Boundary:**
*   **No Gemini Key:** Tests do not require a live Gemini API key.
*   **No Database:** Tests do not connect to a real database.
*   **No Backend Dependency:** Tests mock or intercept backend requests unless a specific test spec dictates otherwise.

## E2E vs. Unit Tests (Vitest)

*   **Unit Tests (Vitest):** Run with `npm test`. These tests reside in `client/src/test`. They test individual components, hooks, and utilities in isolation.
*   **E2E Tests (Playwright):** Run with `npm run e2e`. These tests reside in `client/e2e`. They test the application flow from the user's perspective in a real browser environment.

Neither suite replaces the other; they are complementary.
