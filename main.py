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

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection



def main():



    # scraper = Scraper.Scraper()


    new_scraper = Scraper.Scraper() 
    # new_scraper.complete_df_with_sigle_scrapes(search.air_force_1)



    for i in range(1):
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
