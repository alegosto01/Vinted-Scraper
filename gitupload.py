# import asyncio
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import re
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pyautogui
# import pandas as pd
# from selenium.webdriver.common.action_chains import ActionChains
# import schedule
# import time
# import filters as f
# import searches as search
# import notifications as notif




# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# #1
# options.binary_location = "/usr/bin/google-chrome-stable"   #change to your location 
# #2
# PATH = r'/home/ale/Downloads/chromedriver-linux64/chromedriver' #change also to your location
# service = webdriver.chrome.service.Service(PATH)
# driver = webdriver.Chrome(service=service, options=options)
# from whatsapp_api_client_python import API


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


# def create_webpage(dictionary):
#     input_search = str(dictionary["search"]).replace(" ","%20")
#     try:
#         # https://www.vinted.it/catalog?currency=EUR&order=price_low_to_high&search_text=air%20force%201%20white&color_ids[]=12=35&price_to=100&status_ids[]=1&brand_ids[]=53&brand_ids[]=5977&brand_ids[]=110434&page=3
#         driver.get(f"https://www.vinted.it/catalog?search_text={input_search}&page=1")
#     except:
#         print(f"error")
#     time.sleep(5)
#     try:
#         cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
#         cookie.click()
#     except:
#         print("")
#     input_search = "&search_text=" + input_search

#     order = "&order=" + dictionary["sort"]  
#     price_from = "&price_from=" + dictionary["prezzoDa"]
#     price_to = "&price_to=" + dictionary["prezzoA"]

#     color_list = dictionary["colore"].split("-")
#     color_ids = f.find_color_ids(color_list)
#     color_search = ""
#     for color_id in color_ids:
#         color_search = color_search + "&color_ids[]=" + color_id
    

#     brands_list = dictionary["brands"].split("-")
#     brands_ids = f.find_brand_ids(driver, brands_list)
#     brands_search = ""
#     for brand_id in brands_ids:
#         brands_search = brands_search + "&brand_ids[]=" + brand_id
    
#     status = "&status_ids[]=" + dictionary["status"]

#     webpage = f"https://www.vinted.it/catalog?currency=EUR{order}{input_search}{color_search}{price_from}{price_to}{status}{brands_search}"
#     return webpage

# def split_data(entry):
#     # Split the entry by comma to separate title from other details
#     title, details = entry.split(',', 1)

#     # Extract individual components from details
# #3
#     price = details.split('prezzo:')[1].split('€')[0].strip() + '€'  # Extract price #you can have other value so you probalby have to change zl to value that is in your country
#     brand = details.split('brand:')[1].split(',')[0].strip()  # Extract brand
#     size = details.split('taglia:')[1].strip()  # Extract size
#     return title.strip(), price, brand, size
# data = []

# #x =input("Search text : ")
# #x.replace(" ","%20")
# #p1=int(input("Number of pages :"))

# count = 0
# def make_search(dictionary, driver):
#     print(++count)
#     input_search = dictionary["search"]
#     input_search.replace(" ","%20")
#     webpage = create_webpage(dictionary)
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
#             # print(f"finished at page {page+1}")
#             break
#         else:
#             print(f"im at page {page+1}") 


#         # translate_specs(dictionary, driver)
#         # time.sleep(4)
#         number_results_panel = div_element = driver.find_element(By.CSS_SELECTOR, "div.u-ui-padding-vertical-medium.u-flexbox.u-justify-content-between.u-align-items-center")
#         total_results = number_results_panel.find_element(By.TAG_NAME, "span").text.split(" ")[0].replace("+","")

#         products = driver.find_elements(By.CLASS_NAME, "new-item-box__overlay")

#         if len(products) == 0:
#             last_page = True

#         for product in products:
#             title = product.get_attribute("title")
#             link = product.get_attribute("href")
#             components = split_data(title)
        
#             # Append the data to the list
#             data.append({
#                 "Title": components[0],
#                 "Price": components[1],
#                 "Brand": components[2],
#                 "Size": components[3],
#                 "Link": link
#             })
#     # Convert the list of dictionaries to a DataFrame
#     df = pd.DataFrame(data)

#     old_df = pd.read_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search}.xlsx")

#     if old_df.empty:
#         old_df = df.copy()

#     compare_and_save(df,old_df,input_search)

#     # Save the DataFrame to an Excel file
# #4
#     excel_filename = f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search}.xlsx" #zmiana lokacji zapisu pliku

#     df.to_excel(excel_filename, index=False)

#     print("Data exported to:", excel_filename)

#     with open(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/{input_search} search filters.txt", 'w') as file:
#     # Convert dictionary to string and write to file
#         file.write(str(dictionary))




# def compare_and_save(new_df, old_df, input_search):
#     # Identifying new items

#     new_items = new_df[~new_df['Link'].isin(old_df['Link'])]
#     removed_items = old_df[~old_df['Link'].isin(new_df['Link'])]
    
#     # Identifying removed items



#     # Save new and removed items if any
#     if not new_items.empty:
#         new_items.to_excel(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/new_items.xlsx", header=False, index=False)
        
#         notif.sendMessage(f"Nuova Ricerca: {input_search}, {len(new_items)} Nuovi Items")
#         count = 0
#         for index, row in new_items.iterrows():
#             notif.sendMessage(f"Item {++count}: {row[0]} '  ' {row[4]}")
#     if not removed_items.empty:
#         with pd.ExcelWriter(f"/home/ale/Desktop/Vinted-Web-Scraper/{input_search}/removed_items.xlsx", engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
#             removed_items.to_excel(writer, sheet_name='Sheet1', index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    

#     # Save the current state of the data
#     # new_df.to_csv(file_path, index=False)

# make_search(search.air_force_1, driver)




# # while True:
# #     make_search(search.air_force_1, driver)
# #     time.sleep(1800)



# # schedule.every(30).minutes.do(lambda: )  

# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)  # Wait for a second before checking the schedule again


