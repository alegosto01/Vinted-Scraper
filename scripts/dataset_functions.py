import pandas as pd
import Scraper
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from datetime import datetime
import time
import json
import os
import ast
import shutil
import general_functions as gen_func





def fix_protezione_acquisti_in_size(value):
    if "Protezione" in str(value):
        try:
            return float(str(value).split(",")[0])
        except:
            print(value)
    elif any(word in str(value).lower() for word in ("altro", "taglia unica")):
        return 0.0
    else:
        try:
            return float(value)
        except:
            print(value)
#sometimes the prices are written like 1555 instead of 15.55. the functions adjusts them
def adjust_price_without_decimals(csv_path):
    df = pd.read_csv(csv_path)
    df_to_change = df.loc[df["Size"] == "0"].index
    print(len(df_to_change))
    def replace_float_with_int(value):
        to_remove_list = []
        try:
            value = str(value)
            return value if "." in value else value[:-2] + "." + value[-2:]
        except:
            print(f"It wasn't possible to adjust the value {value}")
            print(type(value))

    df.loc[df_to_change, "Price"] = df.loc[df_to_change, "Price"].apply(replace_float_with_int)
    df.to_csv(csv_path, index=False)
def check_item_from_csv(csv_path, chunk_size, get_images = True, check_venduto = False, get_upload_date = False):

    df_to_check = pd.read_csv(csv_path)

    if check_venduto:
        df_to_check_iter = df_to_check[df_to_check["LastCheck"].isnull()]
    elif get_images:
        df_to_check_iter = df_to_check[df_to_check["Images"] == "[]"]
        df_to_check_iter = df_to_check[df_to_check["Images"] == '"[]"']
        # df_to_check_iter = df_to_check[df_to_check["Images"].isnull()]

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


def download_images_from_csv(csv_path, destination_folder, iterations, chunk = 620):
    def safe_eval(val):                                # Convert string to a list, or return 
                                                        # an empty list if conversion fails
            try:
                return ast.literal_eval(val) if isinstance(val, str) and val.startswith("[") else val
            except (SyntaxError, ValueError):
                print("Error")
                return val

    if not os.path.exists(destination_folder):         # Create the destination folder if it doesn't exist          
        os.makedirs(destination_folder)

    df = pd.read_csv(csv_path)
    if "Downloaded" not in df.columns:                  # If is the first time create the Downloaded column
        df["Downloaded"] = False
    df["Images"] = df["Images"].apply(safe_eval)        # Convert the string in a list of images
    df.to_csv(csv_path, index=False)

    for i in range(iterations):                         # Loop through the number of iterations

        if len(df) == 0:                                # Stop the loop if the images are all downloaded
            break

        df_iter = df[df["Downloaded"] == False]         # Get only the items not downloaded
        df_iter = df_iter.iloc[:chunk]                  # Get a chunk of them

        downloaded_dataids = []                         # List to store the correctly downloaded items
      
        for index, row in df_iter.iterrows():               # Loop through the df and get the images
                                                            # checking if the row has the images links list
            dataid = int(row["Dataid"])                     # Save dataid of the item

            if row["Images"] != "" and row["Images"]:       # Save links if the cell is populated
                image_urls = row["Images"]
            else:
                image_urls = []

            downloaded_bool = True
            if len(image_urls) > 0:                         # If the row has the images start download them
                for index_img, image_url in enumerate(image_urls):      # Loop through all the images and download them in the 
                    print(f"Image {index_img + 1}: {image_url}")
                    destination_path = os.path.join(destination_folder, str(index_img))         # Final path of the image
                    success = gen_func.download_image(image_url, destination_path)              # Return true if the download was successful
                    if not success:                                                             # If download was not successfull do not add the id to downloaded_dataids
                        print(f"Problems downloading the following image = {image_url}")
                        downloaded_bool = False
                if downloaded_bool:
                    downloaded_dataids.append(int(dataid))
                else:
                    print("Not all images or none of them were downloaded")
                df.loc[df["Dataid"].isin(downloaded_dataids), "Downloaded"] = True              # Set the downloaded item as downloaded in the column "Downloaded"
        df.to_csv(csv_path, index=False)








# csv_path = "/home/ale/Desktop/Vinted-Web-Scraper/sold_items_buono.csv"
# df = pd.read_csv(csv_path)

# df["Size"] = df["Size"].apply(fix_protezione_acquisti_in_size)
# # print(len(df_filtered))

# # df = df[~df["Link"].isin(df_size_zero["Link"])]


# df.to_csv("/home/ale/Desktop/Vinted-Web-Scraper/sold_items.csv")


# df_to_check_iter = df_to_check[df_to_check["Images"].isnull()]
# provare a prendere gli ultimi link delle foto in big_csv controllando [] che sono null e "[]"

# for i in range (139):
#     start_time = time.time()  # Start timer
#     check_item_from_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv.csv", 100, get_images=True, check_venduto=False, get_upload_date=False)
#     end_time = time.time()  # End timer
#     elapsed_time = end_time - start_time  # Calculate elapsed time
#     print(elapsed_time)
#     time.sleep(60)




# directory = "/home/ale/Desktop/Vinted-Web-Scraper/sold_items_images/"

# folders = [int(name) for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

# print(folders[:5])


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


# download_images_from_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv_prova_merge.csv","/home/ale/Desktop/Vinted-Web-Scraper/big_csv_images/", iterations=1)


parent_dir = "/home/ale/Desktop/Vinted-Web-Scraper/big_csv_images/"

# List all items in the directory
for folder_name in os.listdir(parent_dir):
    folder_path = os.path.join(parent_dir, folder_name)
    
    # Check if it's a directory and ends with '.0'
    if os.path.isdir(folder_path) and folder_name.endswith(".0"):
        print(f"Deleting folder: {folder_path}")
        shutil.rmtree(folder_path)  # Delete the folder and its contents

print("✅ Deletion complete.")


# df2 = pd.read_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big csv full last check.csv")


# df1 = df1.merge(df2[["Title", "Price", "Brand", "Dataid"]], 
#                 on=["Title", "Price", "Brand"], 
#                 how="left")

# df1.to_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv_prova_merge.csv", index=False)

