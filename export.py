from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir="C:\\Users\\Vijay\\AppData\\Local\\Google\\Chrome\\User Data",
        headless=False,
        channel="chrome",
        args=["--profile-directory=Default"]
    )

    page = context.new_page()
    page.goto("https://matiks.com")

    input("Press Enter when you see you are logged in...")

    context.storage_state(path="matiks_state.json")

    context.close()