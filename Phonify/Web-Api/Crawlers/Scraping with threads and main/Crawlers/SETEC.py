from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import numpy as np


def scrape():

    base_url = 'https://setec.mk/%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B8-%D1%84%D0%BE%D1%82%D0%BE-%D0%B8-%D0%BD%D0%B0%D0%B2%D0%B8%D0%B3%D0%B0%D1%86%D0%B8%D1%98%D0%B0/%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%BD%D0%B8-%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD%D0%B8'
    page_number = 1

    product_data = []

    # Regex patterns
    xiaomi_model_pattern = re.compile(
        r'(Redmi\s(?:Note\s\d{1,2}(?:\sPro\+|\sPro|S|Ultra|Plus)?|(?:A|C|T|X|M|N|Z)?\d{1,2}[A-Za-z]?(?:\sPro\+|\sPro|\sUltra|\sPlus)?))'
        r'|(?:Poco\s[A-Za-z]+\s?\d+(?:\sPro|\sPro\+|[A-Z])?)'
        r'|(?:Xiaomi\s\d{1,2}[A-Z]?\s?(?:Pro\+|Pro|Ultra|Lite)?)',
        re.IGNORECASE
    )

    samsung_model_pattern = re.compile(
        r'Galaxy\s+[A-Za-z0-9]+(?:\s+\d+)?(?:\s*(Ultra|Fold\d*|Flip|5G|FE|Z|\+|Plus))?',
        re.IGNORECASE
    )

    blackview_model_pattern = re.compile(
        r'Blackview\sA(?:60|52|55|80|70|[5-9]\d)?(?:\s(?:Pro|Plus|PRO)?)',
        re.IGNORECASE
    )

    motorola_model_pattern = re.compile(
        r'Motorola\sMoto\s([A-Za-z0-9]+)', re.IGNORECASE
    )

    memory_color_pattern = re.compile(
        r'\d+GB|1TB|Starlight|Midnight|Black|White|Purple|Red|Blue|Green|Pink|Yellow|Titanium|Ultramarine', re.IGNORECASE)

    tcl_model_pattern = re.compile(
        r'onetouch\s+\d{4,6}', re.IGNORECASE
    )
    uniwa_model_pattern = re.compile(
        r'UNIWA\s([A-Za-z0-9]+(?:\sFlip)?)', re.IGNORECASE
    )


    allcall_model_pattern = re.compile(
        r'AllCall\s+([A-Za-z]+)', re.IGNORECASE
    )
    doogee_model_pattern = re.compile(
        r'DOOGEE\s(N\d{2}(?:\sPro)?)', re.IGNORECASE
    )
    huawei_model_pattern = re.compile(
        r'Huawei\s([A-Za-z]+\s?[A-Za-z]*\s?\d+[A-Za-z]*)', re.IGNORECASE
    )
    nokia_model_pattern = re.compile(
        r'Nokia\s(\d+[A-Za-z]*)', re.IGNORECASE
    )
    realme_model_pattern = re.compile(
        r'Realme\s([A-Za-z]?\d+[A-Za-z]*)', re.IGNORECASE
    )
    vivo_model_pattern = re.compile(
        r'Vivo\s([A-Za-z]+\d+[A-Za-z]*)', re.IGNORECASE
    )


    def clean_samsung_model_name(product_name):
        if "Fold" in product_name or "Flip" in product_name:
            match = samsung_model_pattern.search(product_name)
            return match.group(0) if match else np.nan
        else:
            match = samsung_model_pattern.search(product_name)
            if match:
                model_name = match.group(0)
                cleaned_name = ' '.join(
                    [part for part in model_name.split() if not part.isdigit() or part in ["Fold", "Flip", "Plus", "+"]])
                return cleaned_name
            else:
                return np.nan

    def standardize_model_name(model_name):
        # Ensure the model_name is a string before applying replace
        if isinstance(model_name, str):
            # Standardize Galaxy Fold models
            model_name = re.sub(r'Galaxy Fold (\d+)', r'Galaxy Z Fold \1', model_name)
            # Standardize Z Fold models to have a space between 'Z Fold' and the number
            model_name = re.sub(r'Z Fold(\d+)', r'Z Fold \1', model_name)
            # Add space between number and 'FE' in models like S24FE to S24 FE
            model_name = re.sub(r'(\d+)(FE)', r'\1 \2', model_name)
            # Convert Flip 4, Flip 5, Flip 6 to Z Flip 4, Z Flip 5, Z Flip 6
            model_name = re.sub(r'Flip (\d)', r'Z Flip \1', model_name)
        else:
            # Handle cases where model_name is not a string (e.g., float, None)
            model_name = str(model_name)  # Convert to string if not already
        return model_name

    while True:
        url = base_url + '?page=' + str(page_number)
        response = requests.get(url)

        if response.status_code != 200:
            print("Error fetching the page, status code:", response.status_code)
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.select(".product")

        if not products:
            print("No more products found.")
            break

        for product in products:
            product_name = product.select_one(".name a").text.strip()

            regular_price_element = product.select_one(".price-new-new")
            link = product.select_one("div.name a")  # Select the <a> inside the <div class="name">
            phone_link = link['href'] if link else None
            manufacturer = 'Setec'

            if regular_price_element:
                raw_price = regular_price_element.text.strip()
            elif product.select_one(".cena_za_kesh"):
                raw_price = product.select_one(".cena_za_kesh").text.strip()
            else:
                raw_price = None

            if raw_price:
                # Remove non-numeric characters, except for decimal points
                cleaned_price = re.sub(r'[^\d.,]', '', raw_price).replace(',', '.')
                cleaned_price = cleaned_price.replace('.', '')
                # Extract the numeric part
                regular_price = re.search(r'\d+(\.\d+)?', cleaned_price)
                regular_price = float(regular_price.group(0)) if regular_price else np.nan
            else:
                regular_price = np.nan

            parts = product_name.split()
            brand = parts[0] if len(parts) > 0 else np.nan
            if brand.lower() == "samsung":
                model = clean_samsung_model_name(product_name)
                # model=product_name
            elif brand.lower() == "apple":
                model_part = product_name.replace(brand, "").strip()
                model = re.split(memory_color_pattern, model_part, maxsplit=1)[0].strip()
                model = re.sub(r'-$', '', model).strip()
            elif "Xiaomi" in product_name:
                brand = "Xiaomi"
                match = xiaomi_model_pattern.search(product_name)
                if match:
                    model = match.group(0).strip()
                    # Remove the "Xiaomi" prefix if present
                    if model.lower().startswith("xiaomi"):
                        model = model.replace("Xiaomi", "").strip()
                else:
                    model = np.nan
            elif "Blackview" in product_name:
                brand = "Blackview"
                match = blackview_model_pattern.search(product_name)
                model = match.group(0).replace("Blackview", "").strip() if match else np.nan
            elif "Motorola" in product_name:
                brand = "Motorola"
                match = motorola_model_pattern.search(product_name)
                if match:
                    model = f"Moto {match.group(1).strip()}"
                else:
                    model = np.nan
            elif "TCL" in product_name:
                brand = "TCL"
                match = tcl_model_pattern.search(product_name)
                model = match.group(0).replace("tcl", "").strip() if match else np.nan
            elif brand.lower() == "uniwa":
                match = uniwa_model_pattern.search(product_name)
                if match:
                    model = match.group(1).strip()
                else:
                    model = np.nan
            elif brand.lower() == "allcall":
                match = allcall_model_pattern.search(product_name)
                model = match.group(1).strip() if match else np.nan
            elif brand.lower() == "doogee":
                match = doogee_model_pattern.search(product_name)
                model = match.group(1).strip() if match else np.nan
            elif brand.lower() == "huawei":
                match = huawei_model_pattern.search(product_name)
                model = match.group(1).strip() if match else np.nan
            elif brand.lower() == "nokia":
                match = nokia_model_pattern.search(product_name)
                model = match.group(1).strip() if match else np.nan
            elif brand.lower() == "realme":
                match = realme_model_pattern.search(product_name)
                model = match.group(1).strip() if match else np.nan
            elif brand.lower() == "vivo":
                match = vivo_model_pattern.search(product_name)
                model = match.group(1).strip() if match else np.nan
            else:
                model = np.nan
            model = standardize_model_name(model)

            product_data.append([brand, model, product_name, regular_price, manufacturer, phone_link])

        page_number += 1

    df = pd.DataFrame(product_data, columns=["brand", "model", "whole_name", "price", "vendor", "link"])

    #df.to_csv('products_with_details.csv', index=False)

    df = df[df["brand"].str.lower().isin(
        ["samsung", "apple", "xiaomi", "blackview", "motorola", "tcl", "uniwa", "allcall", "doogee", "huawei", "nokia",
         "realme", "vivo"])]

    return df
