# %%
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
import numpy as np


def scrape():

    driver = webdriver.Chrome()

    url = 'https://www.telekom.mk/mobilni-uredi.nspx?priceType=1&deviceType=3&familijarenBudzet=2&collect=true&pagingType=3'
    phones_data = []

    driver.get(url)

    # Regular expressions for phone model matching
    t_phone_model_pattern = re.compile(r'T\s*Phone\s*(\d+)?\s*(Pro)?\s*(5G)?\s*(\d{4})?(?:\s*\+.*)?', re.IGNORECASE)
    samsung_model_pattern = re.compile(r'Galaxy\s+[A-Za-z0-9]+(?:\s+\d+)?(?:\s*(Ultra|Fold\d*|Flip|5G|FE|Z|\+|Plus))?',
                                       re.IGNORECASE)
    oneplus_model_pattern = re.compile(r'OnePlus\s+((\d+\s*(Pro)?)|(Nord\s+\w+))\s*(\d+GB)?', re.IGNORECASE)
    apple_pattern = re.compile(
        r'\d+GB|Apple|1TB|Starlight|Midnight|Black|White|Purple|Red|Blue|Green|Silver|\(2022\)|Pink|Yellow|Titanium|Ultramarine',
        re.IGNORECASE)
    exclusion_pattern = re.compile(r'usb|router', re.IGNORECASE)
    motorola_model_pattern = re.compile(r'Motorola\s+(Edge\s\d+\s\w+|Moto\s\w+|\w+\s\d+)', re.IGNORECASE)
    memory_color_pattern = re.compile(r'\b(\d{2,4}(GB|TB)|Teal|Desert|Natural|Black|White|Silver|Gray)\b', re.IGNORECASE)
    honor_model_pattern = re.compile(r'(Honor\s*\d+|Honor\s*Magic\d+|HONOR\s*\d+)\s*(\w+)?\s*(5G)?\s*(\d+GB)?(?:\+.*)?',
                                     re.IGNORECASE)

    hardcoded_motorola_models = {
        'Motorola Razr 40 Ultra 256GB': 'Razr 40 Ultra',
        'Moto Edge 50 Neo 5G 256GB': 'Moto Edge 50',
        'Moto G54 Power 5G 256GB': 'Moto G54 Power',
        'Moto G85 5G 256GB': 'Moto G85',
        'Moto Edge 40 Neo 5G': 'Moto Edge 40',
        'Motorola Moto G53': 'Moto G53',
        'Moto G14 128GB': 'Moto G14',
        'MOTO E13 64GB': 'Moto E13'
    }
    xiaomi_model_pattern = re.compile(
        r'(Redmi\s(?:Note\s\d{1,2}(?:\sPro\+|\sPro|S|Ultra|Plus)?|(?:A|C|T|X|M|N|Z)?\d{1,2}[A-Za-z]?(?:\sPro\+|\sPro|\sUltra|\sPlus)?))'
        r'|(?:Poco\s[A-Za-z]+\s?\d+(?:\sPro|\sPro\+|[A-Z])?)'
        r'|(?:Xiaomi\s\d{1,2}[A-Z]?\s?(?:Pro\+|Pro|Ultra|Lite)?)',
        re.IGNORECASE
    )

    remove_gb_and_colors = re.compile(
        r'\s*(\d+\s?GB|Gray|Black|White|Purple|Red|Blue|Green|Silver|Pink|Yellow|Ceramic|Titanium|Ultra|Starlight)\s*',
        re.IGNORECASE)


    def extract_motorola_model(name):
        name_cleaned = name.strip()
        if name_cleaned in hardcoded_motorola_models:
            return hardcoded_motorola_models[name_cleaned]

        match = motorola_model_pattern.search(name)
        model = name
        if match:
            model = f"{match.group(1).strip()}"
        if "Power Edition" in name:
            model = f"{match.group(1).strip()} Power Edition"
        return model


    def clean_model_name(name):
        # Remove memory or color info
        name = re.sub(memory_color_pattern, '', name)
        # Remove trailing numbers like "256+" or "512"
        name = re.sub(r'\s+\d+[\+\d]*$', '', name)
        return name.strip()

    def standardize_model_name(model_name):
        # Ensure the model_name is a string before applying replace
        if isinstance(model_name, str):
            # Convert 'Z Fold' models to have a space between 'Z Fold' and the number
            model_name = re.sub(r'Z Fold(\d+)', r'Z Fold \1', model_name)
            model_name = re.sub(r'Z Flip(\d+)', r'Z Flip \1', model_name)
        else:
            # Handle cases where model_name is not a string (e.g., float, None)
            model_name = str(model_name)  # Convert to string if not already
        return model_name


    try:
        button_Cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'all-cookies-btn'))
        )
        button_Cookies.click()
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Error occurred: {e}")

    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    while True:
        try:
            arrow_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#phoneBoxList > div.show-more-devices.ng-scope > span.ion-ios-arrow-down"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", arrow_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", arrow_button)
            time.sleep(1)
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            print("No more 'Show More' buttons available.")
            break

    phones = driver.find_elements(By.CLASS_NAME, 'phoneList-box')
    print(f"Number of phones found: {len(phones)}")

    for phone in phones:
        try:
            name = phone.find_element(By.CSS_SELECTOR, 'div.phone-header h2.ng-binding').text
            price = phone.find_element(By.CSS_SELECTOR, 'div.phoneDetailsHolder div.priceBox div.ng-binding.ng-scope').text

            price = re.sub(r'\.', '', price)

            parts = name.split()
            brand = parts[0]
            model = name
            element = phone.find_element(By.CSS_SELECTOR, "a.btn-magen.order-btn")
            phone_url = element.get_attribute("href")
            manufacturer = 'Telekom'
            if exclusion_pattern.search(name):
                continue

            if 't phone' in name.lower():
                brand = 'T Phone'
                if 't phone 5g' in name.lower():
                    model = 'T phone'
                else:
                    match = t_phone_model_pattern.search(name)
                    model = re.sub(r'\s*5G\s*', '', model, flags=re.IGNORECASE).strip()
                    if match:
                        model_parts = ['T Phone']
                        if match.group(1):
                            model_parts.append(match.group(1))
                        if match.group(2):
                            model_parts.append(match.group(2))
                        model = ' '.join(model_parts).strip()
            elif 'moto' in name.lower():
                brand = 'Motorola'
                model = extract_motorola_model(name)
            elif 'iphone' in name.lower():
                brand = 'Apple'
                model = apple_pattern.sub('', name).strip()
                model = model.replace("ProMax", "Pro Max")
            elif brand.lower() == 'oneplus':
                match = oneplus_model_pattern.search(name)
                if match:
                    model = match.group(1).strip()
                else:
                    model = np.nan
            elif brand.lower() == 'samsung':
                match = samsung_model_pattern.search(name)
                if match:
                    model = match.group(0).strip()
                    model = clean_model_name(model)
                else:
                    model = np.nan
                if 'z flip' in name.lower():
                    model = 'Galaxy Z Flip'
                    match = re.search(r'flip(\d+)', name, re.IGNORECASE)
                    if match:
                        model += str(match.group(1))
                elif 'z fold' in name.lower():
                    model = 'Galaxy Z Fold'
                    match = re.search(r'fold(\d+)', name, re.IGNORECASE)
                    if match:
                        model += str(match.group(1))
            elif brand.lower() == 'alcatel':
                model = parts[1]
            elif brand.lower() == 'honor':
                match = honor_model_pattern.search(name)
                brand = 'Honor'
                if match:
                    model = match.group(1).strip()
                    if match.group(2):
                        model += " " + match.group(2)
                    if '5G' in name:
                        model = re.sub(r'\s*5G', '', model).strip()
                    if '+' in name:
                        model = model.split('+')[0].strip()
                    model = model.replace("Honor", "").strip()
                    model = model.replace("HONOR", "").strip()
            elif brand.lower() == 'tcl':
                model = parts[1]
            elif brand.lower() == 'xiaomi' or 'redmi' in name.lower():
                brand = 'Xiaomi'
                match = xiaomi_model_pattern.search(name)
                if match:
                    model = match.group(0).strip()

                    if model.lower().startswith("xiaomi") and not model.lower().startswith("redmi"):
                        model = model.replace("Xiaomi", "").strip()

                    model = remove_gb_and_colors.sub('', model).strip()

                    model = re.sub(r'\s+', ' ', model).strip()
                else:
                    model = np.nan
                    model = match.group(0).strip()
                if 'mi' in model.lower():
                    model = model.replace('mi', 'Redmi')
                model = model.replace('MI', 'Redmi')
                if '9at' in name.lower():
                    model = model.replace('9A', '9AT')
            model = standardize_model_name(model)
            phones_data.append([brand, model, name, price, manufacturer, phone_url])
        except NoSuchElementException:
            print("Name not found for a phone.")

    df = pd.DataFrame(phones_data, columns=["brand", "model", "whole_name", "price", "vendor", "link"])
    df = df[df["brand"].str.lower().isin(
        ["xiaomi", "apple", "samsung", "oneplus", "tcl", "alcatel", "honor", "motorola", "t phone"])]

    driver.quit()

    return df
