from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from scipy.spatial.distance import cosine, euclidean

# Load pre-trained model tokenizer
# model_name = "bert-base-uncased"
model_name = "roberta-base"
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Functions
def get_embedding(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    # Using mean of last layer hidden states as the sentence embedding
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def calculate_centroid(embeddings):
    return np.mean(embeddings, axis=0)

# Input
# Pre-classified sentences
concrete_sentences = ["The cat sat on the mat.", "The dog barked loudly.", 
                      "She baked a cake.", "John speaks well"]
abstract_sentences = ["Freedom is the right to choose.", "Love is eternal.", 
                      "Happiness is a state of mind.", "Freedom of speech is required"]

# Getting embeddings
concrete_embeddings = [get_embedding(sentence) for sentence in concrete_sentences]
abstract_embeddings = [get_embedding(sentence) for sentence in abstract_sentences]

# Calculating average locations (centroids)
concrete_centroid = calculate_centroid(concrete_embeddings)
abstract_centroid = calculate_centroid(abstract_embeddings)


############ new items calssification


# Function to classify a new text based on closest centroid
def classify_new_text(new_text, centroids, metric="cosine"):
    # Get embedding of the new text
    new_embedding = get_embedding(new_text)

    # Calculate distances to each centroid
    distances = []
    for category, centroid in centroids.items():
        if metric == "cosine":
            distance = cosine(new_embedding, centroid)
        elif metric == "euclidean":
            distance = euclidean(new_embedding, centroid)
        else:
            raise ValueError("Unsupported metric. Use 'cosine' or 'euclidean'.")
        distances.append((category, distance))
    
    # Find the closest centroid
    closest_category = min(distances, key=lambda x: x[1])[0]
    return closest_category

# Example Centroids
centroids = {
    "Brand A": calculate_centroid(brand_a_embeddings),
    "Brand B": calculate_centroid(brand_b_embeddings),
    "Brand C": calculate_centroid(brand_c_embeddings)
}

# Classify a new text
new_text = "Stylish running shoes by Nike"
predicted_category = classify_new_text(new_text, centroids, metric="cosine")

print(f"The new text belongs to: {predicted_category}")

