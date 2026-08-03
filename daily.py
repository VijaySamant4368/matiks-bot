import json
from playwright.sync_api import sync_playwright
import random

URL = "https://matiks.com/search?gameType=DMAS&gameMode=ONLINE_SEARCH&timeLimit=1"
STATE_FILE = "matiks_state.json"

with open(STATE_FILE, "r", encoding="utf-8") as f:
    state_data = json.load(f)
    captured_ua = state_data.get("captured_user_agent")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    context = browser.new_context(
        storage_state=STATE_FILE,
        user_agent=captured_ua,
        viewport={"width": 1280, "height": 720}
    )

    page = context.new_page()

    page.goto(URL)
    print("Reached page:", page.url)

    for i in range(20):
        page.wait_for_timeout(random.randint(10, 15) * 1000)

        length = random.randint(1, 3)
        value = "".join(random.choice("0123456789") for _ in range(length))

        print(f"[{i+1}/20] Sending:", value)

        page.keyboard.type(value)
        page.keyboard.press("Enter")

        page.screenshot(path=f"debug_{i+1}.png", full_page=True)

    print("Done! Final URL:", page.url)

    context.close()
    browser.close()