import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re
import numpy as np


def scrape():

    driver = webdriver.Chrome()

    base_url = 'https://www.neptun.mk/mobilni_telefoni.nspx?page={}&priceRange=1599_119999'
    page_number = 1
    product_data = []

    samsung_model_pattern = re.compile(
        r'Galaxy\s+[A-Za-z0-9]+(?:\s+\d+)?(?:\s*(Ultra|Fold\d*|Flip|5G|FE|Z|\+|Plus))?(?!\s*(\d+)(?!\w))',
        re.IGNORECASE
    )

    memory_color_pattern = re.compile(
        r'\d+GB|1TB|Starlight|Midnight|Black|White|Purple|Red|Blue|Green|Pink|Yellow|Titanium|Ultramarine', re.IGNORECASE)

    xiaomi_model_pattern = re.compile(
        r'(Redmi\s(?:Note\s\d{1,2}(?:\sPro\+|\sPro|S|Ultra|Plus)?|(?:A|C|T|X|M|N|Z)?\d{1,2}[A-Za-z]?(?:\sPro\+|\sPro|\sUltra|\sPlus)?)'
        r'|(?:Poco\s[A-Za-z]+\s?\d+(?:\sPro|\sPro\+|[A-Z])?)'
        r'|(?:Xiaomi\s\d{1,2}[A-Z]?\s?(?:Pro\+|Pro|Ultra|Lite)?)'
        r')',
        re.IGNORECASE
    )
    honor_model_pattern = re.compile(
        r'(HONOR\s(?:X\d+b|200\s(?:Smart|Lite)|Magic6\s(?:Lite|Pro)))',
        re.IGNORECASE
    )


    def clean_xiaomi_model(name, match):
        if "Redmi" in match.group(0):
            return match.group(0).strip()
        return match.group(0).strip()


    nokia_model_pattern = re.compile(r'Nokia\s(\d+[A-Za-z]*)', re.IGNORECASE)


    def clean_model_name(name):
        name = re.sub(memory_color_pattern, '', name)
        name = re.sub(r'(\s+\d+[\+\d]*)$', '', name)
        colors_to_remove = ['Teal', 'Desert', 'Natural']
        for color in colors_to_remove:
            name = re.sub(rf'\s*{color}', '', name, flags=re.IGNORECASE)
        return name.strip()

    def standardize_model_name(model_name):
        if isinstance(model_name, str):
            model_name = re.sub(r'\bS(\d{2})FE\b', r'S\1 FE', model_name, flags=re.IGNORECASE)

            # Add "Z Fold" only if "Fold" is not already preceded by "Z"
            model_name = re.sub(r'(?<!Z )Fold(\d+)', r'Z Fold \1', model_name)
            model_name = re.sub(r'Z Fold(\d+)', r'Z Fold \1', model_name)

            model_name = re.sub(r'(?<!Z )Flip(\d+)', r'Z Flip \1', model_name)
        else:
            # Handle cases where model_name is not a string (e.g., float, None)
            model_name = str(model_name)  # Convert to string if not already
        return model_name


    while True:
        url = base_url.format(page_number)
        driver.get(url)
        time.sleep(1)

        phones = driver.find_elements(By.CSS_SELECTOR, 'div.white-box')

        if not phones:
            print("No more pages.")
            break

        for phone in phones:
            try:
                name = phone.find_element(By.CLASS_NAME, 'product-list-item__content--title').text

                price_elements = phone.find_elements(By.CSS_SELECTOR, '.HappyCard .product-price__amount--value')
                if price_elements:
                    price = price_elements[0].text

                else:
                    price_elements = phone.find_elements(By.CSS_SELECTOR, '.newPriceModel .product-price__amount--value')
                    price = price_elements[0].text

                parts = name.split()
                brand = parts[0] if len(parts) > 0 else np.nan
                element = phone.find_element(By.CSS_SELECTOR, "a[ng-href^='/categories/mobilni_telefoni/']")
                phone_url = element.get_attribute("href")
                manufacturer = 'Neptun'
                if brand.lower() == 'samsung':
                    match = samsung_model_pattern.search(name)
                    if match:
                        model = match.group(0).strip()
                        model = clean_model_name(model)
                    else:
                        model = np.nan
                elif brand.lower() == 'apple':
                    model = clean_model_name(name)
                    if model.lower().startswith("apple"):
                        model = model[5:].strip()
                elif brand.lower() == 'xiaomi':
                    match = xiaomi_model_pattern.search(name)
                    if match:
                        model = clean_xiaomi_model(name, match)
                elif brand.lower() == 'nokia':
                    match = nokia_model_pattern.search(name)
                    if match:
                        model = match.group(0).strip()
                elif brand.lower() == 'honor':
                    match = honor_model_pattern.search(name)
                    if match:
                        model = match.group(1).strip()
                    else:
                        model = ' '.join(parts[:2]).strip() if len(parts) >= 2 else parts[0].strip()
                else:
                    model = np.nan
                price = price.replace('.', '')
                model = standardize_model_name(model)
                product_data.append([brand, model, name, price, manufacturer, phone_url])

            except NoSuchElementException:
                continue

        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, 'ul > li.pagination-next')

            if 'disabled' in next_page_button.get_attribute('class'):
                print("No more pages.")
                break
            else:
                page_number += 1
                continue
        except NoSuchElementException:
            print("Next button not found, exiting loop.")
            break

    df = pd.DataFrame(product_data, columns=["brand", "model", "whole_name", "price", "vendor", "link"])
    df = df[df["brand"].str.lower().isin(["honor", "apple", "xiaomi", "nokia", "samsung"])]

    driver.quit()
    return df