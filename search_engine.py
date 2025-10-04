# search_engine.py

import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import Image
import os

# --- Configuration ---
# These must match the files created by your indexing script
FAISS_INDEX_PATH = 'image_index.faiss'
IMAGE_MAP_PATH = 'image_map.pkl'
MODEL_NAME = 'clip-ViT-B-32'

# --- Load all necessary components ---
print("Loading search engine components...")

# 1. Load the FAISS index
index = faiss.read_index(FAISS_INDEX_PATH)

# 2. Load the image path map
with open(IMAGE_MAP_PATH, 'rb') as f:
    image_map = pickle.load(f)

# 3. Load the pre-trained CLIP model
# This MUST be the same model used for indexing
model = SentenceTransformer(MODEL_NAME)

print("✅ Search engine is ready.")


# --- The Core Search Function ---

def search_images(text_query, top_k=5):
    """
    Performs a semantic search for a text query against the image index.

    Args:
        text_query (str): The user's search query.
        top_k (int): The number of top results to return.

    Returns:
        list[str]: A list of file paths for the top matching images.
    """
    # 1. Encode the text query into a vector embedding.
    query_embedding = model.encode([text_query], convert_to_tensor=True)

    # 2. Convert to NumPy and normalize (same as we did for images).
    query_embedding_np = query_embedding.cpu().numpy().astype('float32')
    faiss.normalize_L2(query_embedding_np)

    # 3. Search the FAISS index for the k nearest neighbors.
    # The search function returns distances and the indices of the neighbors.
    distances, indices = index.search(query_embedding_np, top_k)

    # 4. Use the indices to look up the original image paths from our map.
    results = [image_map[i] for i in indices[0]]

    print(f"Found {len(results)} results for '{text_query}'")
    return results


# Example of how to use it:
if __name__ == '__main__':
    # This is just for testing the search engine directly.
    query = "a photo of a dog playing fetch"
    image_paths = search_images(query, top_k=3)

    print("\n--- Top 3 Results ---")
    for path in image_paths:
        print(path)
        # Optionally, display the image
        try:
            img = Image.open(path)
            img.show(title=os.path.basename(path))
        except Exception as e:
            print(f"Could not open image {path}: {e}")