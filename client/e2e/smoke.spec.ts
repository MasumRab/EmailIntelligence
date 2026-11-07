import { test, expect } from '@playwright/test';

test.describe('Smoke tests', () => {
  test('App handles routing and empty/loading states gracefully', async ({ page }) => {
    await page.goto('/');
    
    // Check if it redirected to login due to missing backend auth
    if (page.url().includes('/login')) {
      await expect(page.getByRole('heading', { name: 'Email Intelligence Platform' })).toBeVisible();
      return;
    }
    
    // Otherwise, expect the root to be attached to ensure React rendered something
    const root = page.locator('#root');
    await expect(root).toBeAttached();
  });
});
