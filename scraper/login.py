import os
import json
import subprocess
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
AUTH_STATE_PATH = DATA_DIR / "auth_state.json"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"


def get_credentials():
    phone = os.getenv("APIFOX_PHONE", "")
    password = os.getenv("APIFOX_PASSWORD", "")
    if not phone or not password:
        from dotenv import load_dotenv
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")
        phone = os.getenv("APIFOX_PHONE", "")
        password = os.getenv("APIFOX_PASSWORD", "")
    if not phone or not password:
        raise ValueError("APIFOX_PHONE and APIFOX_PASSWORD must be set in .env or environment variables")
    return phone, password


def _do_login(headless: bool = True):
    phone, password = get_credentials()
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto("https://app.apifox.com/user/login", wait_until="networkidle")
        page.wait_for_timeout(5000)
        page.screenshot(path=str(SCREENSHOTS_DIR / "01_login_initial.png"))

        sms_btn = page.locator("button:has-text('SMS'), button:has-text('Email'), button:has-text('短信'), button:has-text('邮箱')")
        if sms_btn.count() > 0:
            sms_btn.first.click()
            page.wait_for_timeout(3000)
            page.screenshot(path=str(SCREENSHOTS_DIR / "02_login_form.png"))

        mobile_tab = page.locator("#rc-tabs-0-tab-MobilePassword, [id*='tab-MobilePassword']")
        if mobile_tab.count() > 0:
            mobile_tab.first.click()
            page.wait_for_timeout(2000)
            page.screenshot(path=str(SCREENSHOTS_DIR / "03_mobile_tab.png"))

        mobile_input = page.locator("input#mobile")
        mobile_input.fill(phone)

        mobile_panel = page.locator("#rc-tabs-0-panel-MobilePassword")
        pwd_input = mobile_panel.locator("input#password")
        pwd_input.fill(password)

        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENSHOTS_DIR / "04_filled.png"))

        captcha_slot = mobile_panel.locator("#CaptchaMetaSlot")
        captcha_content = captcha_slot.inner_html() if captcha_slot.count() > 0 else ""
        print(f"Captcha slot content: '{captcha_content}'")

        login_btn = mobile_panel.locator("button[type='submit']").first
        login_btn.click()

        page.wait_for_timeout(8000)
        current_url = page.url
        page.screenshot(path=str(SCREENSHOTS_DIR / "05_after_login.png"))

        if "login" in current_url.lower():
            captcha_after = mobile_panel.locator("#CaptchaMetaSlot").inner_html() if mobile_panel.locator("#CaptchaMetaSlot").count() > 0 else ""
            page_text = page.inner_text("body")[:1000]
            error_els = page.evaluate("""() => {
                const all = document.querySelectorAll('[class*="error"], [class*="invalid"], [role="alert"]');
                return Array.from(all).map(e => e.innerText.trim()).filter(t => t && t.length < 200);
            }""")
            raise RuntimeError(
                f"Login failed. URL: {current_url}\n"
                f"Captcha after: '{captcha_after}'\n"
                f"Errors: {error_els}\n"
                f"Page text: {page_text}"
            )

        page.wait_for_load_state("networkidle")
        context.storage_state(path=str(AUTH_STATE_PATH))
        browser.close()


def login_and_save_state(headless: bool = True) -> dict:
    env = os.environ.copy()
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    env["APIFOX_PHONE"] = os.getenv("APIFOX_PHONE", "")
    env["APIFOX_PASSWORD"] = os.getenv("APIFOX_PASSWORD", "")

    result = subprocess.run(
        [sys.executable, "-c",
         "from scraper.login import _do_login; _do_login(headless=True)"],
        capture_output=True, text=True,
        cwd=str(Path(__file__).resolve().parent.parent),
        env=env
    )
    if result.returncode != 0:
        raise RuntimeError(f"Login failed: {result.stderr}")
    if not AUTH_STATE_PATH.exists():
        raise RuntimeError("Login completed but auth state file not found")
    return {"state_path": str(AUTH_STATE_PATH)}


def ensure_auth_state(headless: bool = True):
    if not AUTH_STATE_PATH.exists():
        print("No auth state found, logging in...")
        login_and_save_state(headless=headless)
    else:
        print(f"Using existing auth state: {AUTH_STATE_PATH}")


def create_authenticated_context(browser: Browser) -> BrowserContext:
    if not AUTH_STATE_PATH.exists():
        raise FileNotFoundError(
            f"Auth state not found at {AUTH_STATE_PATH}. "
            "Run login_and_save_state() first (outside of any playwright context)."
        )
    return browser.new_context(
        storage_state=str(AUTH_STATE_PATH),
        viewport={"width": 1920, "height": 1080}
    )


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    _do_login(headless=True)
    print(f"Login successful. State saved to: {AUTH_STATE_PATH}")
