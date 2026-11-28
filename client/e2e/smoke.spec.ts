import { test, expect } from '@playwright/test';

test.describe('Smoke tests', () => {
  test('App mounts and serves both entry routes', async ({ page }) => {
    await page.goto('/');

    // `#root` is the mount point in client/index.html.
    await expect(page.locator('#root')).toBeAttached();

    // "/" is the Dashboard route in client/src/App.tsx, which renders the Sidebar.
    await expect(page.getByRole('heading', { name: 'GmailAI' })).toBeVisible();

    // "/login" is a separate route; it must render its own page, not the dashboard.
    await page.goto('/login');
    await expect(
      page.getByRole('heading', { name: 'Email Intelligence Platform' })
    ).toBeVisible();
  });
});
