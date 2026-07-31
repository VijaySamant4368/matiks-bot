from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="my_chrome_profile",
        headless=False,
        channel="chrome"
    )

    page = context.new_page()
    page.goto("https://matiks.com")

    input("Press Enter after login...")
    context.close()