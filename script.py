from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🔗 Navigating to Hacker News")
        page.goto("https://news.ycombinator.com/")

        # ✅ Correct selector: now it's 'a.titlelink'
        page.wait_for_selector("a.titlelink")

        headlines = page.query_selector_all("a.titlelink")

        print("📰 Top 5 Hacker News Headlines:")
        for i, h in enumerate(headlines[:5], start=1):
            print(f"{i}. {h.inner_text()}")

        browser.close()

run()
