from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import re
import pandas as pd
import searches as search
import filters as f
import general_functions as gen_func
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime
import dataset_cleaner
from selenium.common.exceptions import NoSuchElementException
import os
import re
from datetime import datetime
from requests_html import HTMLSession
import multiprocessing

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

import requests
#scraping browser proxy
AUTH = 'brd-customer-hl_c6889560-zone-scraping_browser1:wu62tqar4piy'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

# data center proxy
# SBR_WEBDRIVER = f'http://brd-customer-hl_c6889560-zone-datacenter_proxy1:9rg06kk55uec@brd.superproxy.io:22225'


#0ce4bdf2c54deb5096b627b4fba5ae18289f93c488150a496190eeb7c6aec936 # api token sivede in web_unlocker 
#0ce4bdf2c54deb5096b627b4fba5ae18289f93c488150a496190eeb7c6aec936
#b400c1d0-9386-4d0f-b2a6-84dd19356b0c # api token non si vede più

api_token = os.getenv("API_TOKEN")
proxy = "http://brd-customer-hl_c6889560-zone-web_unlocker1:@brd.superproxy.io:22225"

# Proxy URL with authentication
class Scraper:
    # def __init__(self):
        
    def init_driver(self):
        extension_path = "proxy_auth_extension/proxy_auth_extension.zip"

        # Set up Chrome options with your preferences
        chrome_options = Options()
        prefs = {
            "profile.managed_default_content_settings.images": 2,        # Disable images
            "profile.managed_default_content_settings.stylesheets": 2,   # Disable CSS
            "profile.managed_default_content_settings.fonts": 2,         # Disable fonts
            "profile.managed_default_content_settings.media_stream": 2,  # Disable media streaming
            "profile.default_content_setting_values.notifications": 2,   # Block notifications
            "profile.default_content_setting_values.popups": 2,          # Block popups
            "profile.default_content_setting_values.geolocation": 2,     # Block location sharing
            "profile.managed_default_content_settings.javascript": 1,    # Enable JavaScript if necessary
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless=new")  # Run in headless mode
        chrome_options.add_argument("--window-size=375,667")  # Mobile viewport

        #try to set connection
        for attempt in range(3):
            try:
                print('Connecting to Scraping Browser...')
                sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
                driver = Remote(sbr_connection, options=ChromeOptions())
                driver.set_page_load_timeout(120)  # Set timeout to 60 seconds
                # print('Connected! Navigating to https://www.vinted.it...')
                # driver.get('https://www.vinted.it')
                print("fatto")
                return driver
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(15)  # Wait before retrying
        print("Failed to load the page after multiple attempts.")
    
    def get_page_content_quick(self, url):
        payload = {
            "zone": "web_unlocker1",             
            "url": url,    # Target URL
            "format": "html",                 # Raw HTML format
            "method": "GET",                 # Use the GET method
            "country": "IT"                  # Use a US-based proxy
        }
        headers = {
            "Authorization": api_token,  # Replace with your actual API token
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"  # or another referring URL if needed
        }
        response = requests.get(url, params=payload, headers=headers)
        time.sleep(2)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None
    def get_page_content(self, url, timeout=20, sleep=10):
        # url = "https://www.vinted.it/catalog?search_text=air%20force%20men&time=1731608194"

        success = False
        attempts = 0
    
        session = HTMLSession()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        payload = {
            "zone": "web_unlocker1",             
            "url": url,    # Target URL
            "format": "html",                 # Raw HTML format
            "method": "GET",                 # Use the GET method
            "country": "IT"                  # Use a US-based proxy
        }
        headers = {
            "Authorization": api_token,  # Replace with your actual API token
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"  # or another referring URL if needed
        }

        response = session.get(url, json=payload, headers=headers, timeout=40)
        time.sleep(2)
        if response.status_code == 200:
            # Parse the HTML content from the response
            html = response.html
            # Optionally render JavaScript if the content is dynamically loaded
            max_retries = 3
            retry_count = 0

            # while retry_count < max_retries:
            try:
                html.render(timeout=timeout, sleep=sleep)  # Adjust sleep if needed to allow content to load
                # break  # Exit the loop if successful
            except:
                retry_count += 1
                print(f"Timeout occurred. Retrying {retry_count}/{max_retries}...")
                # time.sleep(15)  # Optional: Wait before retrying
            # else:
            #     print("Failed to render page after multiple retries.")
            #     # Add fallback or exit logic
            if html:
                success = True    
                return html
            else:
                print("page not loaded")
                return None
        else:
            print("Failed to retrieve the page:", response.status_code)
            print("Response message:", response.text[:20])  # Print the first 500 characters of the response
    
    def fetch_page_and_check(self,item, non_really_sold_items_ids):
        try:
            # if int(item["Dataid"]) in non_really_sold_items_ids:
            #     return item, False, "AlreadyChecked"
            url = item["Link"]
            html_content = self.get_page_content(url, timeout=60, sleep=30)
            time.sleep(2)

            if html_content:
                element = html_content.find('div[data-testid="item-status--content"]', first=True)
                if element and element.text == "Venduto":
                    return item, True, "Sold"
            time.sleep(5)
            return item, False, "On Sale"
        except Exception:
            time.sleep(3)
            return item, False, "On Sale"
        
    # create the url setting all the filters of the search
    def create_webpage(self, dictionary): 
        input_search = str(dictionary["search"]).replace(" ","%20")
        input_search = "&search_text=" + input_search
        #set sorting order
        order = "&order=" + dictionary["sort"]

        #setting price fro and price to
        price_from = "" if dictionary["prezzoDa"] == " " else "&price_from=" + dictionary["prezzoDa"]
        price_to = "" if dictionary["prezzoA"] == " " else "&price_to=" + dictionary["prezzoA"]

        #set colors list
        color_search = ""
        if dictionary["colore"] != " ":
            color_list = dictionary["colore"].split("-")
            color_ids = f.find_color_ids(color_list)
            for color_id in color_ids:
                color_search = color_search + "&color_ids[]=" + color_id

        #set brand list
        brands_search = ""

        if dictionary["brands"] != " ":
            brands_list = dictionary["brands"].split("-")
            brands_ids = []
            non_saved_brands = []

            brands_df = pd.read_csv("brand_ids.csv")
            # brand_dict = dict(zip(brands_df['brand'], brands_df['brand_id']))

            for brand in brands_list:
                #if i don't already have the brand saved is search it
                if brand not in brands_df["Brand"].values:
                    non_saved_brands.append(brand)
                else: #if i have it i just take it
                    brands_ids.append(brands_df.loc[brands_df['Brand'] == brand, 'Brand_id'].iloc[0])
                
            if non_saved_brands:
                        #setting the input search

                print("creo pagine")
                
                self.driver = self.init_driver()

                #get the page 
                gen_func.safe_get(self.driver,f"https://www.vinted.it/catalog?currency=EUR{input_search}")
                try:
                    cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
                    cookie.click()
                except:
                    pass
                # with open("output.txt", "w") as file:
                #     file.write(self.driver.page_source)

                print("dormo")
                time.sleep(5)
                print("smetto di dormire")

                print("brand non salvati ancora, li cerco")
                brands_ids.extend(f.find_brand_ids(self.driver, non_saved_brands))
                self.driver.quit()

            for brand_id in brands_ids:
                print(brand_id)
                brands_search = brands_search + "&brand_ids[]=" + str(brand_id)

        #set condition of the items
        condition = "" if dictionary["condition"] == " " else "&status_ids[]=" + dictionary["condition"]
        
        #set item's category
        category = "" if dictionary["category"] == " " else "&catalog[]=" + search.categories[dictionary["category"]]




        webpage = f"https://www.vinted.it/catalog?currency=EUR{order}{input_search}{color_search}{price_from}{price_to}{condition}{brands_search}{category}"    
        # webpage = "https://www.vinted.it/catalog?search_text=adidas%20gazelle%20black%20and%20white&status_ids[]=1&color_ids[]=12&currency=EUR"
        return webpage

    #scrpe the catagol page and get the main info of the items
    def scrape_products(self, dictionary):

        #get input search
        input_search = dictionary["search"]

        #set path to main forlder of the search
        product_root_folder = f"{dictionary['search']}/"

        # Create directories if they don't exist
        if not os.path.exists(product_root_folder):
            os.makedirs(product_root_folder)  

        data = []

        #create the page to scrape
        webpage = self.create_webpage(dictionary)
        last_page = False

        #loop through all the pages available
        page = 0


        for i in range(10):
            new_webpage = webpage + "&page=" + str(page+1)
            print(f"im searching in {new_webpage}")

            html_content = self.get_page_content(new_webpage, timeout=20, sleep=10)

            try:
                element = html_content.find('meta[content="Una community, migliaia di brand e tantissimo stile second-hand. Ti va di iniziare? Ecco come funziona."]', first=True)
            except:
                continue
                
            
            time.sleep(5)


            #if the previous page was empty then stop
            if last_page:
                # page -= 1
                print(f"finished at page {page+1}")
                break
            else:
                print(f"im at page {page+1}")

                    #find list of products in the page
            products = html_content.find('.new-item-box__overlay')


            all_likes_counts = html_content.find('.u-background-white.u-flexbox.u-align-items-center.new-item-box__favourite-icon')

            #if the page has 0 products mean that we can stop scraping
            print(f"len products = {len(products)}")

            if len(products) == 0:
                last_page = True

            #get all the data from the products
            for product in products:

                #get link, dataid, and components (which contains tile, price, size and brand)
                title = gen_func.remove_illegal_characters(product.attrs.get("title"))
                components = gen_func.split_data(title)
                link = product.attrs.get("href")
                if "referrer=catalog" not in link:
                    continue
                data_id = product.attrs.get("data-testid", "").split("-")

                if len(data_id) == 7:
                    data_id = data_id[3]
                else:
                    data_id = data_id[1]


                likes_count = 0

                for element in all_likes_counts:
                    # Retrieve the "data-testid" attribute
                    element_data_test_id = element.attrs.get("data-testid", "")
                    
                    # Check if data_test_id contains the desired data_id
                    if data_id and data_id in element_data_test_id:
                        aria_label = element.attrs.get("aria-label","")
                        if aria_label != "Aggiungi ai preferiti": # if equal means 0 likes
                            likes_count = aria_label.split("Aggiunto ai preferiti da ")[1].split(" ")[0] # Adjust based on actual aria-label structure
                            break  # Stop once the correct element is found

                
                # Append the data to the list
                data.append({
                    "Title": components[0],
                    "Price": float(re.sub(r'[^\d.]', '', components[1].replace(',', '.'))), #remove non digits caracters and cast it to float
                    "Brand": components[2],
                    "Size": components[3],
                    # "Condition": search.condition_dict[dictionary[condition]],
                    "Link": link,
                    "Likes": likes_count,
                    "Dataid": str(data_id),
                    "MarketStatus": "On Sale",
                    "SearchDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Images": []
                })
            
            page += 1
        return data       


    #scrpe the catagol page and get the main info of the items
    def scrape_products_serial(self, dictionary, search_count):

        #get input search
        input_search = dictionary["search"]

        #set path to main forlder of the search
        product_root_folder = f"{dictionary['search']}/"

        # Create directories if they don't exist
        if not os.path.exists(product_root_folder):
            os.makedirs(product_root_folder)  

        data = []

        #create the page to scrape
        webpage = self.create_webpage(dictionary)
        last_page = False

        #loop through all the pages available
        page = 0

        for i in range(10):
            new_webpage = webpage + "&page=" + str(page+1)
            print(f"im searching in {new_webpage}")

            html_content = self.get_page_content(new_webpage, timeout=25, sleep=5)

            try:
                element = html_content.find('meta[content="Una community, migliaia di brand e tantissimo stile second-hand. Ti va di iniziare? Ecco come funziona."]', first=True)
            except:
                continue

            # time.sleep(5)

            #if the previous page was empty then stop
            if last_page:
                # page -= 1
                print(f"finished at page {page+1}")
                break
            else:
                print(f"im at page {page+1}")

                    #find list of products in the page
            products = html_content.find('.new-item-box__overlay')

            all_likes_counts = html_content.find('.u-background-white.u-flexbox.u-align-items-center.new-item-box__favourite-icon')

            #if the page has 0 products mean that we can stop scraping
            print(f"len products = {len(products)}")

            if len(products) == 0:
                last_page = True

            #get all the data from the products
            for product in products:

                #get link, dataid, and components (which contains tile, price, size and brand)
                title = gen_func.remove_illegal_characters(product.attrs.get("title"))
                components = gen_func.split_data(title)
                link = product.attrs.get("href")
                if "referrer=catalog" not in link:
                    continue
                data_id = product.attrs.get("data-testid", "").split("-")

                if len(data_id) == 7:
                    data_id = data_id[3]
                else:
                    data_id = data_id[1]

                likes_count = 0

                for element in all_likes_counts:
                    # Retrieve the "data-testid" attribute
                    element_data_test_id = element.attrs.get("data-testid", "")
                    
                    # Check if data_test_id contains the desired data_id
                    if data_id and data_id in element_data_test_id:
                        aria_label = element.attrs.get("aria-label","")
                        if aria_label != "Aggiungi ai preferiti": # if equal means 0 likes
                            likes_count = aria_label.split("Aggiunto ai preferiti da ")[1].split(" ")[0] # Adjust based on actual aria-label structure
                            break  # Stop once the correct element is found

                
                # Append the data to the list
                data.append({
                    "Title": components[0],
                    "Price": float(re.sub(r'[^\d.]', '', components[1].replace(',', '.'))), #remove non digits caracters and cast it to float
                    "Brand": components[2],
                    "Size": components[3],
                    # "Condition": search.condition_dict[dictionary[condition]],
                    "Link": link,
                    "Likes": likes_count,
                    "Dataid": str(data_id),
                    "MarketStatus": "On Sale",
                    "SearchDate": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Page": page+1,
                    "SearchCount": search_count,
                    "Images": []
                })
            
            page += 1
        return data       
    

    
    #scrape the specific web page of an item
    def scrape_single_product(self, url, data_id, get_images = False): #dictionary was a parameter
        #get path of the main folder of the search
        # product_root_folder = f"{dictionary['search']}"
        # self.driver = self.init_driver()

        html_content = self.get_page_content(url, timeout=40, sleep=20)
        if html_content is None:
            return [], []
        page_exists = True

        # #check if the page still exists
        # try:
        #     # Try to find the "page doesn't exist" indicator element

        #     page_doesnt_exist = html_content.find("img[src='https://marketplace-web-assets.vinted.com/assets/error-page/404-rack.svg']")
        #     # page_doesnt_exist = self.driver.find_element(By.XPATH, "//img[@src='https://marketplace-web-assets.vinted.com/assets/error-page/404-rack.svg']")
        #     print("Page does not exist.")  # This will execute if the element is found
        #     page_exists = True ###DA METTERE FALSE
        # except NoSuchElementException:
        #     pass

        #f the page exists then get all the data, else remove the row from the df (for now)
        if page_exists:

            print("PAge EXISTS")            
            #get reviews count and star rating
            time.sleep(2)
            try:
                reviews_element = html_content.find("div[class='web_ui__Rating__rating web_ui__Rating__small']", first=True).text
                # reviews_element = html_content.find("h4[class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left']").text
                reviews_count = int(reviews_element)
            except:
                print("PAGE FAILED TO LOAD")
                reviews_count = 0

            # try:
            try:
                stars_element = html_content.find("div[class='web_ui__Rating__rating web_ui__Rating__small']", first=True)
                stars_text = stars_element.attrs.get("aria-label").split(" ")
                if len(stars_text) == 10:
                    stars = stars_element.attrs.get("aria-label").split(" ")[6]
                else:
                    stars = stars_element.attrs.get("aria-label").split(" ")[2]
            except:
                stars = -1
            # stars = self.driver.find_elements(By.XPATH, "//div[@class='web_ui__Rating__star web_ui__Rating__full']")

            try:
                #get location
                location_element = html_content.find("div.details-list__item-value--redesign[itemprop='location']", first=True)
                location = location_element.text if location_element else None            
                # location = self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='location']").text

            except:
                location = "Unknown"

            try:
                #get views
                views_count_element = html_content.find("div.details-list__item-value--redesign[itemprop='view_count']", first=True)
                views_count = int(views_count_element.text) if views_count_element else None  
                # views_count = int(self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='view_count']").text)
            except:
                views_count = -1
            
            
            #get interested people
            try:
                interested_count_element = html_content.find("div.details-list__item-value--redesign[itemprop='interested']", first=True)
                interested_count = int(interested_count_element.text.split(" ")[0]) if interested_count_element else None  
                # interested_count = int(self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='interested']").text.split(" ")[0])
            except:
                interested_count = -1

            try:
                #get upload date
                upload_date = " ".join(
                    html_content.find("div.details-list__item-value--redesign[itemprop='upload_date']", first=True).text.split()[:-1]
                    # self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='upload_date']").text.split()[:-1]
                    )
            except:
                upload_date = "Unknown"
            
            try:
                #get item description
                item_description = html_content.find("span[class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']", first=True).text
                # item_description = self.driver.find_element(By.XPATH, "//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']").text
            except:
                item_description = "Unknown"
            try:
                #get seller name
                seller_name = html_content.find(f"span[data-testid*='profile-username']", first=True).text
            except:
                seller_name = "Unknown"
            # except:
            #     print("problem finding something")
            #     return [], []
            
            try:
                item_condition_element = html_content.find("div[data-testid='item-attributes-status']", first=True)
                item_condition = item_condition_element.find("div[class='details-list__item-value--redesign']", first=True).text
            except:
                item_condition = "Unknown"

            print(f"condition = {item_condition}")
            new_seller_row = {
                    "SellerId": " ",
                    "SellerName": seller_name,
                    "Location": location,
                    "ItemCondition": item_condition,
                    "ItemDescription": item_description,
                    "ReviewsCount": reviews_count,
                    "Stars": stars
            }



            # #checking if the seller is already saved or not and adding it if not
            # if seller_name in seller_df["SellerName"].values:
            #     seller_id = seller_df.loc[seller_df["SellerName"] == seller_name, "SellerId"].values[0]
            # else:
            #     max_id += 1
            #     seller_id = max_id
            #     # seller_id = seller_df["SellerId"].iloc[-1] + 1
            #     new_seller_row = {
            #         "SellerId": max_id,
            #         "SellerName": seller_name,
            #         "Location": location,
            #         "ReviewsCount": reviews_count,
            #         "Stars": stars
            #     }
            #     seller_df = pd.concat([seller_df, pd.DataFrame([new_seller_row])], ignore_index=True)

            ### get images or not depending on what is set in the bool parameter get_images
            if get_images:
                print("getting images urls")
                image_urls = self.get_all_product_images(url)
            else:
                image_urls = []

            new_row = {
                "Images": image_urls,
                "Interested_count": interested_count,
                "View_count": views_count,
                "Description": item_description,
                "Condition": item_condition,
                "Upload_date": upload_date,
                "Dataid": data_id,
                "SellerId": " ",
                "SellerName": seller_name
            }
        else:
            new_row = []
            print("The page doesnt exist")
        
        print(f"new row = {new_row}")
        return new_row, new_seller_row

        # if len(stars) >= 4 and reviews_count > 3:
        #     print("almeno 4 stelle e 3 reviews")
        # else:
        #     print("non abbastanza stelle o reviews")
        
    def get_all_product_images(self, url):
        self.driver = self.init_driver()

        gen_func.safe_get(self.driver,url)

        #click on one image to open the carousel

        image_button = self.driver.find_element(By.XPATH, "//button[@class='item-thumbnail']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", image_button)
        self.driver.execute_script("arguments[0].click();", image_button)

        time.sleep(2)
        #get all the images
        image_carousel = self.driver.find_element(By.XPATH, "//div[contains(@class, 'image-carousel__image-wrapper')]")
        images_element = image_carousel.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images_element]
        return image_urls

    def compare_and_save_df_serial(self, new_df, old_df, input_search, non_really_sold_items_ids):

        print("in compare and save")
        # Identifying new items
        # old_df['Link'] = old_df['Link'].astype(str).str.strip()
        # new_df['Link'] = new_df['Link'].astype(str).str.strip()


        # new_df = new_df.loc[~(new_df['Link']).isin(old_df['Link'])]
        # old_df.loc[~(old_df['Link']).isin(new_df['Link']), 'MarketStatus'] = 'Sold'

        ############### above old approach, doesn't work########


        ############ ????should i mark the new items as new ???????#########
        # new_df.loc[:, "MarketStatus"] = "New"


        link_list_old = list(old_df["Link"].values)
        link_list_new = list(new_df["Link"].values)

        for link in link_list_new:
            if link in link_list_old:
                old_df.loc[old_df["Link"] == link, "SearchDate"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                # if old_df:
                new_df = new_df.drop(new_df[new_df['Link'] == link].index)


        print("dropped dubpliactes and updates search date")
        new_items_count = len(new_df)

        # for index, row in old_df.iterrows():
        #     if row["MarketStatus"] != "OutOfSearch":
                # if row["MarketStatus"] == "On Sale":
                    
        items_sold_to_check = []


        for link in link_list_old:
            if link not in link_list_new:
                old_df.loc[old_df["Link"] == link, "MarketStatus"] = "Sold"

        print("marked sold items")

        print(f"new items count {new_items_count}")

        min_search = old_df["SearchCount"].min()
        max_pag = old_df["Page"].max()
        
        while len(old_df) + new_items_count > 900:
            print(f"Before drop: LEN = {len(old_df)}, New Items Count = {new_items_count}")
            
            print(f"Min SearchCount: {min_search}, Max Page: {max_pag}")
            rows_to_drop = old_df[(old_df["SearchCount"] == min_search) & (old_df["Page"] == max_pag)]
            
            if rows_to_drop.empty:
                print("No rows to drop, breaking to avoid infinite loop.")
            else:        
                old_df = old_df.drop(rows_to_drop.index)
                print(f"After drop: LEN = {len(old_df)}")
            
            if max_pag == 1:
                min_search += 1
                max_pag = 10
            else:
                max_pag -= 1
            

        print("dropped outofsearch items")


        items_to_fully_scrape = []

        ## check if they are actually sold or just not found

        quick_sold_items_df = pd.read_csv(f"quick_sold_items_scarpe_donna.csv")



        items_sold_to_check = old_df.loc[old_df["MarketStatus"] == "Sold"]

        # items_sold_to_check = [item for item in items_sold_to_check.ite if int(item["Dataid"]) not in non_really_sold_items_ids]
        
        items_sold_to_check = items_sold_to_check[~items_sold_to_check['Dataid'].isin(non_really_sold_items_ids)]
        items_sold_to_check = items_sold_to_check[~items_sold_to_check['Dataid'].isin(list(quick_sold_items_df["Dataid"].values))]

        # items_sold_to_check = [item for item in items_sold_to_check if int(item["Dataid"]) not in list(quick_sold_items_df["Dataid"].values)]

        
        print(f"len sold items {len(items_sold_to_check)}")

        # items_sold_to_check = [item for item in items_sold_to_check if int(item["Dataid"]) not in non_really_sold_items_ids]

        # for index, item in items_sold_to_check.iterrows():
        #     if int(item["Dataid"]) not in non_really_sold_items_ids:
        #         url = item["Link"]
        #         html_content = self.get_page_content_quick(url)
        #         if html_content:
        #             print("page loaded")
        #             try:
        #                 element = html_content.find('div[data-testid="item-status--content"]', first=True)
        #                 if element.text == "Venduto":
        #                     items_to_fully_scrape.append(item)
        #                     print("item sold for real")
        #                     print(item["Title"])
        #             except:
        #                 old_df.loc[old_df["Link"] == url, "MarketStatus"] = "On Sale"
        #                 non_really_sold_items_ids.add(int(item["Dataid"]))
        #                 print("item not sold")
        #         else:
        #             old_df.loc[old_df["Link"] == url, "MarketStatus"] = "On Sale"
        #             print("item not sold")
        #         time.sleep(1)
        #     else:
        #         print("item already checked and was not actually sold before")

        # Parallel execution
        items_to_fully_scrape = []
        non_really_sold_items_ids = []

        max_workers = min(8, multiprocessing.cpu_count())

        with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers based on system/network capacity
            futures = [executor.submit(self.fetch_page_and_check, row, non_really_sold_items_ids)
                    for _, row in items_sold_to_check.iterrows()]

            for future in as_completed(futures):
                item, sold, status = future.result()
                if sold:
                    items_to_fully_scrape.append(item)
                    print(f"Item sold for real: {item['Title']} + {item['Link']}")
                else:
                    if status == "On Sale":
                        non_really_sold_items_ids.append(int(item["Dataid"]))
                        old_df.loc[old_df["Link"] == item["Link"], "MarketStatus"] = "On Sale"
                    print(f"Item not sold: {item['Title']}")

        print("Parallel scraping complete.")

        
        seller_df = pd.read_csv(f"Sellers.csv")

        new_seller_rows = []      
        new_quick_sold_rows = []


        ## SCRAPE FULLY THE ITEMS JUST SOLD
        # for item in items_to_fully_scrape:

        print(f"Items to fully scrape: {len(items_to_fully_scrape)}")
        for item in items_to_fully_scrape:
            url = item["Link"]
            data_id = item["Dataid"]
            new_row, new_seller_row = self.scrape_single_product(url, data_id)
            

            if new_row and new_seller_row["ReviewsCount"] > 3 and float(new_seller_row["Stars"]) > 3.0:
                print("new row added")
                new_seller_rows.append(new_seller_row)
                full_row = {
                    "Images": new_row["Images"],
                    "Interested_count": new_row["Interested_count"],
                    "View_count": new_row["View_count"],
                    "Item_description": new_row["Description"],
                    "Condition": new_row["Condition"],
                    "Upload_date": new_row["Upload_date"],
                    "Dataid": new_row["Dataid"],
                    "SellerId": " ",
                    "SellerName": new_row["SellerName"],
                    "Title": item["Title"],
                    "Price": item["Price"], #remove non digits caracters and cast it to float
                    "Brand": item["Brand"],
                    "Size": item["Size"],
                    "Link": item["Link"],
                    "Likes": item["Likes"],
                    "MarketStatus": "Sold",
                    "SearchDate": item["SearchDate"],
                    "Page": item["Page"],   
                    "SearchCount": item["SearchCount"]
                }
                new_quick_sold_rows.append(full_row)
            else:
                print("seller not good enough")
                old_df.loc[old_df["Link"] == url, "MarketStatus"] = "On Sale"
                non_really_sold_items_ids.append(int(data_id))

    
        max_id = seller_df["SellerId"].max()
        columns_seller = ["SellerId", "SellerName", "Location", "ReviewsCount", "Stars"]

        temp_seller_df = pd.DataFrame(new_seller_rows, columns=columns_seller)
        temp_seller_df.drop_duplicates(subset=["SellerName"], keep='first', inplace=True)

        #create a temporary df with the new rows
        columns = ["Images","Interested_count","View_count","Item_description","Condition","Upload_date","Dataid","SellerId","SellerName","Title","Price","Brand","Size","Link","Likes","MarketStatus","SearchDate","Page","SearchCount"]
        complementary_df = pd.DataFrame(new_quick_sold_rows, columns=columns)

        for index, row in complementary_df.iterrows():  
            if row["SellerName"] in seller_df["SellerName"].values:
                seller_id = seller_df.loc[seller_df["SellerName"] == row["SellerName"], "SellerId"].values[0]
                complementary_df.at[index, "SellerId"] = seller_id  # Modify directly in DataFrame
                temp_seller_df.drop(temp_seller_df[temp_seller_df["SellerName"] == row["SellerName"]].index, inplace=True)
            else:
                max_id += 1
                complementary_df.at[index, "SellerId"] = max_id  # Modify directly in DataFrame
                temp_seller_df.loc[temp_seller_df["SellerName"] == row["SellerName"], "SellerId"] = max_id

    #maybe this row can be removed
    # df.reset_index(drop=True, inplace=True)  # This removes the old index

    #add the temporary df with the new rows to the original df
    # new_df = df.set_index('Dataid').combine_first(complementary_df.set_index('Dataid')).reset_index()
    # new_df.to_csv(f"{dictionary['search']}/{dictionary['search']}.csv", index=False)
    
    
        new_seller_df = pd.concat([seller_df, temp_seller_df], ignore_index=True)
        new_seller_df.to_csv(f"Sellers.csv", index=False)            
        
        quick_sold_items_df = pd.concat([quick_sold_items_df, complementary_df], ignore_index=True)

        quick_sold_items_df.to_csv(f"quick_sold_items_scarpe_donna.csv", index=False)
        
        print("Temp seller df:")
        print(temp_seller_df)

        print("Quick sold items df:")
        print(quick_sold_items_df)


        



        print("Before concat")

        # Save new items
        if len(new_df) > 0:
            print("concateno il nuovo dataset")
            old_df = pd.concat([old_df, new_df], ignore_index=True)
            old_df = old_df.drop_duplicates(subset=["Link"], keep='first', inplace=False)
            old_df.to_csv(f"{input_search}/{input_search}.csv", index=False)

            # notif.sendMessage(f"Nuova Ricerca: {input_search}, {len(new_items)} Nuovi Items")


            # send message and download main image

            # count = 0
            # for index, row in enumerate(new_df):
            #     #send whatsapp messages
            #     # notif.sendMessage(f"Item {count}: {row.iloc[0]} '  ' {row.iloc[4]}")
            #     count += 1
            #     #download images
            #     data_id = row["Dataid"]
            #     img_link = row["Image"]
            #     if(img_link != ""):
            #         gen_func.ensure_path_exists(f'{input_search}/{input_search} images')
            #         gen_func.download_image(img_link, f'{input_search}/{input_search} images/{data_id}')



        # if not removed_items.empty:
        #     for row in removed_items:
        #     last_row = gen_func.get_last_non_empty_row_excel(f"{input_search}/removed_items {input_search}.xlsx")
        #     with pd.ExcelWriter(f"{input_search}/removed_items {input_search}.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        #         removed_items.to_excel(writer, sheet_name='Sheet1', index=False, header=True, startrow= ++last_row)
        # else:
        #     print("nessun articolo è stato venduto")

        # Save the current state of the data
        # new_df.to_csv(file_path, index=False)

    #fill the database with additional data scraping every item's webpage
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
            old_df.to_csv(f"{input_search}/{input_search}.csv", index=False)

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
            #         gen_func.ensure_path_exists(f'{input_search}/{input_search} images')
            #         gen_func.download_image(img_link, f'{input_search}/{input_search} images/{data_id}')



        # if not removed_items.empty:
        #     for row in removed_items:
        #     last_row = gen_func.get_last_non_empty_row_excel(f"{input_search}/removed_items {input_search}.xlsx")
        #     with pd.ExcelWriter(f"{input_search}/removed_items {input_search}.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        #         removed_items.to_excel(writer, sheet_name='Sheet1', index=False, header=True, startrow= ++last_row)
        # else:
        #     print("nessun articolo è stato venduto")

        # Save the current state of the data
        # new_df.to_csv(file_path, index=False)

    #fill the database with additional data scraping every item's webpage
    def complete_df_with_sigle_scrapes(self, dictionary):

        csv_path = f"{dictionary['search']}/{dictionary['search']}.csv"

        images_root_folder = f"{dictionary['search']}/{dictionary['search']} images"
        
        #read csv to modify it
        df = pd.read_csv(csv_path)

        print(f"len df = {len(df)}")
        #initialize a list of new rows to add to the csv
        new_rows = []
        new_seller_rows = []

        seller_csv_path = "Sellers.csv"
        seller_df = pd.read_csv(seller_csv_path)
        

        #loop through the dataset to detect the row which are missing the info from the single product scrape
        for index, row in df.iterrows():  

            # print(f"row = {row['Images']}")
            #if images is empty means that the row doesn't have the complete info
            #also check that the folder is not created already, if it is we can skip it
            # if pd.isna(row["Images"]) and not os.path.exists(f"{dictionary['search']}/{dictionary['search']} images/{row['Dataid']}"):
            # if len(list(row["Images"])) == 0:
                # self.driver = self.init_driver()

                #get the extra data
                new_row, new_seller_row = self.scrape_single_product(str(row["Link"]), row["Dataid"])

                # if new_row:

                #     #maybe this can removed
                #     df["Images"] = df["Images"].astype("object")

                #     #fill the images cell with the list of images just scraped
                #     df.at[index, "Images"] = new_row["Images"]

                #     # Remove the images from the new_row becauase right above i populated the column "images" in the original df
                #     first_key = next(iter(new_row))
                #     new_row.pop(first_key)

                #     #download and store all the images
                #     image_folder_path = gen_func.download_all_images(df.at[index, "Images"], dictionary, new_row["Dataid"])
                    
                #     #check the images to recognize if the item is what we want
                #     is_item_right = dataset_cleaner.check_single_item_images(dictionary, image_folder_path)
                # else: #if new_row is empty means that the page doeas exist anymore
                #     is_item_right = False

                #if the item is correct we store it otherwise we drop the whole row in the csv
                new_rows.append(new_row)
                new_seller_rows.append(new_seller_row)
                # if is_item_right:
                #     new_rows.append(new_row)
                # else:
                #     df.drop(index, inplace=True)  # Drop the row in the main DataFrame
            # time.sleep(10)
        max_id = seller_df["SellerId"].max()

        columns_seller = ["SellerId", "SellerName", "Location", "ReviewsCount", "Stars"]
        temp_seller_df = pd.DataFrame(new_seller_rows, columns=columns_seller)
        temp_seller_df.drop_duplicates(subset=["SellerName"], keep='first', inplace=True)

        
        # seller_df.to_csv(seller_csv_path, index=False)

        #create a temporary df with the new rows
        columns = ["Interested_count", "View_count", "Item_description", "Upload_date", "Dataid", "SellerId", "SellerName"]
        complementary_df = pd.DataFrame(new_rows, columns=columns)

        for index, row in complementary_df.iterrows():  
            if row["SellerName"] in seller_df["SellerName"].values:
                seller_id = seller_df.loc[seller_df["SellerName"] == row["SellerName"], "SellerId"].values[0]
                complementary_df.at[index, "SellerId"] = seller_id  # Modify directly in DataFrame
                temp_seller_df.drop(temp_seller_df[temp_seller_df["SellerName"] == row["SellerName"]].index, inplace=True)
            else:
                max_id += 1
                complementary_df.at[index, "SellerId"] = max_id  # Modify directly in DataFrame
                temp_seller_df.loc[temp_seller_df["SellerName"] == row["SellerName"], "SellerId"] = max_id

        #maybe this row can be removed
        df.reset_index(drop=True, inplace=True)  # This removes the old index

        #add the temporary df with the new rows to the original df
        new_df = df.set_index('Dataid').combine_first(complementary_df.set_index('Dataid')).reset_index()
        new_df.to_csv(f"{dictionary['search']}/{dictionary['search']}.csv", index=False)
        
        
        new_seller_df = pd.concat([seller_df, temp_seller_df], ignore_index=True)
        new_seller_df.to_csv(seller_csv_path, index=False)

        # add all new images and info to items 
        # new_df = pd.merge(df, complementary_df, on="Dataid", how="left")

        #overwrite the csv with the updated data

        


