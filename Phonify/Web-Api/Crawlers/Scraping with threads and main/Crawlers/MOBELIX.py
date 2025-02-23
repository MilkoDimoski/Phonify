import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def scrape():

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode (no GUI)
    service = Service(r'C:\Users\angel\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(options=chrome_options)

    base_url = "https://mobelix.com.mk/mk/mobilni-telefoni?page={}"
    phones_data = []

    exclude_keywords = ["Buds", "AirTag", "Air Pods", "Watch", "HomePod", "Earbuds", "GOPRO", "iPad", "Tab", "MacBook",
                        "Pad"]
    exclude_keywords1 = ["5g", "ram", "gb", "storage", "Нови - Без кутија", "E-Sim", "huawei", "xiaomi", "blackberry",
                         "one plus", "asus", "google"]

    def scrape_page(page_number):
        url = base_url.format(page_number)
        driver.get(url)
        time.sleep(2)

        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_increment = 700
        current_position = 0

        while current_position < last_height:
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(1)
            current_position += scroll_increment
            new_height = driver.execute_script("return document.body.scrollHeight")

            if current_position >= new_height:
                break

        phones = driver.find_elements(By.CLASS_NAME, 'product-wrapper')
        for phone in phones:
            try:
                name = phone.find_element(By.CLASS_NAME, 'mb-0').text
                model = phone.find_element(By.CLASS_NAME, 'h5.font-weight-normal').text
                cena = phone.find_element(By.CLASS_NAME, 'h5.price').text
                element = phone.find_element(By.CSS_SELECTOR, "a.d-flex.w-100")
                phone_url = element.get_attribute("href")
                manufacturer = 'Mobelix'

                # Skip unwanted models
                if "fe" == model.strip().lower():
                    continue
                if any(keyword.lower() in model.lower() for keyword in exclude_keywords):
                    continue

                # Clean model name
                cleaned_model = ' '.join([part.strip() for part in model.split() if not any(
                    keyword.lower() in part.strip().lower() for keyword in exclude_keywords1)])
                cleaned_model = ' '.join([
                    word for word in cleaned_model.split()
                    if not (word.lower().endswith("gb") or word.lower().endswith("tb"))
                ])
                cleaned_model = cleaned_model.replace("Нови - Без кутија", "").strip()
                if "samsung" in name.lower() and "galaxy" not in cleaned_model.lower():
                    cleaned_model = "Galaxy " + cleaned_model

                cleaned_model = cleaned_model.replace("Samsung", "").strip()
                cleaned_model = cleaned_model.replace("One Plus", "").strip()

                # Parse price
                if len(cena.split(".")) > 2:
                    price = int(cena.split(".")[1][2:].replace("\n", "").replace(",", ""))
                else:
                    price = int(cena.split(".")[0].replace("\n", "").replace(",", ""))

                # Collect data
                phones_data.append({
                    "brand": name,
                    "model": cleaned_model,
                    "whole_name": model,
                    "price": price,
                    "vendor": manufacturer,
                    "link": phone_url
                })
            except Exception as e:
                print(f"Error scraping phone on page {page_number}: {e}")

        print(f"Page {page_number} scraped successfully!")


    page_number = 1  # Start with page 1
    while True:
        scrape_page(page_number)

        # Check for next page
        pagination = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination li.page-item')
        next_page_button = pagination[-1]  # Last page item in the list
        if 'disabled' in next_page_button.get_attribute('class'):
            print("No more pages.")
            break

        # Go to the next page
        page_number += 1

    # Convert data to DataFrame
    df = pd.DataFrame(phones_data)
    driver.quit()
    return df