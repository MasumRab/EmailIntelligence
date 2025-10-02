import re
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        # Navigate to the Gradio app
        page.goto("http://127.0.0.1:7860", timeout=60000)

        # Wait for the UI to be ready
        expect(page.get_by_label("Email Subject")).to_be_visible(timeout=30000)

        # Input data
        page.get_by_label("Email Subject").fill("Important Project Update")
        page.get_by_label("Email Content").fill("This is a test to confirm the new UI is working correctly and that the visualizations are displayed.")

        # Click the analyze button
        page.get_by_role("button", name="Analyze Email").click()

        # Wait for the analysis to complete by checking for an output
        expect(page.get_by_label("Topic")).not_to_be_empty(timeout=30000)
        expect(page.get_by_label("Sentiment")).not_to_be_empty()

        # Switch to the visualizations tab
        page.get_by_role("tab", name="Visualizations").click()

        # Wait for the plots to be visible
        expect(page.locator("div.plot-container.plotly")).to_have_count(2, timeout=20000)

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

        print("Verification script ran successfully and screenshot was taken.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)