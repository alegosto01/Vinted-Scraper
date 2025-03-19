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
import shutil
import tracemalloc
import ast
import getpass


# SBR_WEBDRIVER = f'http://brd-customer-hl_c6889560-zone-datacenter_proxy1:9rg06kk55uec@brd.superproxy.io:22225'

AUTH = 'brd-customer-hl_c6889560-zone-scraping_browser1:wu62tqar4piy'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'


def main():

    # get_images_forgotten("/home/ale/Desktop/Vinted-Web-Scraper/quick_sold_items_scarpe_donna.csv")
    
    # download_all_images("/home/ale/Desktop/Vinted-Web-Scraper/quick_sold_items_scarpe_donna.csv")
    
    # scraper.get_page_content("https://www.vinted.it/")

    # scraper = Scraper.Scraper()

    # scraper.complete_df_with_sigle_scrapes(search.mocassini_prada)

    # first_product_id = 0

# #     print("ricerca fedi santi")

# #     dictionary = search.search_fedi_santi

# #     scraper = Scraper.Scraper()
# #     print(f"search = {dictionary}")
# #     input_search = dictionary["search"]

# #     scraped_data = scraper.scrape_products(dictionary)
# #     columns = ['Title', 'Price', 'Brand', 'Size', 'Link', 'Likes', 'Dataid',
# # 'MarketStatus', 'SearchDate', 'Images']
# #     new_df = pd.DataFrame(scraped_data, columns=columns)


# #     # if i == 0:
# #     #     first_product_id = new_df['Dataid'].iloc[-1]
# #     #     print(f"First product id = {first_product_id}")


# #     #if it doesn't exists means that is the first search ever
# #     if os.path.exists(f"{input_search}/{input_search}.csv"):
# #         print("not first search i call compare and save")
# #         old_df = pd.read_csv(f"{input_search}/{input_search}.csv")
# #         scraper.compare_and_save_df(new_df,old_df,input_search)
# #     else:
# #         old_df = new_df.copy()
# #         old_df.reset_index(drop=True, inplace=True)  # This removes the old index
# #         old_df.to_csv(f"{input_search}/{input_search}.csv", index=False)
# #         print("first search csv created")

###############################################################################

    #initialize the output.txt file
    # output_file = open("output.txt", "w")
    # sys.stdout = output_file

    print(f"Date : {datetime.today}")

    # sys.stdout = sys.__stdout__
    # output_file.close()


    non_really_sold_items_ids = set()
    path = "/home/ale/Desktop/Vinted-Web-Scraper/ / .csv"
    big_csv_path = "/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv.csv"

    if os.path.exists(path):
        df = pd.read_csv(path)
        big_df = pd.read_csv(big_csv_path)

        # df.reset_index(drop=True, inplace=True)
        # big_df.reset_index(drop=True, inplace=True)

        new_df = pd.concat([df, big_df], ignore_index=True)
        new_df.to_csv(big_csv_path, index=False)

        try:
            shutil.rmtree("/home/ale/Desktop/Vinted-Web-Scraper/ /")
        except:
            pass
    times = []

    for i in range(10):
        print(f"Round {i}")
        for dictionary in search.programmed_searches:
            start_time = time.time()  # Start timer


            # Redirect sys.stdout to the file
            # output_file = open("output.txt", "a")

            # sys.stdout = output_file

            tracemalloc.start()

            current, peak = tracemalloc.get_traced_memory()

            print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
            print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

            scrape_for_quick_items(dictionary, i, non_really_sold_items_ids)

            # sys.stdout = sys.__stdout__

            # # Close the file
            # output_file.close()

            # After restoring, this will print to the console again
            # print("This will be printed on the console.")

            tracemalloc.stop()
            end_time = time.time()  # End timer
            elapsed_time = end_time - start_time  # Calculate elapsed time
            times.append(elapsed_time)
            print(f"Iteration time: {elapsed_time:.2f} seconds")  # Print time taken for this iteration

        time.sleep(10)

        # time.sleep(3600)
    print(times)


def get_images_forgotten(path):
    df = pd.read_csv(path)
    scraper = Scraper.Scraper()
    counter = 0
    for index, row in df.iloc[330:].iterrows():
        if row["Images"] == "[]":
            try:
                df.at[index, "Images"] = scraper.get_all_product_images(row["Link"])
            except:
                pass
            counter += 1
            if counter == 100:
                print("aggiornato csv")
                df.to_csv(path)
                break

def get_sold_items_slow(path):
    df = pd.read_csv(path)

def download_all_images(path):

    root_folder = "/home/ale/Desktop/Vinted-Web-Scraper/quick_sold_items_images/"
    already_downloaded = [int(name) for name in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, name))]

    df = pd.read_csv(path)
    df = df[df["Images"] != "[]"]
    df = df[~df["Dataid"].isin(already_downloaded)]
    print(len(df))
    counter = 0 
    for index, row in df.iterrows():
        print(f"Index: {index}")
        folder_path = os.path.join(root_folder,str(row["Dataid"]))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        images = ast.literal_eval(row['Images'])
        # print(f"data id = {type(images)}")
        for index_2, image_url in enumerate(images):
            print(f"Image {index_2 + 1}: {image_url}")
            gen_func.download_image(image_url, os.path.join(folder_path,str(index_2)))
        counter += 1
        time.sleep(5)
        # if counter == 50:
        #     break

def scrape_for_quick_items(dictionary, i, non_really_sold_items_ids):
    scraper = Scraper.Scraper()
    print(f"search = {dictionary}")
    input_search = dictionary["search"]
    # product_root_folder = f"{dictionary['search']}"

    scraped_data = scraper.scrape_products_serial(dictionary, i)
    columns = ['Title', 'Price', 'Brand', 'Size', 'Link', 'Likes', 'Dataid',
'MarketStatus', 'SearchDate', 'Images', "SearchCount", "Page"]
    new_df = pd.DataFrame(scraped_data, columns=columns)

    #if it doesn't exists means that is the first search ever
    if os.path.exists(f"{input_search}/{input_search}.csv"):
        print("not first search i call compare and save")
        old_df = pd.read_csv(f"{input_search}/{input_search}.csv")
        scraper.compare_and_save_df_serial(new_df,old_df,input_search, non_really_sold_items_ids)
    else:
        old_df = new_df.copy()
        old_df.reset_index(drop=True, inplace=True)  # This removes the old index
        old_df.to_csv(f"{input_search}/{input_search}.csv", index=False)
        # os.chmod("/home/ale/Desktop/Vinted-Web-Scraper/ /", 0o777)  # Set full read/write/execute permissions for all users
        # os.system(f"chown -R {getpass.getuser()}:{getpass.getuser()} {'/home/ale/Desktop/Vinted-Web-Scraper/ /'}")

        print("first search csv created")



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









# for index, row in df_iter.iterrows():
#             if row["Images"] != "" and row["Images"]:
#                 image_urls = row["Images"]
#                 print("good")
#             else:
#                 image_urls = []
#                 print("bad")
#                 break
#             if len(image_urls) > 0:
#             image_folder_path = os.path.join(root_folder,str(row["Dataid"]))
#             if not os.path.exists(image_folder_path):
#                 os.makedirs(image_folder_path)
#             for index_img, image_url in enumerate(image_urls):
#             image_url = image.get_attribute("src")
#                 print(f"Image {index_img + 1}: {image_url}")
#                 print("path exists i wont created it")
#                 gen_func.download_image(image_url,os.path.join(image_folder_path, str(index_img)))
#             downloaded_dataids.append(int(row["Dataid"]))