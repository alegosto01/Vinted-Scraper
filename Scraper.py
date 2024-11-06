
import asyncio
# from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import searches as search
import filters as f
import general_functions as gen_func
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import Product
import os
from datetime import datetime

from seleniumwire import webdriver
from bs4 import BeautifulSoup

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

from webdriver_manager.chrome import ChromeDriverManager
# SCRAPEOPS_API_KEY = '5933586b-0a57-43ab-b57c-0f0e4086a22d'



AUTH = 'brd-customer-hl_c6889560-zone-scraping_browser1:wu62tqar4piy'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'
username = "brd-customer-hl_c6889560-zone-web_unlocker1"
password = "amqftay7z516"
brightdata_proxy = f"http://{username}-web-unlocker:{password}@zproxy.lum-superproxy.io:22225"


# f"http://{username}:{password}@zproxy.lum-superproxy.io:22225"

################# CODICE USATO PRIMA NEI TENTATIVI DI FAR FUNZIONARE BRIGHT DATA ##############À   
# class Scraper:
#     def __init__(self):
#         # self.dictionary = dictionary
#         self.driver = self.init_driver()
#         # self.product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{self.dictionary['search']}/"
        
#     def init_driver(self):
#         # Code to initialize Selenium WebDriver
#         # options = Options()
#         # options.add_argument("--log-level=3")  # Suppress logs by setting log level
#         # options.add_argument("--disable-logging")
#         # options.add_argument("--no-sandbox")
#         # options.add_argument("--disable-gpu")
#         # options.add_argument("--disable-dev-shm-usage")


#         options = uc.ChromeOptions()
#         options.add_argument(f'--proxy-server={brightdata_proxy}')

#         # options.add_experimental_option("detach", True)
#         # options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
#         # options.binary_location = r'/home/ale/Downloads/chromedriver-linux64/chromedriver'   #change to your location
#         #2
#         # latestchromedriver = ChromeDriverManager().install()

#         options.add_argument("--incognito")
#         options.add_argument('--disable-popup-blocking')
#         options.add_argument("--force-device-scale-factor=0.8")
#         PATH = r'/home/ale/Downloads/chromedriver-linux64/chromedriver' #change also to your location
#         # service = uc.chrome.service.Service(PATH)
#         # driver = uc.Chrome(options=options, use_subprocess=False,selenium ,driver_executable_path=latestchromedriver)
#         # driver.implicitly_wait(5)  # Wait for elements to load

#         ## Send Request Using ScrapeOps Proxy


#         print('Connecting to Scraping Browser...')
#         sbr_connection = ChromiumRemoteConnection(brightdata_proxy, 'goog', 'chrome')
#         driver = Remote(sbr_connection, options=ChromeOptions())
#         driver.get('https://www.vinted.it')
#         print("driver ready")
#         return driver

###################################


# Define Bright Data Proxy Information
username = "brd-customer-hl_c6889560-zone-web_unlocker1"
password = "amqftay7z516"  # Replace with your password
proxy_host = "zproxy.lum-superproxy.io"
proxy_port = 22225

# Proxy URL with authentication
brightdata_proxy = f"http://{username}:{password}@{proxy_host}:{proxy_port}"

class Scraper:
    def __init__(self):
        self.driver = self.init_driver()
        
    def init_driver(self):
        # # Initialize Chrome options
        chrome_options = ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings.images": 2,        # Disable images
            "profile.managed_default_content_settings.stylesheets": 2,   # Disable CSS
            "profile.managed_default_content_settings.fonts": 2,         # Disable fonts
            "profile.managed_default_content_settings.media_stream": 2,  # Disable media streaming
            "profile.default_content_setting_values.notifications": 2,   # Block notifications
            "profile.default_content_setting_values.popups": 2,          # Block popups
            "profile.default_content_setting_values.geolocation": 2,     # Block location sharing
            "profile.managed_default_content_settings.javascript": 1,    # Enable JS if necessary
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")  # Headless mode
        chrome_options.add_argument("--window-size=375,667")  # Mobile viewport for reduced traffic
        # options.add_argument("--incognito")
        # options.add_argument('--disable-popup-blocking')
        # options.add_argument("--force-device-scale-factor=0.8")

        # # Add proxy settings with authentication
        # options.add_argument(f'--proxy-server={brightdata_proxy}')
        
        # # Path to your ChromeDriver executable
        # chrome_driver_path = r'/home/ale/Downloads/chromedriver-linux64 (1)/chromedriver-linux64/chromedriver'

        # print('Connecting to the website using the Bright Data proxy...')

        # # Initialize the Selenium WebDriver using Chrome
        # driver = uc.Chrome(options=options, driver_executable_path=chrome_driver_path)

        # # Test by opening Vinted
        # driver.get('https://www.vinted.it')
        # print("Driver is ready and connected")
        print('Connecting to Scraping Browser...')
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        driver = Remote(sbr_connection, options=ChromeOptions())
        driver.set_page_load_timeout(120)  # Set timeout to 60 seconds
        print('Connected! Navigating to https://www.vinted.it...')
        driver.get('https://www.vinted.it')
        print("fatto")
        return driver

    def create_webpage(self, dictionary):
        input_search = str(dictionary["search"]).replace(" ","%20")
        input_search = "&search_text=" + input_search
        print("creo pagine")


        self.driver.get(f"https://www.vinted.it/catalog?currency=EUR{input_search}")

        print("dormo")
        time.sleep(5)

        print("smetto di domrire")

        order = "&order=" + dictionary["sort"]
        price_from = "&price_from=" + dictionary["prezzoDa"]
        price_to = "&price_to=" + dictionary["prezzoA"]

        color_list = dictionary["colore"].split("-")
        color_ids = f.find_color_ids(color_list)
        color_search = ""
        for color_id in color_ids:
            color_search = color_search + "&color_ids[]=" + color_id


        brands_list = dictionary["brands"].split("-")
        brands_ids = f.find_brand_ids(self.driver, brands_list)
        brands_search = ""
        for brand_id in brands_ids:
            brands_search = brands_search + "&brand_ids[]=" + brand_id

        status = "&status_ids[]=" + dictionary["status"]
        category = "&catalog[]=" + search.categories[dictionary["category"]]

        webpage = f"https://www.vinted.it/catalog?currency=EUR{order}{input_search}{color_search}{price_from}{price_to}{status}{brands_search}{category}"    
        return webpage

    def scrape_products(self, dictionary):
        input_search = dictionary["search"]
        product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/"

        # Create directories if they don't exist
        if not os.path.exists(product_root_folder):
            os.makedirs(product_root_folder)  

        data = []
        webpage = self.create_webpage(dictionary)
        last_page = False

        for page in range(10000):
            # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
            gen_func.load_page(self.driver, webpage, page+1)
            
            # self.driver.get(f"{webpage} + &page={page+1}")
            time.sleep(5)
            try:
                cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
                cookie.click()
            except:
                pass
            if last_page:
                print(f"finished at page {page+1}")
                break
            else:
                print(f"im at page {page+1}")


            products = self.driver.find_elements(By.CLASS_NAME, "new-item-box__overlay")

            if len(products) == 0:
                last_page = True

            for product in products:
                title = gen_func.remove_illegal_characters(product.get_attribute("title"))
                link = product.get_attribute("href")
                components = gen_func.split_data(title)
                data_id = product.get_attribute("data-testid").split("-")

                if len(data_id) == 7:
                    data_id = data_id[3]
                else:
                    data_id = data_id[1]

                #get image's url
                img_url = ""
                try:
                    img_url = self.driver.find_element(By.XPATH, f"//img[contains(@data-testid, '{data_id}--image')]")
                    img_url = img_url.get_attribute("src")
                except:
                    pass
                # product = Product(components[0], components[1], components[2], components[3], link, img_url, data_id)
                # data.append(product)

                # Append the data to the list
                data.append({
                    "Title": components[0],
                    "Price": components[1],
                    "Brand": components[2],
                    "Size": components[3],
                    "Link": link,
                    "Image": img_url,
                    "dataid": data_id,
                    "MarketStatus": "On Sale",
                    "SearchDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })
        return data
    

    def scrape_single_product(self, url, data_id, dictionary):
        product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/"

        self.driver.get(url)

        #get reviews count and rating
        reviews_number_father = self.driver.find_element(By.XPATH, "//div[@class='web_ui__Rating__label']")
        reviews_count = int(reviews_number_father.find_element(By.XPATH, "//h4[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left']").text)
        stars = self.driver.find_elements(By.XPATH, "//div[@class='web_ui__Rating__star web_ui__Rating__full']")

        #get location
        location = self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='location']").text

        #get views
        views_count = self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='view_count']").text

        #get interested people
        interested_count = self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='interested']").text.split(" ")[0]

        #get upload date
        upload_date = " ".join(
            self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='upload_date']").text.split()[:-1]
            )
        
        #get item description
        item_description = self.driver.find_element(By.XPATH, "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']").text




        #click on one image
        image_button = self.driver.find_element(By.XPATH, "//button[@class='item-thumbnail']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", image_button)
        self.driver.execute_script("arguments[0].click();", image_button)

        time.sleep(2)
        #get all the images
        # images_father = self.driver.find_elements(By.XPATH, "//div[@class='image-carousel__image-wrapper']")
        image_carousel = self.driver.find_element(By.XPATH, "//div[contains(@class, 'image-carousel__image-wrapper')]")
        images_element = image_carousel.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images_element]

        print(len(image_urls))
        for index, image_url in enumerate(image_urls):
            # image_url = image.get_attribute("src")
            print(f"Image {index + 1}: {image_url}")
            if not os.path.exists(f"{product_root_folder}{data_id}"):
                folder_path = os.join({product_root_folder},{data_id})
                os.makedirs(folder_path)
            gen_func.download_image(image_url, os.join(folder_path,{index}))

        if len(stars) >= 4 and reviews_count > 3:
            print("almeno 4 stelle e 3 reviews")
        else:
            print("non abbastanza stelle o reviews")
        

    def compare_and_save_df(self, new_df, old_df, input_search):
    # Identifying new items

        new_items = new_df[~new_df['Link'].isin(old_df['Link'])]
        new_items["MarketStatus"] = "New"

        # removed_items = old_df[~old_df['Link'].isin(new_df['Link'])]
        old_df.loc[~old_df['Link'].isin(new_df['Link']), 'MarketStatus'] = 'Sold'

        # print(len(removed_items))

        # Identifying removed items

        # Save new and removed items if any
        if not new_items.empty:
            old_df.append(new_df)
            #new_items.to_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/new_items {input_search}.xlsx", header=True, index=False)

            # notif.sendMessage(f"Nuova Ricerca: {input_search}, {len(new_items)} Nuovi Items")

            count = 0
            for index, row in enumerate(new_df):
                #send whatsapp messages
                # notif.sendMessage(f"Item {count}: {row.iloc[0]} '  ' {row.iloc[4]}")
                count += 1
                #download images
                data_id = row["dataid"]
                img_link = row["Image"]
                if(img_link != ""):
                    gen_func.ensure_path_exists(f'/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} images')
                    gen_func.download_image(img_link, f'/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} images/{data_id}')
        else:
            print("non ci sono nuovi articoli")
            gen_func.empty_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/new_items {input_search}.xlsx")


        # if not removed_items.empty:
        #     for row in removed_items:
        #     last_row = gen_func.get_last_non_empty_row_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items {input_search}.xlsx")
        #     with pd.ExcelWriter(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items {input_search}.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        #         removed_items.to_excel(writer, sheet_name='Sheet1', index=False, header=True, startrow= ++last_row)
        # else:
        #     print("nessun articolo è stato venduto")

        # Save the current state of the data
        # new_df.to_csv(file_path, index=False)





# def make_search(dictionary, driver):
#     data = []
#     # input_search = dictionary["search"]
#     # input_search.replace(" ","%20")
#     webpage = create_webpage(dictionary, driver)
#     last_page = False

#     for page in range(10000):
#         # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
#         driver.get(f"{webpage} + &page={page+1}")
#         time.sleep(5)
#         try:
#             cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
#             cookie.click()
#         except:
#             pass
#         if last_page:
#             print(f"finished at page {page+1}")
#             break
#         else:
#             print(f"im at page {page+1}")


#         products = driver.find_elements(By.CLASS_NAME, "new-item-box__overlay")

#         if len(products) == 0:
#             last_page = True

#         for product in products:
#             title = gen_func.remove_illegal_characters(product.get_attribute("title"))
#             link = product.get_attribute("href")
#             components = split_data(title)
#             data_id = product.get_attribute("data-testid").split("-")

#             if len(data_id) == 7:
#                 data_id = data_id[3]
#             else:
#                 data_id = data_id[1]

#             #get image's url
#             img_url = driver.find_element(By.XPATH, f"//img[contains(@data-testid, '{data_id}--image')]")
#             img_url = img_url.get_attribute("src")

        


#             # Append the data to the list
#             data.append({
#                 "Title": components[0],
#                 "Price": components[1],
#                 "Brand": components[2],
#                 "Size": components[3],
#                 "Link": link,
#                 "Image": img_url,
#                 "dataid": data_id
#             })
#     # Convert the list of dictionaries to a DataFrame
#     df = pd.DataFrame(data)

#     old_df = pd.read_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search}.xlsx")

#     #if there is nothing in the already saved excel
#     if old_df.empty:
#         old_df = df.copy()

#     compare_and_save_df(df,old_df,input_search)

#     # Save the DataFrame to an Excel file
# #4
#     excel_file_path = f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search}.xlsx" #zmiana lokacji zapisu pliku

#     df.to_excel(excel_file_path, index=False)

#     print("Data exported to:", excel_file_path)







# def get_images_from_products(driver, url):
#     # Locate image elements (this example uses XPATH to find all <img> tags)
#     images = driver.find_elements(By.XPATH, "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']")
    

#     # Loop through the images and print the 'src' attribute (image URLs)
#     for index, image in enumerate(images):
#         image_url = image.get_attribute("src")
#         print(f"Image {index + 1}: {image_url}")