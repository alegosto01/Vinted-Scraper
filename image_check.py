from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os
import cv2
import numpy as np
from scipy.stats import skew, kurtosis



# Load model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32"    )
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def check_item(true_option, wrong_option, image):

    # Load and preprocess image
    image = Image.open(image)
    inputs = processor(text=[true_option, wrong_option], images=image, return_tensors="pt", padding=True)

    # Perform image recognition
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    # print(f"Probabilities: {probs[0]}")    
    return probs[0].detach().numpy()




def calculate_blur(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found at path '{image_path}'")
        return None

    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded successfully
    if image is None:
        print(f"Error: Unable to load image from '{image_path}'")
        return None

    # Calculate the Laplacian and its variance
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    print(f"Laplacian variance: {laplacian_var}")
    return float(laplacian_var)

def calculate_images_blur_stats(folder_path):
    from pathlib import Path

    def get_file_paths(folder_path):
        """
        Get all file paths in a folder using pathlib.
        """
        return [str(file) for file in Path(folder_path).rglob('*') if file.is_file()]

    files = get_file_paths(folder_path)
    # files = [f"{image}.jpg" for image in files]
    print(files)
    lap_vars = [calculate_blur(image) for image in files]
    lap_vars = [value for value in lap_vars if value is not None]

    if not lap_vars:
        print("No valid images found.")
        return None
    

    statistics = {
        "Mean": np.mean(lap_vars),
        "Standard Deviation": np.std(lap_vars),
        "Minimum": np.min(lap_vars),
        "Maximum": np.max(lap_vars),
        "Skewness": skew(lap_vars),
        "Kurtosis": kurtosis(lap_vars)
    }

    print(statistics)
    return statistics


# calculate_images_blur_stats("/home/ale/Desktop/Vinted-Web-Scraper/air force 1 bianche/")

# for image in os.listdir("/home/ale/Desktop/Vinted-Web-Scraper/air force 1 bianche/air force 1 bianche images"):
#     file_path = os.path.join("/home/ale/Desktop/Vinted-Web-Scraper/air force 1 bianche/air force 1 bianche images/", image)

#     prob = check_item("air force 1 full white shoes", "not air force 1 full white shoes",file_path)
#     # print(prob[0])
#     if prob[0] > 0.75:
#         print(image)
#     # if prob < 0.95:
#     #     os.remove(file_path)

