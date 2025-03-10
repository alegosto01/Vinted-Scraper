import pandas as pd
import Scraper
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from datetime import datetime
import time
import json
import os
import ast

import general_functions as gen_func
def check_item_from_csv(csv_path, chunk_size, get_images = True, check_venduto = False, get_upload_date = False):

    df_to_check = pd.read_csv(csv_path)

    if check_venduto:
        df_to_check_iter = df_to_check[df_to_check["LastCheck"].isnull()]
    elif get_images:
        # df_to_check_iter = df_to_check[df_to_check["Images"] == "[]"]
        df_to_check_iter = df_to_check[df_to_check["Images"].isnull()]

    print(f"len = {len(df_to_check_iter)}")

    # df_to_check_iter = df_to_check[:chunk_size]
    sold_items = []
    checked_items = []
    scraper = Scraper.Scraper()
    max_workers = min(8, multiprocessing.cpu_count())

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, (_, row) in enumerate(df_to_check_iter.iterrows()):
            # print(f"row = {row}")
            if i >= chunk_size:  # Stop after X iterations
                break
            futures.append(executor.submit(scraper.fetch_page_and_check, row, True))


        for future in as_completed(futures):
            item, sold, status = future.result()
            if get_images:
                df_to_check.loc[item.name, "Images"] = json.dumps(item["Images"])
                # print(item)
            # if get_upload_date:
            #     df_to_check.loc[item.name, "Upload_date"] = json.dumps(item["Upload_date"])

            if check_venduto:
                if sold:
                    sold_items.append(item)
                    print(f"Item sold for real: {item['Title']} + {item['Link']}")
                else:
                    print(f"Item not sold: {item['Title']}")
                    checked_items.append(item)
        # print(sold_items)

    if check_venduto:
        columns = ["Images","Upload_date","Dataid","Title","Price","Brand","Size","Link","Likes","MarketStatus","SearchDate","Page","SearchCount","LastCheck"]
        new_sold_items_df = pd.DataFrame(sold_items, columns=columns)
        new_sold_items_df["LastCheck"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        empty_rows = df_to_check[df_to_check["LastCheck"].isnull()].index[:chunk_size]  # Get first 100 empty rows
        df_to_check.loc[empty_rows, "LastCheck"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Update the values


        old_sold_items_df = pd.read_csv("/home/ale/Desktop/Vinted-Web-Scraper/sold_items.csv")
        final_sold_items_df = pd.concat([new_sold_items_df, old_sold_items_df], ignore_index=True)
        final_sold_items_df.to_csv(f"/home/ale/Desktop/Vinted-Web-Scraper/sold_items.csv", index=False)

    if get_images:
        df_to_check.to_csv(csv_path, index=False)


######SISTEMA GIU download_images_from_csv ########

def download_images_from_csv(csv_path, root_folder, iterations, chunk = 400):
    for i in range(iterations):
        df = pd.read_csv(csv_path)
        df = df.loc[df["Downloaded"] != "Yes"]

        if len(df) == 0:
            break

        df_iter = df.iloc[:chunk]
        print(len(df_iter))
        # df_iter = df_iter.iloc[:50]
        downloaded_dataids = []
        df_iter['Images'] = df_iter['Images'].apply(ast.literal_eval)

        for index, row in df_iter.iterrows():
            print(f"{row['Dataid']}")
            if row["Images"] != "" and row["Images"]:
                image_urls = row["Images"]
            else:
                break
            image_folder_path = os.path.join(root_folder,str(row["Dataid"]))
            if not os.path.exists(image_folder_path):
                os.makedirs(image_folder_path)
            for index_img, image_url in enumerate(image_urls):
            # image_url = image.get_attribute("src")
                print(f"Image {index_img + 1}: {image_url}")
                # print("path exists i wont created it")
                gen_func.download_image(image_url,os.path.join(image_folder_path, str(index_img)))
            downloaded_dataids.append(int(row["Dataid"]))
            
        #set the downloaded images to yes so thta i don't download them anymore
        df.loc[df["Dataid"].isin(downloaded_dataids), "Downloaded"] = "Yes"
        df.to_csv(csv_path, index=False)


# provare a prendere gli ultimi link delle foto in big_csv controllando [] che sono null e "[]"

# for i in range (1):
#     start_time = time.time()  # Start timer
#     check_item_from_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv.csv", 100, get_images=True, check_venduto=False, get_upload_date=False)
#     end_time = time.time()  # End timer
#     elapsed_time = end_time - start_time  # Calculate elapsed time
#     print(elapsed_time)
#     time.sleep(60)




# directory = "/home/ale/Desktop/Vinted-Web-Scraper/sold_items_images/"

# folders = [int(name) for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

# print(folders[:5])

# df = pd.read_csv("/home/ale/Desktop/Vinted-Web-Scraper/sold_items_copy_28_02_2025.csv")

# print(len(df))

# df = df.drop_duplicates(subset="Dataid")

# print(len(df))

# df["Dataid"] = df["Dataid"].astype(int)

# df.loc[df["Dataid"].isin(folders), "Downloaded"] = "Yes"

# yes_list = df["Dataid"]

# dif_list = [id for id in yes_list if id not in folders]

# print(len(dif_list))

# print(dif_list[:5])

# # df.to_csv("/home/ale/Desktop/Vinted-Web-Scraper/sold_items.csv", index=False)

# print(f"len folders {len(folders)}")


download_images_from_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv.csv","/home/ale/Desktop/Vinted-Web-Scraper/big_csv_images/", iterations=100)




