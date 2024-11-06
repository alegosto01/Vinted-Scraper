from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import os


# Load model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
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


# for image in os.listdir("/home/ale/Desktop/Vinted-Web-Scraper/air force 1 bianche/air force 1 bianche images"):
#     file_path = os.path.join("/home/ale/Desktop/Vinted-Web-Scraper/air force 1 bianche/air force 1 bianche images/", image)

#     prob = check_item("air force 1 full white shoes", "not air force 1 full white shoes",file_path)
#     # print(prob[0])
#     if prob[0] > 0.75:
#         print(image)
#     # if prob < 0.95:
#     #     os.remove(file_path)

