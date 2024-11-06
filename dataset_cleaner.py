import pandas as pd
import image_check as img_check
import os
import searches as search
import shutil

def remove_wrong_items(search):
    images_path =os.path.join("/home/ale/Desktop/Vinted-Web-Scraper/", search["search"],search["search"] + " images") 
    # dataset = pd.read_excel(dataset_path)
    removed_images_path = images_path + " removed"
    for image in os.listdir(images_path):
        file_path = os.path.join(images_path, image)
        prob = img_check.check_item(search["search"], f"not {search['search']}",file_path)

        if prob[0] < 0.5:    
            print(f"prob[0] = {prob[0]} image = {image}")
            shutil.move(file_path, os.path.join(removed_images_path, image))


    ## remove the items from the excell
    

remove_wrong_items(search.air_force_1)
