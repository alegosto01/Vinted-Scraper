import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import requests
import os
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
import conversations as conv
import general_functions as gen_func
from whatsapp_api_client_python import API
import undetected_chromedriver as uc
import Scraper
import conversations as conv
import searches as search
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

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

import sys
import ssl

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

SBR_WEBDRIVER = 'https://brd-customer-hl_c6889560-zone-scraping_browser1:wu62tqar4piy@brd.superproxy.io:9515'


def main():


# SBR_WEBDRIVER = f'https://brd-customer-hl_c6889560-zone-scraping_browser1:11@brd.superproxy.io:9515'

# def main():

#         #!/usr/bin/env python
#     print('If you get error "ImportError: No module named \'six\'" install six:\n'+\
#         '$ sudo pip install six');
#     print('To enable your free eval account and get CUSTOMER, YOURZONE and ' + \
#         'YOURPASS, please contact sales@brightdata.com')

#     ssl._create_default_https_context = ssl._create_unverified_context
#     if sys.version_info[0]==2:
#         import six
#         from six.moves.urllib import request
#         opener = request.build_opener(
#             request.ProxyHandler(
#                 {'http': 'http://brd-customer-hl_c6889560-zone-web_unlocker1:amqftay7z516@brd.superproxy.io:22225',
#                 'https': 'http://brd-customer-hl_c6889560-zone-web_unlocker1:amqftay7z516@brd.superproxy.io:22225'}))
#         print(opener.open('https://www.vinted.it').read())
#     if sys.version_info[0]==3:
#         import urllib.request
#         opener = urllib.request.build_opener(
#             urllib.request.ProxyHandler(
#                 {'http': 'http://brd-customer-hl_c6889560-zone-web_unlocker1:amqftay7z516@brd.superproxy.io:22225',
#                 'https': 'http://brd-customer-hl_c6889560-zone-web_unlocker1:amqftay7z516@brd.superproxy.io:22225'}))
#         print(opener.open('https://www.vinted.it').read())

    # username = "brd-customer-hl_c6889560-zone-web_unlocker1"
    # password = "amqftay7z516"  # Replace with your password
    # proxy_host = "zproxy.lum-superproxy.io"
    # proxy_port = 22225
    # # proxy = {
    # #     'http': f'http://{username}:{password}@{proxy_host}:{proxy_port}',
    # #     'https': f'http://{username}:{password}@{proxy_host}:{proxy_port}'
    # # }
    # proxy = {
    #      'http': 'http://localhost:24000',
    #      'https': 'http://localhost:24000'
    # }   


    # try:
    #     response = requests.get('https://www.vinted.it', proxies=proxy)
    #     print(response.status_code)
    # except Exception as e:
    #     print(f"Error: {e}")


    # scraper = Scraper.Scraper() 
    # scraper.scrape_single_product(url="https://www.vinted.it/items/3919311596-adidas-campus-00s-black-and-white-gum-j?referrer=catalog" ,data_id=3919311596, dictionary=
    #                               search.air_force_1)


    new_scraper = Scraper.Scraper() 

    for i in range(5):
        print(f"Round {i}")
        for dictionary in search.programmed_searches:
            print(f"search = {dictionary}")
            input_search = dictionary["search"]
            product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}"


            scraped_data = new_scraper.scrape_products(dictionary)

            new_df = pd.DataFrame(scraped_data)

            #if it doesn't exists means that is the first search ever
            if os.path.exists(f"{product_root_folder}{input_search}.csv"):
                print("not first search i call compare and save")
                old_df = pd.read_csv()
                new_scraper.compare_and_save_df(new_df,old_df,input_search)
            else:
                old_df = new_df.copy()
                old_df.to_csv(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search}.csv")
                print("first search csv created")

            # Save the DataFrame to an Excel file
            #4
            # excel_file_path = f"{product_root_folder}{input_search}.xlsx" #zmiana lokacji zapisu pliku

            #new_df.to_excel(excel_file_path, index=False)
            print("Data exported to:", os.path.join(product_root_folder, input_search), ".csv")
            time.sleep(60)

    #     time.sleep(3600)









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
input("Press Enter to close the browser manually...")
