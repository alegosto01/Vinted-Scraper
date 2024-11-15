from selenium.webdriver.common.by import By
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

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection



#scraping browser proxy
AUTH = 'brd-customer-hl_c6889560-zone-scraping_browser1:wu62tqar4piy'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

# data center proxy
# SBR_WEBDRIVER = f'http://brd-customer-hl_c6889560-zone-datacenter_proxy1:9rg06kk55uec@brd.superproxy.io:22225'


#0ce4bdf2c54deb5096b627b4fba5ae18289f93c488150a496190eeb7c6aec936 # api token sivede in web_unlocker 

#b400c1d0-9386-4d0f-b2a6-84dd19356b0c # api token non si vede più

api_token = os.getenv("API_TOKEN")
proxy = "http://brd-customer-hl_c6889560-zone-web_unlocker1:@brd.superproxy.io:22225"

# Proxy URL with authentication
class Scraper:
    # def __init__(self):
        
    def init_driver(self):
        extension_path = "/home/ale/Desktop/Vinted-Web-Scraper/proxy_auth_extension/proxy_auth_extension.zip"

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
                print('Connected! Navigating to https://www.vinted.it...')
                driver.get('https://www.vinted.it')
                print("fatto")
                return driver
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(15)  # Wait before retrying
        print("Failed to load the page after multiple attempts.")
    
    def get_page_content(self, url):
        # url = "https://www.vinted.it/catalog?search_text=air%20force%20men&time=1731608194"

        success = False
        attempts = 0
        
        while success == False and attempts < 5:
            session = HTMLSession()

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
            response = session.post(url, json=payload, headers=headers)


            if response.status_code == 200:
                # Parse the HTML content from the response
                html = response.html
                # Optionally render JavaScript if the content is dynamically loaded
                html.render(sleep=1)  # Adjust sleep if needed to allow content to load   
                if html:
                    success = True    
                    return html
            else:
                print("Failed to retrieve the page:", response.status_code)
                print("Response message:", response.text)
            
    # create the url setting all the filters of the search
    def create_webpage(self, dictionary): 

        self.driver = self.init_driver(self)

        #setting the input search
        input_search = str(dictionary["search"]).replace(" ","%20")
        input_search = "&search_text=" + input_search
        print("creo pagine")

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
        # webpage = "https://www.vinted.it/catalog?search_text=adidas%20gazelle%20black%20and%20white&status_ids[]=1&color_ids[]=12&currency=EUR"
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
            
            webpage = webpage + str(page+1)

            html_content = self.get_page_content(webpage)
                        
            time.sleep(5)

            # #if is the first access accept the cookies
            # try:
            #     cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            #     cookie.click()
            # except:
            #     pass


            #if the previous page was empty then stop
            if last_page:
                print(f"finished at page {page+1}")
                break
            else:
                print(f"im at page {page+1}")

                    #find list of products in the page
            products = html_content.find('.new-item-box__overlay')


            all_likes_counts = html_content.find('.u-background-white.u-flexbox.u-align-items-center.new-item-box__favourite-icon')

            #if the page has 0 products mean that we can stop scraping
            if len(products) == 0:
                last_page = True

            data = []
            #get all the data from the products
            for product in products:

                #get link, dataid, and components (which contains tile, price, size and brand)
                title = gen_func.remove_illegal_characters(product.attrs.get("title"))
                components = gen_func.split_data(title)
                link = product.attrs.get("href")
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
                            likes_count = aria_label.split("Aggiunto ai preferiti da ")[1][0] # Adjust based on actual aria-label structure
                            break  # Stop once the correct element is found


                # Append the data to the list
                data.append({
                    "Title": components[0],
                    "Price": float(re.sub(r'[^\d.]', '', components[1].replace(',', '.'))), #remove non digits caracters and cast it to float
                    "Brand": components[2],
                    "Size": components[3],
                    "Link": link,
                    "Likes": likes_count,
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
        self.driver = self.init_driver()

        # html_content = self.get_page_content(url)
        # page_exists = True

        #check if the page still exists
        try:
            # Try to find the "page doesn't exist" indicator element

            # page_doesnt_exist = html_content.find("img[src='https://marketplace-web-assets.vinted.com/assets/error-page/404-rack.svg']")
            page_doesnt_exist = self.driver.find_element(By.XPATH, "//img[@src='https://marketplace-web-assets.vinted.com/assets/error-page/404-rack.svg']")
            print("Page does not exist.")  # This will execute if the element is found
            page_exists = False
        except NoSuchElementException:
            pass

        #f the page exists then get all the data, else remove the row from the df (for now)
        if page_exists:
            time.sleep(1)
            
            #get reviews count and star rating
            # reviews_number_father = html_content.find("div[class='web_ui__Rating__label']")
            reviews_number_father = self.driver.find_element(By.XPATH, "//div[@class='web_ui__Rating__label']")
            reviews_count = 0
            try:
                # reviews_count = html_content.find("h4[class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left']")
                reviews_count = int(reviews_number_father.find_element(By.XPATH, "//h4[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left']").text)
            except:
                pass

            # stars = html_content.find("div[class='web_ui__Rating__star web_ui__Rating__full']")
            stars = self.driver.find_elements(By.XPATH, "//div[@class='web_ui__Rating__star web_ui__Rating__full']")

            #get location
            # location_element = html_content.find("div.details-list__item-value[itemprop='location']", first=True)
            # location = location_element.text if location_element else None            
            location = self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='location']").text

            #get views
            # views_count_element = html_content.find("div.details-list__item-value[itemprop='view_count']", first=True)
            # views_count = location_element.text if location_element else None  
            views_count = int(self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='view_count']").text)

            #get interested people
            interested_count = 0
            try:
                # interested_count_element = html_content.find("div.details-list__item-value[itemprop='interested']", first=True)
                # interested_count = location_element.text.split(" ")[0] if location_element else None  
                interested_count = int(self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='interested']").text.split(" ")[0])
            except:
                pass


            #get upload date
            upload_date = " ".join(
                # html_content.find("div.details-list__item-value[itemprop='interested']", first=True).text.split()[:-1]
                self.driver.find_element(By.XPATH, "//div[@class='details-list__item-value' and @itemprop='upload_date']").text.split()[:-1]
                )
            
            #get item description
            # item_description = html_content.find("span[class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']")
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

        



