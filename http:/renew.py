renew.py

import os
import time
from playwright.sync_api import sync_playwright

EMAIL = os.environ.get("KATABUMP_EMAIL")
PASSWORD = os.environ.get("KATABUMP_PASSWORD")
SERVER_ID = os.environ.get("SERVER_ID", "d1712508")

def main():
    if not EMAIL or not PASSWORD:
        print("â‌Œ ط®ط·ط§: ظ…طھط؛غŒط±ظ‡ط§غŒ KATABUMP_EMAIL غŒط§ KATABUMP_PASSWORD ط¯ط± Secrets طھط¹ط±غŒظپ ظ†ط´ط¯ظ‡â€Œط§ظ†ط¯.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        try:
            print("ًں”„ ط¯ط± ط­ط§ظ„ ظˆط±ظˆط¯ ط¨ظ‡ طµظپط­ظ‡ ظ„ط§ع¯غŒظ† Katabump...")
            page.goto("https://control.katabump.com/auth/login", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            print("ًں”‘ ط¯ط± ط­ط§ظ„ ظˆط§ط±ط¯ ع©ط±ط¯ظ† ط§ط·ظ„ط§ط¹ط§طھ ظ„ط§ع¯غŒظ†...")
            # ظ¾غŒط¯ط§ ع©ط±ط¯ظ† ظپغŒظ„ط¯ ط§غŒظ…غŒظ„/ظ†ط§ظ…â€Œع©ط§ط±ط¨ط±غŒ ط¨ط§ ع†ظ†ط¯ ط³ظ„ع©طھظˆط± ظ¾ط´طھغŒط¨ط§ظ†
            user_input = page.locator('input[name="username"], input[name="email"], input[type="text"], input[type="email"]').first
            pass_input = page.locator('input[name="password"], input[type="password"]').first

            user_input.fill(EMAIL)
            pass_input.fill(PASSWORD)

            # ع©ظ„غŒع© ط±ظˆغŒ ط¯ع©ظ…ظ‡ ظˆط±ظˆط¯
            submit_btn = page.locator('button[type="submit"], input[type="submit"]').first
            submit_btn.click()

            page.wait_for_timeout(8000)

            print(f"ًںŒگ ط¯ط± ط­ط§ظ„ ظ‡ط¯ط§غŒطھ ط¨ظ‡ ط³ط±ظˆط± {SERVER_ID}...")
            page.goto(f"https://control.katabump.com/server/{SERVER_ID}", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            # ط¨ط±ط±ط³غŒ ظˆ ع©ظ„غŒع© ط¯ع©ظ…ظ‡ Renew
            renew_btn = page.locator('button:has-text("Renew"), a:has-text("Renew")')
            if renew_btn.count() > 0 and renew_btn.first.is_visible():
                renew_btn.first.click()
                print("ًںژ‰ ط¯ع©ظ…ظ‡ Renew ط¨ط§ ظ…ظˆظپظ‚غŒطھ ع©ظ„غŒع© ط´ط¯!")
                page.wait_for_timeout(3000)
            else:
                print("â„¹ï¸ڈ ط¯ع©ظ…ظ‡ Renew ط¯ط± ط­ط§ظ„ ط­ط§ط¶ط± ظپط¹ط§ظ„ ظ†غŒط³طھ غŒط§ ط³ط±ظˆط± ظ†غŒط§ط²غŒ ط¨ظ‡ طھظ…ط¯غŒط¯ ظ†ط¯ط§ط±ط¯.")

        except Exception as e:
            print(f"â‌Œ ط®ط·ط§غŒغŒ ط±ط® ط¯ط§ط¯: {e}")
            # ط°ط®غŒط±ظ‡ طھطµظˆغŒط± ط§ط² طµظپط­ظ‡ ط¬ظ‡طھ ط¹غŒط¨â€ŒغŒط§ط¨غŒ ط¯ظ‚غŒظ‚
            page.screenshot(path="error_screenshot.png")
            raise e
        finally:
            browser.close()
