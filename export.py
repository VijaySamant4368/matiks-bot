import json
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

STATE_FILE = "matiks_state.json"
TARGET_URL = "https://matiks.com"

def capture_auth():
    # Create a clean temporary user data directory so Google Sign-In works
    temp_dir = tempfile.mkdtemp()

    with sync_playwright() as p:
        print("Launching real Chrome profile...")
        
        # Use real installed Chrome with an isolated profile
        context = p.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            channel="chrome",  # Uses your installed Google Chrome
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled", # Prevents "Browser not secure" block
            ]
        )

        page = context.new_page()

        print(f"Navigating to {TARGET_URL}...")
        page.goto(TARGET_URL)

        print("\n" + "=" * 60)
        print("ACTION REQUIRED:")
        print("1. Log in to Matiks manually in the Chrome window that just opened.")
        print("2. Once completely logged in and at the home page, come back here.")
        print("3. Press ENTER in this console.")
        print("=" * 60 + "\n")

        input("Press ENTER after you have successfully logged in...")

        # 1. Capture the exact User-Agent from this Chrome instance
        user_agent = page.evaluate("navigator.userAgent")

        # 2. Capture storage state (cookies + localStorage)
        state_data = context.storage_state()

        # 3. Save the User-Agent directly inside the state JSON for portable reading
        state_data["captured_user_agent"] = user_agent

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2)

        print(f"\n Success! State and User-Agent saved to '{STATE_FILE}'.")
        print(f"Captured User-Agent:\n{user_agent}\n")

        context.close()

if __name__ == "__main__":
    capture_auth()