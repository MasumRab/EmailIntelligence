import { test, expect } from '@playwright/test';

test.describe('Interaction tests', () => {
  test('Login form accepts text and keeps the submit button enabled', async ({ page }) => {
    await page.goto('/login');

    await expect(
      page.getByRole('heading', { name: 'Email Intelligence Platform' })
    ).toBeVisible();

    const usernameInput = page.getByLabel('Username');
    await usernameInput.fill('testuser');
    await expect(usernameInput).toHaveValue('testuser');

    const passwordInput = page.getByLabel('Password');
    await passwordInput.fill('password123');
    await expect(passwordInput).toHaveValue('password123');

    const loginButton = page.getByRole('button', { name: 'Login' });
    await expect(loginButton).toBeEnabled();
  });

  test('Unrouted paths fall back to the dashboard shell', async ({ page }) => {
    // client/src/App.tsx declares "/", "/login" and "/profile" only. wouter's default
    // route renders the Dashboard for anything else — there is no auth guard and no
    // login redirect, so assert the shell that actually renders.
    await page.goto('/dashboard');
    await expect(page.getByRole('heading', { name: 'GmailAI' })).toBeVisible();
  });
});
