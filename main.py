import asyncio
# from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import requests
import os
from datetime import datetime

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import schedule
import time
import filters as f
import searches as search
import notifications as notif
import conversations as conv
import general_functions as gen_func
from whatsapp_api_client_python import API
import undetected_chromedriver as uc
import Scraper
import conversations as conv
import searches as search
from selenium.webdriver.chrome.options import Options
import urllib.request
import os
import re
import requests
from bs4 import BeautifulSoup
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

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from urllib.request import build_opener, ProxyHandler, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import sys
import ssl

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.proxy import Proxy, ProxyType
import sys
import requests
import filters
# SBR_WEBDRIVER = f'http://brd-customer-hl_c6889560-zone-datacenter_proxy1:9rg06kk55uec@brd.superproxy.io:22225'

AUTH = 'brd-customer-hl_c6889560-zone-scraping_browser1:wu62tqar4piy'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'


def main():
    # scraper.get_page_content("https://www.vinted.it/")

    # scraper = Scraper.Scraper()

    # scraper.complete_df_with_sigle_scrapes(search.mocassini_prada)

    # first_product_id = 0

    non_really_sold_items_ids = []
    for i in range(10):
        print(f"Round {i}")
        for dictionary in search.programmed_searches:
            
            scraper = Scraper.Scraper()
            print(f"search = {dictionary}")
            input_search = dictionary["search"]
            product_root_folder = f"{dictionary['search']}"

            scraped_data = scraper.scrape_products_serial(dictionary, i)
            columns = ['Title', 'Price', 'Brand', 'Size', 'Link', 'Likes', 'Dataid',
    'MarketStatus', 'SearchDate', 'Images', "SearchCount", "Page"]
            new_df = pd.DataFrame(scraped_data, columns=columns)


            # if i == 0:
            #     first_product_id = new_df['Dataid'].iloc[-1]
            #     print(f"First product id = {first_product_id}")


            #if it doesn't exists means that is the first search ever
            if os.path.exists(f"{input_search}/{input_search}.csv"):
                print("not first search i call compare and save")
                old_df = pd.read_csv(f"{input_search}/{input_search}.csv")
                scraper.compare_and_save_df_serial(new_df,old_df,input_search, non_really_sold_items_ids)
            else:
                old_df = new_df.copy()
                old_df.reset_index(drop=True, inplace=True)  # This removes the old index
                old_df.to_csv(f"{input_search}/{input_search}.csv", index=False)
                print("first search csv created")

        time.sleep(20)

        # time.sleep(3600)





if __name__ == '__main__':
    main()

# air_force_1 = {"search":"air force 1 bianche",
#             "prezzoDa":"35",
#             "prezzoA":"70",
#             "status":"1",
#             "colore":"bianco",
#             "brands":"Air Force-Nike Air-Nike",
#             "sort":"newest_first",
#             "category": "scarpe uomo"}

# scraper = Scraper.Scraper(search.air_force_1)


# conv.log_in(scraper.driver)


# Convert the list of dictionaries to a DataFrame




#stop from quitting the page    


# def main():
#     # scraper = Scraper.Scraper()


#     proxy_options = {
#         'proxy': {
#             'http': 'http://brd-customer-hl_c6889560-zone-datacenter_proxy1:9rg06kk55uec@brd.superproxy.io:22225',
#             'https': 'https://brd-customer-hl_c6889560-zone-datacenter_proxy1:9rg06kk55uec@brd.superproxy.io:22225',
#             'no_proxy': 'localhost,127.0.0.1'
#         }
#     }

#     # Configure Chrome options
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")  # Optional: Run in headless mode if needed
#     chrome_options.add_argument("--window-size=1200,800")
#     custom_caps = {
#         'acceptInsecureCerts': True  # Example capability
#     }
#     chrome_options.add_experimental_option("prefs", custom_caps)

#     # Initialize Selenium Wire’s WebDriver with remote WebDriver settings
#     driver = webdriver.Remote(
#         command_executor="http://localhost:4444/wd/hub",  # Connect to the remote Selenium server
#         options=chrome_options,
#         seleniumwire_options=proxy_options  # Pass proxy settings to Selenium Wire
#     )

#     try:
#         # Navigate to the page
#         print("Connecting to Vinted...")
#         driver.get("https://www.vinted.it/catalog?search_text=adidas%20gazelle%20black%20and%20white&status_ids[]=1&color_ids[]=12&currency=EUR&time=1731535560")
#         print("Page loaded")

#         # Wait for the element to be available
#         brand_menu_button = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//h1[@class='web_ui__Text__text web_ui__Text__heading web_ui__Text__left']"))
#         )
#         if brand_menu_button:
#             print("Element found:", brand_menu_button)

#     except Exception as e:
#         print("Error occurred:", e)

#     finally:
#         driver.quit()
#         print("Browser closed.")
