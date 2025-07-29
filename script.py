from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to a working URL
        page.goto("https://news.ycombinator.com")

        # Wait for headlines to be visible
        page.wait_for_selector("a.storylink")

        # Extract the first 5 headlines
        headlines = page.query_selector_all("a.storylink")[:5]
        for i, h in enumerate(headlines, start=1):
            print(f"{i}. {h.inner_text()}")

        browser.close()

if __name__ == "__main__":
    run()
