import pandas as pd
import Scraper
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from datetime import datetime
import time
import json

def check_if_item_got_sold(csv_path, chunk_size, get_images = False):

    df_to_check = pd.read_csv(csv_path)

    df_to_check_iter = df_to_check[df_to_check["LastCheck"].isnull()]

    # df_to_check_iter = df_to_check[:chunk_size]

    print(len(f"len df {df_to_check}"))
    sold_items = []
    checked_items = []
    scraper = Scraper.Scraper()
    max_workers = min(8, multiprocessing.cpu_count())
    counter = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, (_, row) in enumerate(df_to_check_iter.iterrows()):
            if i >= chunk_size:  # Stop after X iterations
                break
            futures.append(executor.submit(scraper.fetch_page_and_check, row, True))


        for future in as_completed(futures):
            # counter += 1
            item, sold, status = future.result()
            if get_images:
                df_to_check.loc[item.name, "Images"] = json.dumps(item["Images"])

            if sold:
                sold_items.append(item)
                print(f"Item sold for real: {item['Title']} + {item['Link']}")
            else:
                print(f"Item not sold: {item['Title']}")
                checked_items.append(item)
            # if counter == chunk_size:
            #     break
    # print(sold_items)
    columns = ["Images","Upload_date","Dataid","Title","Price","Brand","Size","Link","Likes","MarketStatus","SearchDate","Page","SearchCount"]
    new_sold_items_df = pd.DataFrame(sold_items, columns=columns)

    old_sold_items_df = pd.read_csv("/home/ale/Desktop/Vinted-Web-Scraper/sold_items.csv")
    final_sold_items_df = pd.concat([new_sold_items_df, old_sold_items_df], ignore_index=True)
    final_sold_items_df.to_csv(f"/home/ale/Desktop/Vinted-Web-Scraper/sold_items.csv", index=False)

    
    empty_rows = df_to_check[df_to_check["LastCheck"].isnull()].index[:chunk_size]  # Get first 100 empty rows
    df_to_check.loc[empty_rows, "LastCheck"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Update the values

    df_to_check.to_csv("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv.csv", index=False)

    # print("Parallel scraping complete.")


for i in range (10):
    start_time = time.time()  # Start timer
    check_if_item_got_sold("/home/ale/Desktop/Vinted-Web-Scraper/big_csv/big_csv.csv", 1000, get_images=True)
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(elapsed_time)
    time.sleep(60)