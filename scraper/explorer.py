import json
from pathlib import Path
from playwright.sync_api import sync_playwright, Page
from .login import create_authenticated_context, ensure_auth_state

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
PROJECT_URL = "https://app.apifox.com/project/7631843"


def explore_project_page(headless: bool = True):
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    ensure_auth_state(headless=headless)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = create_authenticated_context(browser)
        page = context.new_page()

        api_responses = []

        def handle_response(response):
            url = response.url
            if "api.apifox.com" in url or "apifox.com/api" in url:
                try:
                    body = response.text()
                    api_responses.append({
                        "url": url,
                        "status": response.status,
                        "body_preview": body[:2000] if body else ""
                    })
                except Exception:
                    pass

        page.on("response", handle_response)

        page.goto(PROJECT_URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(SCREENSHOTS_DIR / "03_project_page.png"), full_page=True)

        page_structure = {
            "project_url": PROJECT_URL,
            "page_title": page.title(),
            "current_url": page.url,
            "nav_items": [],
            "sidebar_items": [],
            "api_responses": api_responses,
            "page_text_preview": "",
        }

        try:
            nav_links = page.locator("nav a, [role='tab'], .ant-menu-item, .ant-tabs-tab").all()
            for link in nav_links[:30]:
                text = link.inner_text().strip()
                href = link.get_attribute("href") or ""
                if text:
                    page_structure["nav_items"].append({"text": text, "href": href})
        except Exception as e:
            page_structure["nav_items_error"] = str(e)

        try:
            sidebar_items = page.locator(".ant-tree-treenode, .sidebar-item, [class*='sidebar'] [class*='item']").all()
            for item in sidebar_items[:50]:
                text = item.inner_text().strip()
                if text:
                    page_structure["sidebar_items"].append(text)
        except Exception as e:
            page_structure["sidebar_items_error"] = str(e)

        try:
            page_structure["page_text_preview"] = page.inner_text("body")[:3000]
        except Exception as e:
            page_structure["page_text_preview_error"] = str(e)

        test_report_entries = []
        try:
            report_tab = page.locator("text=测试报告, text=测试, text=报告, text=自动化测试").first
            if report_tab.is_visible():
                report_tab.click()
                page.wait_for_timeout(3000)
                page.screenshot(path=str(SCREENSHOTS_DIR / "04_test_report_tab.png"), full_page=True)

                report_items = page.locator("[class*='report'] [class*='item'], [class*='report'] [class*='card'], tr[class*='report'], .ant-list-item").all()
                for item in report_items[:20]:
                    text = item.inner_text().strip()
                    link = item.locator("a").first
                    href = link.get_attribute("href") or "" if link.is_visible() else ""
                    test_report_entries.append({"text": text, "href": href})

                page_structure["test_report_page_text"] = page.inner_text("body")[:3000]
        except Exception as e:
            page_structure["test_report_error"] = str(e)

        page_structure["test_report_entries"] = test_report_entries

        all_links = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a[href]')).map(a => ({
                text: a.innerText.trim().substring(0, 100),
                href: a.getAttribute('href')
            })).filter(l => l.text || l.href);
        }""")
        page_structure["all_links"] = all_links[:100]

        output_path = DATA_DIR / "page_structure.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(page_structure, f, ensure_ascii=False, indent=2)

        print(f"Page structure saved to: {output_path}")
        print(f"Screenshots saved to: {SCREENSHOTS_DIR}")
        print(f"Found {len(api_responses)} API responses")
        print(f"Found {len(test_report_entries)} test report entries")
        print(f"Found {len(all_links)} links on page")

        browser.close()

    return page_structure


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    explore_project_page(headless=True)
