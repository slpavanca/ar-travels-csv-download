from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import os
import time
import re

def run():
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove this if you want browser visible
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "download.prompt_for_download": False,
        "download.default_directory": os.getcwd(),  # Save to current dir
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://arll.artravells.in/")

        wait.until(EC.presence_of_element_located((By.NAME, "login"))).send_keys("mahesh")
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys("123456")
        driver.find_element(By.ID, "login_button").click()

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.header-menu-bar"))).click()
        driver.find_element(By.CSS_SELECTOR, "a#reports_id").click()
        driver.find_element(By.CSS_SELECTOR, 'a[id="3"]').click()

        # Select "Report Type"
        report_dropdown = wait.until(EC.presence_of_element_located((By.ID, "report_id")))
        Select(report_dropdown).select_by_value("147")

        # Select "All Services"
        Select(driver.find_element(By.ID, "report_service_all")).select_by_value("-1")

        # Wait for coach list to load
        wait.until(lambda d: len(Select(d.find_element(By.ID, "report_coach_id")).options) > 1)
        Select(driver.find_element(By.ID, "report_coach_id")).select_by_visible_text("- All -")

        # Select Hub
        wait.until(lambda d: len(Select(d.find_element(By.ID, "hub_options")).options) > 1)
        Select(driver.find_element(By.ID, "hub_options")).select_by_value("1")

        # Select "Yesterday" from date range
        wait.until(lambda d: len(Select(d.find_element(By.ID, "report_date_range")).options) > 1)
        Select(driver.find_element(By.ID, "report_date_range")).select_by_visible_text("Yesterday")

        # Submit form
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Run Report"]').click()

        # Wait for CSV link
        download_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary.hide_for_print")))
        download_href = download_link.get_attribute("href")

        # Download the file manually
        import requests
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"])

        response = session.get(download_href)
        original_filename = re.findall(r'filename="([^"]+)"', response.headers.get("content-disposition", ""))
        filename = original_filename[0] if original_filename else "report.csv"

        # Rename file based on date inside filename
        match = re.search(r"([A-Za-z]+) (\d{4}) (\d{2})", filename)
        if match:
            month_str, year_str, day_str = match.groups()
            try:
                original_date = datetime.strptime(f"{day_str} {month_str} {year_str}", "%d %B %Y")
                new_date = original_date - timedelta(days=1)
                new_date_str = new_date.strftime("%B %Y %d")
                old_date_str = f"{month_str} {year_str} {day_str}"
                new_filename = filename.replace(old_date_str, new_date_str)
            except:
                new_filename = filename
        else:
            new_filename = filename

        with open(new_filename, "wb") as f:
            f.write(response.content)
        print(f"✅ File downloaded as {new_filename}")

    finally:
        driver.quit()

if __name__ == "__main__":
    run()


