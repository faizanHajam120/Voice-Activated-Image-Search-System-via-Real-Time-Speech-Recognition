# create_index.py

import os
import pickle
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm
import kagglehub

# --- Configuration ---
print("Downloading COCO 2017 dataset from Kaggle Hub...")
# This will download the dataset to a local cache on your Mac.
# If it's already downloaded, this step will be very fast.
try:
    dataset_path = kagglehub.dataset_download("awsaf49/coco-2017-dataset")
    print(f"Dataset located at: {dataset_path}")
except Exception as e:
    print(f"Error downloading dataset: {e}")
    print("Please ensure you have authenticated with Kaggle. In your terminal, you can set up your credentials.")
    exit()

# The specific folder within the dataset we want to index.
IMAGE_DIR = os.path.join(dataset_path, 'coco2017', 'val2017')
MODEL_NAME = 'clip-ViT-B-32'
FAISS_INDEX_PATH = 'image_index.faiss'
IMAGE_MAP_PATH = 'image_map.pkl'

# --- Main Indexing Logic ---

def create_index():
    """
    Processes all images, generates embeddings using a CLIP model,
    and stores them in a FAISS index for efficient similarity searching.
    """
    print("Starting the image indexing process...")

    # 1. Load the pre-trained model.
    print(f"Loading the '{MODEL_NAME}' model...")
    model = SentenceTransformer(MODEL_NAME)

    # 2. Find all valid image files.
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    try:
        image_paths = [
            os.path.join(IMAGE_DIR, fname)
            for fname in os.listdir(IMAGE_DIR)
            if os.path.splitext(fname)[1].lower() in valid_extensions
        ]
    except FileNotFoundError:
        print(f"Error: Could not find the image directory: {IMAGE_DIR}")
        print("Please check that the dataset downloaded correctly and the path is correct.")
        return

    if not image_paths:
        print(f"Error: No images found in '{IMAGE_DIR}'.")
        return

    print(f"Found {len(image_paths)} images to index.")

    # 3. Generate embeddings for all images.
    print("Generating image embeddings... (This will take a few minutes)")
    image_embeddings = model.encode(
        [Image.open(filepath) for filepath in image_paths],
        batch_size=32,
        convert_to_tensor=True,
        show_progress_bar=True
    )
    image_embeddings_np = image_embeddings.cpu().numpy().astype('float32')
    faiss.normalize_L2(image_embeddings_np)
    print("Embeddings generated.")

    # 4. Create and build the FAISS index.
    embedding_dim = image_embeddings_np.shape[1]
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(image_embeddings_np)
    print(f"FAISS index created with {index.ntotal} vectors.")

    # 5. Save the index and the image path map.
    print(f"Saving FAISS index to '{FAISS_INDEX_PATH}'...")
    faiss.write_index(index, FAISS_INDEX_PATH)

    image_map = {i: path for i, path in enumerate(image_paths)}
    with open(IMAGE_MAP_PATH, 'wb') as f:
        pickle.dump(image_map, f)

    print(f"Image path map saved to '{IMAGE_MAP_PATH}'.")
    print("\n--- Indexing complete! ---")
    print("You can now run the main_app.py file.")


if __name__ == '__main__':
    create_index()