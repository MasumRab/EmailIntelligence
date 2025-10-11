from playwright.sync_api import expect, sync_playwright


def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console errors
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        # Capture failed network requests
        failed_requests = []

        def handle_response(response):
            if not response.ok:
                failed_requests.append(f"URL: {response.url}, Status: {response.status}")

        page.on("response", handle_response)

        try:
            # Navigate to the frontend application
            page.goto("http://localhost:5173/", timeout=30000)

            # Since the page isn't loading fully, we can't wait for a specific element.
            # Instead, we'll just wait for a short period to allow network requests to be made.
            page.wait_for_timeout(5000)  # Wait 5 seconds

            # Take a screenshot of whatever has loaded.
            screenshot_path = "jules-scratch/verification/verification.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot of current state saved to {screenshot_path}")

        except Exception as e:
            print(f"An error occurred during verification: {e}")

        finally:
            if errors:
                print("\nCaptured Console Errors:")
                for error in errors:
                    print(error)
            if failed_requests:
                print("\nCaptured Failed Network Requests:")
                for req in failed_requests:
                    print(req)
            browser.close()


if __name__ == "__main__":
    run_verification()
