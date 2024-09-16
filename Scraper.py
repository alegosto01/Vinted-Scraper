
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
import searches as search
import requests
import filters as f
import general_functions as gen_func
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import Product
import os


# def create_webpage(dictionary, driver):
#         input_search = str(dictionary["search"]).replace(" ","%20")
#         try:
#             # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
#             driver.get(f"https://www.vinted.it/catalog?search_text={input_search}&page=1")
#         except:
#             print(f"error")
#         time.sleep(5)
#         try:
#             cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
#             cookie.click()
#         except:
#             print("")
#         input_search = "&search_text=" + input_search

#         order = "&order=" + dictionary["sort"]
#         price_from = "&price_from=" + dictionary["prezzoDa"]
#         price_to = "&price_to=" + dictionary["prezzoA"]

#         color_list = dictionary["colore"].split("-")
#         color_ids = f.find_color_ids(color_list)
#         color_search = ""
#         for color_id in color_ids:
#             color_search = color_search + "&color_ids[]=" + color_id


#         brands_list = dictionary["brands"].split("-")
#         brands_ids = f.find_brand_ids(driver, brands_list)
#         brands_search = ""
#         for brand_id in brands_ids:
#             brands_search = brands_search + "&brand_ids[]=" + brand_id

#         status = "&status_ids[]=" + dictionary["status"]

#         webpage = f"https://www.vinted.it/catalog?currency=EUR{order}{input_search}{color_search}{price_from}{price_to}{status}{brands_search}&catalog[]=1231"
#         return webpage



def compare_and_save_df(new_df, old_df, input_search):
    # Identifying new items

    new_items = new_df[~new_df['Link'].isin(old_df['Link'])]
    removed_items = old_df[~old_df['Link'].isin(new_df['Link'])]

    print(len(removed_items))

    # Identifying removed items

    # Save new and removed items if any
    if not new_items.empty:
        new_items.to_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/new_items.xlsx", header=True, index=False)

        # notif.sendMessage(f"Nuova Ricerca: {input_search}, {len(new_items)} Nuovi Items")

        count = 0
        for index, row in new_items.iterrows():
            #send whatsapp messages
            # notif.sendMessage(f"Item {count}: {row.iloc[0]} '  ' {row.iloc[4]}")
            count += 1
            #download images
            data_id = row.iloc[6]
            gen_func.ensure_path_exists(f'/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} images')
            download_image(row.iloc[5], f'/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} images/{data_id}')
    else:
        print("non ci sono nuovi articoli")
        gen_func.empty_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/new_items {input_search}.xlsx")


    if not removed_items.empty:
        last_row = gen_func.get_last_non_empty_row_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items.xlsx")
        with pd.ExcelWriter(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items {input_search}.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            removed_items.to_excel(writer, sheet_name='Sheet1', index=False, header=True, startrow= ++last_row)
    else:
        print("nessun articolo è stato venduto")

    # Save the current state of the data
    # new_df.to_csv(file_path, index=False)
    

class Scraper:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.driver = self.init_driver()    
        self.product_root_folder = f"/home/ale/Desktop/Vinted-Web-Scraper/{self.dictionary["search"]}/"
    def init_driver(self):
        # Code to initialize Selenium WebDriver
        options = Options()
        options.add_argument("--log-level=3")  # Suppress logs by setting log level
        options.add_argument("--disable-logging")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")

        # options = uc.ChromeOptions()
        # options.add_experimental_option("detach", True)
        # options.add_experimental_option("excludeSwitches", ["enable-logging"])
        #1
        options.binary_location = "/usr/bin/google-chrome-stable"   #change to your location
        #2
        PATH = r'/home/ale/Downloads/chromedriver-linux64/chromedriver' #change also to your location
        # service = uc.chrome.service.Service(PATH)
        driver = uc.Chrome(options=options, use_subprocess=False)
        driver.implicitly_wait(5)  # Wait for elements to load
        return driver

    def create_webpage(self):
        input_search = str(self.dictionary["search"]).replace(" ","%20")
        # try:
        #     # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
        #     self.driver.get(f"https://www.vinted.it/catalog?search_text={input_search}&page=1")
        # except:
        #     print(f"error")
        # time.sleep(5)
        # try:
        #     cookie = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        #     cookie.click()
        # except:
        #     print("")
        input_search = "&search_text=" + input_search

        order = "&order=" + self.dictionary["sort"]
        price_from = "&price_from=" + self.dictionary["prezzoDa"]
        price_to = "&price_to=" + self.dictionary["prezzoA"]

        color_list = self.dictionary["colore"].split("-")
        color_ids = f.find_color_ids(color_list)
        color_search = ""
        for color_id in color_ids:
            color_search = color_search + "&color_ids[]=" + color_id


        brands_list = self.dictionary["brands"].split("-")
        brands_ids = f.find_brand_ids(self.driver, brands_list)
        brands_search = ""
        for brand_id in brands_ids:
            brands_search = brands_search + "&brand_ids[]=" + brand_id

        status = "&status_ids[]=" + self.dictionary["status"]
        category = "&catalog[]=" + search.categories[self.dictionary["category"]]

        webpage = f"https://www.vinted.it/catalog?currency=EUR{order}{input_search}{color_search}{price_from}{price_to}{status}{brands_search}{category}"    
        return webpage

    def scrape_products(self):
        input_search = self.dictionary["search"]
        
        # Create directories if they don't exist
        if not os.path.exists(self.product_root_folder):
            os.makedirs(self.product_root_folder)  

        data = []
        webpage = self.create_webpage(self.dictionary, self.driver)
        last_page = False

        for page in range(10000):
            # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
            self.driver.get(f"{webpage} + &page={page+1}")
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
                components = split_data(title)
                data_id = product.get_attribute("data-testid").split("-")

                if len(data_id) == 7:
                    data_id = data_id[3]
                else:
                    data_id = data_id[1]

                #get image's url
                img_url = self.driver.find_element(By.XPATH, f"//img[contains(@data-testid, '{data_id}--image')]")
                img_url = img_url.get_attribute("src")

            
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
                    "dataid": data_id
                })
        return data
    



    def scrape_single_product(self, url, data_id):
        self.driver.get(url)

        reviews_number_father = self.driver.find_element(By.XPATH, "//div[@class='web_ui__Rating__label']")
        
        reviews_count = int(reviews_number_father.find_element(By.XPATH, "//h4[@class='web_ui__Text__text web_ui__Text__caption web_ui__Text__left']").text)
        stars = self.driver.find_elements(By.XPATH, "//div[@class='web_ui__Rating__star web_ui__Rating__full']")

        #click on one image
        image_button = self.driver.find_element(By.XPATH, "//button[@class='item-thumbnail']")
        image_button.click()

        # self.driver.execute_script("arguments[0].click();", image_button)

        #get all the images
        # images_father = self.driver.find_elements(By.XPATH, "//div[@class='image-carousel__image-wrapper']")
        image_urls = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'image-carousel__image')]")
        print(len(image_urls))
        for index, image in enumerate(image_urls):
            image_url = image.get_attribute("src")
            print(f"Image {index + 1}: {image_url}")
            if not os.path.exists(f"{self.product_root_folder}{data_id}"):
                os.makedirs(f"{self.product_root_folder}{data_id}")
            download_image(image_url, f"{self.product_root_folder}{data_id}/{index}")

        if len(stars) >= 4 and reviews_count > 3:
            print("va bene")
        else:
            print("non va bene")
        def close(self):
            # Close the driver when done
            self.driver.quit()


   
def split_data(entry):
    # Split the entry by comma to separate title from other details
    title, details = entry.split(',', 1)

    # Extract individual components from details
#3
    price = details.split('prezzo:')[1].split('€')[0].strip() + '€'  # Extract price #you can have other value so you probalby have to change zl to value that is in your country
    brand = details.split('brand:')[1].split(',')[0].strip()  # Extract brand
    size = details.split('taglia:')[1].strip()  # Extract size
    return title.strip(), price, brand, size



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





def download_image(image_url, path):
    response = requests.get(image_url)
    with open(path, 'wb') as file:
        file.write(response.content)


# def get_images_from_products(driver, url):
#     # Locate image elements (this example uses XPATH to find all <img> tags)
#     images = driver.find_elements(By.XPATH, "//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__portrait web_ui__Image__scaled web_ui__Image__ratio']")
    

#     # Loop through the images and print the 'src' attribute (image URLs)
#     for index, image in enumerate(images):
#         image_url = image.get_attribute("src")
#         print(f"Image {index + 1}: {image_url}")