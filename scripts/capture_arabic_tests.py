import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/chromium", headless=True)

        # 1. Desktop Viewport (1440x900)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://localhost:2949/")
        page.wait_for_timeout(1500)
        page.screenshot(path="/tmp/lh_test_1_desktop_home.png")

        # Open Arabic test chat
        chat_item = page.locator("text=اختبار مصفوفة اللغة العربية").first
        if chat_item.is_visible():
            chat_item.click()
            page.wait_for_timeout(2000)

            # 1. Scroll to Top (Quran & Intro)
            top_elem = page.locator("text=القرآن الكريم").first
            if top_elem.is_visible():
                top_elem.scroll_into_view_if_needed()
                page.wait_for_timeout(800)
            else:
                page.evaluate("() => { const el = document.querySelector('[role=\"log\"] > div'); if (el) el.scrollTop = 0; }")
                page.wait_for_timeout(800)
            page.screenshot(path="/tmp/lh_test_2_desktop_chat.png", full_page=False)

            # 2. Scroll to LaTeX Math & Code blocks
            math_elem = page.locator("text=الرياضيات والمعادلات").first
            if math_elem.is_visible():
                math_elem.scroll_into_view_if_needed()
                page.wait_for_timeout(800)
            page.screenshot(path="/tmp/lh_test_3_desktop_chat_math_code.png")

            # 3. Scroll to Tables, CJK, and Mixed text
            table_elem = page.locator("text=الجداول المنسقة").first
            if table_elem.is_visible():
                table_elem.scroll_into_view_if_needed()
                page.wait_for_timeout(800)
            page.screenshot(path="/tmp/lh_test_4_desktop_chat_tables_cjk.png")

        # 2. Open Settings dialog
        settings_btn = page.locator("[data-testid='settings-toggle'], button:has-text('الإعدادات')").first
        if settings_btn.is_visible():
            settings_btn.click()
            page.wait_for_timeout(1000)
            page.screenshot(path="/tmp/lh_test_5_settings_dialog.png")
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

        # 3. Tablet Viewport (1024x768)
        tablet_page = browser.new_page(viewport={"width": 1024, "height": 768})
        tablet_page.goto("http://localhost:2949/")
        tablet_page.wait_for_timeout(1500)
        tablet_page.locator("text=اختبار مصفوفة اللغة العربية").first.click()
        tablet_page.wait_for_timeout(1500)
        tablet_page.screenshot(path="/tmp/lh_test_6_tablet_chat.png")

        # 4. Narrow / Mobile Viewport (768x1024)
        mobile_page = browser.new_page(viewport={"width": 768, "height": 1024})
        mobile_page.goto("http://localhost:2949/")
        mobile_page.wait_for_timeout(1500)
        mobile_page.screenshot(path="/tmp/lh_test_7_narrow_home.png")

        browser.close()
        print("All test screenshots captured successfully.")

if __name__ == "__main__":
    run()
