from playwright.sync_api import sync_playwright
import random
import time

URL = "https://matiks.com/search?gameType=DMAS&gameMode=ONLINE_SEARCH&timeLimit=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        storage_state="matiks_state.json"
    )

    page = context.new_page()

    page.goto(URL)
    # page.wait_for_load_state("networkidle")
    print("Reached page", URL)
    for i in range(20):
        page.wait_for_timeout(random.randint(10, 15) * 1000)

        length = random.randint(1, 3)
        value = "".join(random.choice("0123456789") for _ in range(length))

        print("Sending:", value)

        page.keyboard.type(value)
        page.keyboard.press("Enter")

    print("Done:", page.url)

    context.close()
    browser.close()