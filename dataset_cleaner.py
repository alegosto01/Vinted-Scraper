import pandas as pd
import image_check as img_check
import os
import searches as search
import shutil

def remove_wrong_items(search):
    images_path =os.path.join("/", search["search"],search["search"] + " images") 
    # dataset = pd.read_excel(dataset_path)
    removed_images_path = images_path + " removed"
    for image in os.listdir(images_path):
        file_path = os.path.join(images_path, image)
        prob = img_check.check_item(search["search"], f"not {search['search']}",file_path)

        if prob[0] < 0.5:    
            print(f"prob[0] = {prob[0]} image = {image}")
            shutil.move(file_path, os.path.join(removed_images_path, image))

# def clean_dataset(df):
#     for 
    ## remove the items from the excell
    

# remove_wrong_items(search.air_force_1)

#check all the images of an item and evaluate to aproove it or not
def check_single_item_images(dictionary, images_folder_path):

    correct = []
    incorrect = []
    is_item_right = True

    for image in os.listdir(images_folder_path):
        file_path = os.path.join(images_folder_path, str(image))
        prob = img_check.check_item(dictionary["search"], f"not {dictionary['search']}",file_path)

        print(f"prob[0] = {prob[0]} image = {image}")

        if prob[0] < 0.5:    
            incorrect.append(image)
            # shutil.move(file_path, os.path.join(removed_images_path, image))
        else:
            correct.append(image)

    ratio = 0
    try:
        ratio = float(len(correct)) / float(len(incorrect))
    except ZeroDivisionError:
        pass

    if ratio != 0 and ratio < 1.3:
        is_item_right = False
        print("more incorrect than correct")
        #delete images
        #
        #
        #
        # 
    else:
        print("perfect new valid item")

    return is_item_right