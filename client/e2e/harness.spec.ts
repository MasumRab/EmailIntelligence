import { test, expect } from '@playwright/test';

test.describe('Environment Harness', () => {
  test('React root mounts and document responds', async ({ page }) => {
    const response = await page.goto('/');
    expect(response?.ok()).toBeTruthy();
    
    // Check that title is non-empty
    const title = await page.title();
    expect(title.length).toBeGreaterThan(0);
    
    const root = page.locator('#root');
    await expect(root).toBeAttached();
  });
});
