from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto("https://arll.artravells.in/")

        
        page.wait_for_selector('input[name="login"]', timeout=15000)  # Wait 15s max
        page.fill('input[name="login"]', 'mahesh')

        
        page.wait_for_selector('input[name="password"]', timeout=15000)  # Wait 15s max
        page.fill('input[name="password"]', '123456')
         
        page.click('input#login_button')
        page.wait_for_load_state("networkidle")

        page.click('a.header-menu-bar')
        page.click('a#reports_id')
        page.click('a[id="3"]')

        page.evaluate("""
            () => {
                const el = document.querySelector('#report_id');
                el.value = '147';
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)

        page.evaluate("""
            () => {
                const el = document.querySelector('#report_service_all');
                el.value = '-1';
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)

        page.wait_for_function("""
            () => {
                const el = document.querySelector('#report_coach_id');
                return el && el.options.length > 1;
            }
        """)

        page.click("#report_coach_id_chosen .chosen-single")
        page.locator("ul.chosen-results li", has_text="- All -").click()

        page.wait_for_function("""
            () => {
                const el = document.querySelector('#hub_options');
                return el && el.options.length > 1;
            }
        """)

        page.evaluate("""
            () => {
                const el = document.querySelector('#hub_options');
                el.value = '1';
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)

        page.wait_for_function("""
            () => {
                const el = document.querySelector('#report_date_range');
                return el && el.options.length > 1;
            }
        """)

        page.click("#report_date_range_chosen .chosen-single")
        page.locator("ul.chosen-results li", has_text="Yesterday").click()

        page.wait_for_timeout(2000)
        page.click('input[type="submit"][value="Run Report"]')
        page.wait_for_selector("table#report_results", timeout=15000)
        page.wait_for_selector("a.btn.btn-primary.hide_for_print", timeout=15000)

        with page.expect_download() as download_info:
            page.locator("a.btn.btn-primary.hide_for_print", has_text="Show Detailed View (CSV)").click()
        download = download_info.value

        original_filename = download.suggested_filename
        match = re.search(r"([A-Za-z]+) (\d{4}) (\d{2})", original_filename)
        if match:
            month_str, year_str, day_str = match.groups()
            try:
                original_date = datetime.strptime(f"{day_str} {month_str} {year_str}", "%d %B %Y")
                new_date = original_date - timedelta(days=1)
                new_date_str = new_date.strftime("%B %Y %d")
                old_date_str = f"{month_str} {year_str} {day_str}"
                new_filename = original_filename.replace(old_date_str, new_date_str)
            except:
                new_filename = original_filename
        else:
            new_filename = original_filename

        download_path = os.path.join(os.getcwd(), new_filename)
        download.save_as(download_path)
        print(f"✅ File downloaded as {new_filename}")

        browser.close()

if __name__ == "__main__":
    run()

