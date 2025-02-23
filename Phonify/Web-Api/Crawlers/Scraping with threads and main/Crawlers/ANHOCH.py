import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import pandas as pd
import re
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape():
    # Define patterns
    apple_pattern = re.compile(
        r'\d+GB|1TB|Starlight|Midnight|Black|White|Purple|Red|Blue|Green|Pink|Yellow|Titanium|Ultramarine',
        re.IGNORECASE)
    number_pattern = re.compile(r'(\d+)')
    flip_fold_pattern = re.compile(r'Galaxy\s+Z\s+(Fold|Flip)\s*(\d+)?', re.IGNORECASE)
    general_samsung_pattern = re.compile(r'Galaxy\s+[A-Za-z0-9]+(?:\s+\d+)?(?:\s*(Ultra|FE|Z|\+|Plus))?', re.IGNORECASE)
    xiaomi_model_pattern = re.compile(
        r'(Redmi\s(?:Note\s\d{1,2}(?:\sPro\+|\sPro|S|Ultra|Plus)?|(?:A|C|T|X|M|N|Z)?\d{1,2}[A-Za-z]?(?:\sPro\+|\sPro|\sUltra|\sPlus)?))'
        r'|(?:Poco\s[A-Za-z]+\s?\d+(?:\sPro|\sPro\+|[A-Z])?)'
        r'|(?:Xiaomi\s\d{1,2}[A-Z]?\s?(?:Pro\+|Pro|Ultra|Lite)?)',
        re.IGNORECASE
    )
    motorola_model_pattern = re.compile(r'Motorola\s+(Edge\s\d+\s\w+|Moto\s\w+|\w+\s\d+)', re.IGNORECASE)
    cat_model_pattern = re.compile(r'(?<=Cat\s)(S\d{2,3}(?:\sH\+|\sPro)?)', re.IGNORECASE)
    google_pixel_pattern = re.compile(r'Pixel\s+\d+\s+(Pro\s*XL|XL\s*Pro|Pro|XL)?', re.IGNORECASE)
    nokia_model_pattern = re.compile(
        r'Nokia\s(\d{2,4}[A-Za-z]*)', re.IGNORECASE
    )

    # Define extraction functions
    def extract_nokia_model(name):
        match = nokia_model_pattern.search(name)
        return match.group(0).strip() if match else name

    def extract_google_pixel_model(name):
        match = google_pixel_pattern.search(name)
        return match.group(0).strip() if match else name

    def extract_samsung_model(name):
        match = flip_fold_pattern.search(name) or general_samsung_pattern.search(name)
        return match.group(0).strip() if match else name

    def extract_xiaomi_model(name):
        match = xiaomi_model_pattern.search(name)
        return match.group(0).strip() if match else name

    def extract_motorola_model(name):
        match = motorola_model_pattern.search(name)
        model = name
        if match:
            model = f"{match.group(1).strip()}"
        if "Power Edition" in name:
            model = f"{match.group(1).strip()} Power Edition"
        return model

    def extract_cat_model(name):
        match = cat_model_pattern.search(name)
        return match.group(0).strip() if match else name

    def format_samsung_model(name):
        # Ensure the model_name is a string before applying the replace
        if isinstance(name, str):
            # For Plus models (e.g., S23 Plus -> S23+)
            name = re.sub(r'(\d{2})\s*Plus', r'\1+', name)
        return name

    # Set up WebDriver
    driver = webdriver.Chrome()

    base_url = 'https://www.anhoch.com/categories/mobilni-telefoni/products?brand=&attribute=&toPrice=274980&inStockOnly=1&sort=latest&perPage=50&page={}'
    page_number = 1
    product_data = []
    popup_closed = False

    while True:
        url = base_url.format(page_number)
        driver.get(url)

        time.sleep(3)
        if not popup_closed:
            try:
                popup_closed = True
                # Wait for the 'Show More' button to be clickable
                arrow_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "#phoneBoxList > div.show-more-devices.ng-scope > span.ion-ios-arrow-down"))
                )

                # Scroll the 'Show More' button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", arrow_button)
                time.sleep(1)

                # Click the 'Show More' button
                driver.execute_script("arguments[0].click();", arrow_button)
                time.sleep(1)

            except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
                print("No more 'Show More' buttons available.")
                popup_closed = True
                # Mark popup as closed after handling 'Show More' button issue
                try:
                    # Find and click the close button for the popup
                    close_button = driver.find_element(By.CSS_SELECTOR,
                                                       '.modal-content .modal-body .popup-banner-inner .close')
                    close_button.click()
                    print("Popup closed.")
                except NoSuchElementException:
                    print("Close button for the popup not found.")
                    popup_closed = True  # Mark popup as closed, continue further

        phones = driver.find_elements(By.CSS_SELECTOR, 'div.col')
        prices = driver.find_elements(By.CLASS_NAME, "product-price")

        if not phones:
            print("No more pages.")
            break

        for phone in phones:

            try:
                price_element = None
                name = phone.find_element(By.CLASS_NAME, 'product-name').text
                price_list = phone.find_elements(By.CLASS_NAME, 'product-price')[1]

                price_element = re.sub(r'[^\d.,]', '', price_list.text)
                cleaned_price = price_element.replace('.', '')
                price = cleaned_price.split(',')[0]

                parts = name.split(" ")
                brand = parts[0]
                model = name
                manufacturer = 'Anhoch'
                product_card = phone.find_element(By.CSS_SELECTOR, '.product-card-middle')
                phone_url = product_card.find_element(By.CSS_SELECTOR, 'a.product-name').get_attribute('href')

                if 'blackview' in name.lower():
                    brand = 'Blackview'
                    model = parts[2]
                elif 'denver' in name.lower():
                    brand = 'Denver'
                    model = parts[3]
                elif 'philips' in name.lower():
                    brand = 'Philips'
                    model = parts[3]
                elif brand.lower() == "apple":
                    model_part = name.replace("Apple", "").strip()
                    model = re.split(apple_pattern, model_part, maxsplit=1)[0].strip()
                    numbers = re.findall(number_pattern, model)
                    if len(numbers) > 1:
                        first_number = numbers[0]
                        model = re.split(rf'{first_number}.*', model, maxsplit=1)[0].strip() + f" {first_number}"
                elif brand.lower() == "samsung":
                    model = extract_samsung_model(name)
                    model = format_samsung_model(model)  # Apply formatting for Plus models
                    # Remove standalone ' 5 ' (with spaces before and after) from the model
                    # model = re.sub(r'(?<=\s)5', '', model)
                elif brand.lower() == "xiaomi":
                    model = extract_xiaomi_model(name)
                elif brand.lower() == "motorola":
                    model = extract_motorola_model(name)
                elif brand.lower() == "cat":
                    model = extract_cat_model(name)
                elif brand.lower() == 'google':  # Add condition for Google Pixel
                    model = extract_google_pixel_model(name)
                elif brand.lower() == "nokia":
                    model = extract_nokia_model(name)
                else:
                    model = np.nan

                product_data.append([brand, model, name, price, manufacturer, phone_url])
            except NoSuchElementException:
                continue

        try:
            next_button = driver.find_element(By.CSS_SELECTOR,
                                              'ul.pagination li.page-item:last-child > button.page-link')
            if 'disabled' in next_button.get_attribute('class'):
                print("Reached the last page.")
                break
            else:
                page_number += 1
        except NoSuchElementException:
            print("Pagination not found, stopping.")
            break

    # Save to CSV
    df = pd.DataFrame(product_data, columns=["brand", "model", "whole_name", "price", "vendor", "link"])
    df = df[df["brand"].str.lower().isin(
        ["philips", "denver", "motorola", "blackview", "samsung", "apple", "xiaomi", "nokia", "cat", "google"])]

    driver.quit()
    return df
