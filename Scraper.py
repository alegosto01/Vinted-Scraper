
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
import dataset_cleaner
from seleniumwire import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


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

        # Initialize Chrome options
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

        #try to set connection
        for attempt in range(3):
            try:
                print('Connecting to Scraping Browser...')
                sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
                driver = Remote(sbr_connection, options=ChromeOptions())
                driver.set_page_load_timeout(120)  # Set timeout to 60 seconds
                print('Connected! Navigating to https://www.vinted.it...')
                driver.get('https://www.vinted.it')
                print("fatto")
                return driver
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(15)  # Wait before retrying
        print("Failed to load the page after multiple attempts.")

    # create the url setting all the filters of the search
    def create_webpage(self, dictionary): 

        #setting the input search
        input_search = str(dictionary["search"]).replace(" ","%20")
        input_search = "&search_text=" + input_search
        print("creo pagine")

        #get the page 
        gen_func.safe_get(self.driver,f"https://www.vinted.it/catalog?currency=EUR{input_search}")

        print("dormo")
        time.sleep(5)
        print("smetto di dormire")

        #set sorting order
        order = "&order=" + dictionary["sort"]

        #setting price fro and price to
        price_from = "" if dictionary["prezzoDa"] == " " else "&price_from=" + dictionary["prezzoDa"]
        price_to = "" if dictionary["prezzoA"] == " " else "&price_to=" + dictionary["prezzoA"]

        #set colors list
        color_list = dictionary["colore"].split("-")
        color_ids = f.find_color_ids(color_list)
        color_search = ""
        for color_id in color_ids:
            color_search = color_search + "&color_ids[]=" + color_id

        #set brand list
        brands_list = dictionary["brands"].split("-")
        brands_ids = f.find_brand_ids(self.driver, brands_list)
        brands_search = ""
        for brand_id in brands_ids:
            brands_search = brands_search + "&brand_ids[]=" + brand_id

        #set condition of the items
        status = "" if dictionary["status"] == " " else "&status_ids[]=" + dictionary["status"]
        
        #set item's category
        category = "" if dictionary["category"] == " " else "&catalog[]=" + search.categories[dictionary["category"]]

        #write the final webpage
        webpage = f"https://www.vinted.it/catalog?currency=EUR{order}{input_search}{color_search}{price_from}{price_to}{status}{brands_search}{category}"    
        return webpage

    #scrpe the catagol page and get the main info of the items
    def scrape_products(self, dictionary):
        #get input search
        input_search = dictionary["search"]

        #set path to main forlder of the search
        product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/"

        # Create directories if they don't exist
        if not os.path.exists(product_root_folder):
            os.makedirs(product_root_folder)  

        data = []

        #create the page to scrape
        webpage = self.create_webpage(dictionary)
        last_page = False

        #loop through all the pages available
        for page in range(10000):
            # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
            
            #load each page
            gen_func.load_page(self.driver, webpage, page+1)
            
            time.sleep(5)

            #if is the first access accept the cookies
            try:
                cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
                cookie.click()
            except:
                pass
            #if the previous page was empty then stop
            if last_page:
                print(f"finished at page {page+1}")
                break
            else:
                print(f"im at page {page+1}")

            #find list of products in the page
            products = self.driver.find_elements(By.CLASS_NAME, "new-item-box__overlay")

            #if the page has 0 products mean that we can stop scraping
            if len(products) == 0:
                last_page = True

            #get all the data from the products
            for product in products:

                #get link, dataid, and components (which contains tile, price, size and brand)
                title = gen_func.remove_illegal_characters(product.get_attribute("title"))
                components = gen_func.split_data(title)
                link = product.get_attribute("href")
                data_id = product.get_attribute("data-testid").split("-")

                if len(data_id) == 7:
                    data_id = data_id[3]
                else:
                    data_id = data_id[1]

                # Append the data to the list
                data.append({
                    "Title": components[0],
                    "Price": float(re.sub(r'[^\d.]', '', components[1].replace(',', '.'))), #remove non digits caracters and cast it to float
                    "Brand": components[2],
                    "Size": components[3],
                    "Link": link,
                    # "Image": img_url,
                    "Dataid": data_id,
                    "MarketStatus": "On Sale",
                    "SearchDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Images": []
                })
        return data
    
    #scrape the specific web page of an item
    def scrape_single_product(self, url, data_id, dictionary):

        #get path of the main folder of the search
        product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}"

        self.driver.get(url)
        page_exists = True

        #check if the age still exists
        try:
            # Try to find the "page doesn't exist" indicator element
            page_doesnt_exist = self.driver.find_element(By.XPATH, "//img[@src='https://marketplace-web-assets.vinted.com/assets/error-page/404-rack.svg']")
            print("Page does not exist.")  # This will execute if the element is found
            page_exists = False
        except NoSuchElementException:
            pass

        #f the page exists then get all the data, else remove the row from the df (for now)
        if page_exists:
            time.sleep(1)
            
            #get reviews count and star rating
            reviews_number_father = self.driver.find_element(By.XPATH, "//div[@class='web_ui__Rating__label']")
            reviews_count = 0
            try:
                reviews_count = int(reviews_number_father.find_element(By.XPATH, "//h4[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left']").text)
            except:
                pass

            stars = self.driver.find_elements(By.XPATH, "//div[@class='web_ui__Rating__star web_ui__Rating__full']")

            #get location
            location = self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='location']").text

            #get views
            views_count = int(self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='view_count']").text)

            #get interested people
            interested_count = 0
            try:
                interested_count = int(self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='interested']").text.split(" ")[0])
            except:
                pass


            #get upload date
            upload_date = " ".join(
                self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='upload_date']").text.split()[:-1]
                )
            
            #get item description
            item_description = self.driver.find_element(By.XPATH, "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']").text

            #click on one image to open the carousel
            image_button = self.driver.find_element(By.XPATH, "//button[@class='item-thumbnail']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", image_button)
            self.driver.execute_script("arguments[0].click();", image_button)

            time.sleep(2)
            #get all the images
            image_carousel = self.driver.find_element(By.XPATH, "//div[contains(@class, 'image-carousel__image-wrapper')]")
            images_element = image_carousel.find_elements(By.TAG_NAME, "img")
            image_urls = [img.get_attribute("src") for img in images_element]
            
            new_row = {
                "Images": image_urls,
                "Interested_count": interested_count,
                "View_count": views_count,
                "Item_description": item_description,
                "Upload_date": upload_date,
                "Dataid": data_id
            }
        else:
            new_row = []
            print("The page doesnt exist")
        return new_row

        # if len(stars) >= 4 and reviews_count > 3:
        #     print("almeno 4 stelle e 3 reviews")
        # else:
        #     print("non abbastanza stelle o reviews")
        

    def compare_and_save_df(self, new_df, old_df, input_search):
        # Identifying new items
        new_items = new_df[~new_df['Link'].isin(old_df['Link'])]
        new_items["MarketStatus"] = "New"

        # removed_items = old_df[~old_df['Link'].isin(new_df['Link'])]

        # mark sold items as sold
        old_df.loc[~old_df['Link'].isin(new_df['Link']), 'MarketStatus'] = 'Sold'


        # Save new items
        if not new_items.empty:
            old_df.append(new_df)
            old_df.to_csv(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search}.csv", index=False)

            # notif.sendMessage(f"Nuova Ricerca: {input_search}, {len(new_items)} Nuovi Items")


            #send message and download main image

            # count = 0
            # for index, row in enumerate(new_df):
            #     #send whatsapp messages
            #     # notif.sendMessage(f"Item {count}: {row.iloc[0]} '  ' {row.iloc[4]}")
            #     count += 1
            #     #download images
            #     data_id = row["Dataid"]
            #     img_link = row["Image"]
            #     if(img_link != ""):
            #         gen_func.ensure_path_exists(f'/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} images')
            #         gen_func.download_image(img_link, f'/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} images/{data_id}')



        # if not removed_items.empty:
        #     for row in removed_items:
        #     last_row = gen_func.get_last_non_empty_row_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items {input_search}.xlsx")
        #     with pd.ExcelWriter(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items {input_search}.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        #         removed_items.to_excel(writer, sheet_name='Sheet1', index=False, header=True, startrow= ++last_row)
        # else:
        #     print("nessun articolo è stato venduto")

        # Save the current state of the data
        # new_df.to_csv(file_path, index=False)

    #fill the database with additional data scraping every item's webpage
    def complete_df_with_sigle_scrapes(self, dictionary):

        csv_path = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/{dictionary['search']}.csv"
        images_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/{dictionary['search']} images"
        
        #read csv to modify it
        df = pd.read_csv(csv_path)

        print(f"len df = {len(df)}")
        #initialize a list of new rows to add to the csv
        new_rows = []

        #loop through the dataset to detect the row which are missing the info from the single product scrape
        for index, row in df.iterrows():  
            #if images is empty means that the row doesn't have the complete info
            #also check that the folder is not created already, if it is we can skip it
            if pd.isna(row["Images"]) and not os.path.exists(f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/{dictionary['search']} images/{row['Dataid']}"):
                self.driver = self.init_driver()

                #get the extra data
                new_row = self.scrape_single_product(str(row["Link"]), row["Dataid"], dictionary)


                if new_row:

                    #maybe this can removed
                    df["Images"] = df["Images"].astype("object")

                    #fill the images cell with the list of images just scraped
                    df.at[index, "Images"] = new_row["Images"]

                    # Remove the images from the new_row becauase right above i populated the column "images" in the original df
                    first_key = next(iter(new_row))
                    new_row.pop(first_key)

                    #download and store all the images
                    image_folder_path = gen_func.download_all_images(df.at[index, "Images"], dictionary, new_row["Dataid"])
                    
                    #check the images to recognize if the item is what we want
                    is_item_right = dataset_cleaner.check_single_item_images(dictionary, image_folder_path)
                else: #if new_row is empty means that the page doeas exist anymore
                    is_item_right = False

                #if the item is correct we store it otherwise we drop the whole row in the csv
                if is_item_right:
                    new_rows.append(new_row)
                else:
                    df.drop(index, inplace=True)  # Drop the row in the main DataFrame
            time.sleep(10)

        #create a temporary df with the new rows
        columns = ["Interested_count", "View_count", "Item_description", "Upload_date", "Dataid"]
        complementary_df = pd.DataFrame(new_rows, columns=columns)

        #maybe this row can be removed
        df.reset_index(drop=True, inplace=True)  # This removes the old index

        #add the temporary df witht he new rows to the original df
        new_df = df.set_index('Dataid').combine_first(complementary_df.set_index('Dataid')).reset_index()

        # add all new images and info to items 
        # new_df = pd.merge(df, complementary_df, on="Dataid", how="left")

        #overwrite the csv with the updated data
        new_df.to_csv(f"/home/ale/Desktop/Vinted-Web-Scraper/{dictionary['search']}/{dictionary['search']}.csv", index=False)

        



