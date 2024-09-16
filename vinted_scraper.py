import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import schedule
import time
import filters as f
import searches as search
import notifications as notif
import scraping_functions as scrape
import conversations as conv
import general_functions as gen_func
from whatsapp_api_client_python import API
import undetected_chromedriver as uc
import Scraper

from selenium.webdriver.chrome.options import Options

# #translate_specs non serve più
# def translate_specs(dictionary, driver):
#     for key in dictionary:
#         filters = dictionary[key].split("-")
#         count = len(filters)

#         if key == "prezzoDa":
#             f.click_price_menu(driver)
#             f.set_price_from(driver, dictionary[key])
#         if key == "prezzoA":
#             f.set_price_to(driver, dictionary[key])
#             f.click_price_menu(driver)
#         if key == "condition":
#             if dictionary[key] == "nuovo senza cartellino":
#                 f.select_new_without_bill(driver)

#         if key == "colore":
#             f.click_color_list_menu(driver)
#             for i in range(count):
#                 if filters[i] == "bianco":
#                     f.select_white(driver)
#                 elif filters[i] == "nero":
#                     f.select_black(driver)

#         if key == "brand":
#             f.click_brand_list_menu(driver)

#             f.tick_brands(filters, driver)

#         if key == "sort":
#             f.click_sort_list_menu(driver)
#             f.sort_items(driver,dictionary[key])



scraper = Scraper(search.air_force_1)

# Convert the list of dictionaries to a DataFrame
data = scraper.scrape_products()

input_search = scraper.dictionary["search"]

new_df = pd.DataFrame(data)

old_df = pd.read_excel(f"{scraper.product_root_folder}{input_search}.xlsx")

#if there is nothing in the already saved excel
if old_df.empty:
    old_df = new_df.copy()

scraper.compare_and_save_df(new_df,old_df,input_search)

# Save the DataFrame to an Excel file
#4
excel_file_path = f"{scraper.product_root_folder}{input_search}.xlsx" #zmiana lokacji zapisu pliku

new_df.to_excel(excel_file_path, index=False)

print("Data exported to:", excel_file_path)



#stop from quitting the page    
input("Press Enter to close the browser manually...")
