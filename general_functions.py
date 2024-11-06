from openpyxl import load_workbook
import os
import random as rnd
import time
import requests
from selenium.common.exceptions import WebDriverException


def empty_excel(path):
    wb = load_workbook(path)
    ws = wb['Sheet1']  # Change 'Sheet1' to your specific sheet name

    # Loop through all rows and columns to clear content
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.value = None

    # Save the workbook
    wb.save(path)


    
def remove_illegal_characters(value):
    """Removes illegal characters that Excel does not support."""
    ILLEGAL_CHARACTERS = [chr(i) for i in range(32) if i not in (9, 10, 13)] + [chr(127)]
    for char in ILLEGAL_CHARACTERS:
        value = value.replace(char, "")
    return value


def ensure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)  # Create directories if they don't exist


def get_last_non_empty_row_excel(file_path):
    wb = load_workbook(file_path)
    ws = wb['Sheet1']  # Change 'Sheet1' to your sheet name
    for row in range(ws.max_row, 0, -1):
        if any(cell.value is not None for cell in ws[row]):
            return row
    return 0  # If all rows are empty

def random_sleep(range_from, range_to):
    seconds = rnd.uniform(range_from, range_to)
    time.sleep(seconds)



def download_image(image_url, path):
    response = requests.get(image_url)
    with open(path, 'wb') as file:
        file.write(response.content)

   
def split_data(entry):
    # Split the entry by comma to separate title from other details
    title, details = entry.split(',', 1)

    # Extract individual components from details
#3
    price = details.split('prezzo:')[1].split('€')[0].strip() + '€'  # Extract price #you can have other value so you probalby have to change zl to value that is in your country
    brand = details.split('brand:')[1].split(',')[0].strip()  # Extract brand
    size = details.split('taglia:')[1].strip()  # Extract size
    return title.strip(), price, brand, size


MAX_RETRIES = 3 # Maximum number of retries

def load_page(driver, webpage, page):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            driver.get(f"{webpage}&page={page+1}")
            break  # Break the loop if the page loads successfully
        except WebDriverException as e:
            print(f"Error loading page: {e}")
            retries += 1
            time.sleep(2)  # Wait for 2 seconds before retrying
            if retries == MAX_RETRIES:
                print("Max retries reached, unable to load page.")
                raise e  # Raise the exception after max retries


import time

def safe_get(driver, url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            driver.get(url)
            return  # Exit if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)  # Wait before retrying
    print("Failed to load the page after multiple attempts.")