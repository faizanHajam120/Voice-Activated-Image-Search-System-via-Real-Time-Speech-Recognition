# API Documentation

This document describes the programmatic interfaces available in the Voice-Activated Image Search System.

## Note

This application is primarily a GUI-based desktop application. The "API" refers to the programmatic interfaces within the Python modules, not REST endpoints.

## Python Module Interfaces

### search_engine.py

#### search_images(query, top_k=5)
Search for images using a text query.

**Parameters:**
- `query` (string, required): The search query
- `top_k` (integer, optional): Number of results to return (default: 5)

**Returns:**
```python
[
    {
        "image_path": "images/car1.jpg",
        "similarity_score": 0.95,
        "metadata": {
            "filename": "car1.jpg",
            "size": "1920x1080",
            "format": "JPEG"
        }
    }
]
```

### realtimesttfinal.py

#### MicrophoneStream
Class for handling microphone audio input.

#### listen_print_loop(responses)
Process audio responses from Google Cloud Speech-to-Text.

**Parameters:**
- `responses`: Audio response stream from Google Cloud STT

### main_app.py

#### ImageSearchApp
Main Tkinter GUI application class.

**Methods:**
- `__init__()`: Initialize the GUI
- `start_voice_recognition()`: Start voice input
- `display_search_results(results)`: Display search results

## Usage Examples

### Basic Image Search
```python
from search_engine import search_images

# Search for images
results = search_images("red car", top_k=5)
for result in results:
    print(f"Image: {result['image_path']}, Score: {result['similarity_score']}")
```

### Voice Recognition Integration
```python
from realtimesttfinal import MicrophoneStream, listen_print_loop
from search_engine import search_images

# Use voice recognition with image search
# (This is handled automatically in main_app.py)
```

### Creating Image Index
```python
# Run the index creation script
python create_index.py

# Or use programmatically
from create_index import create_image_index
create_image_index(image_directory="path/to/images")
```

## Error Handling

The application handles various error conditions:

### Common Exceptions
- `FileNotFoundError`: When image files or index files are missing
- `ImportError`: When required dependencies are not installed
- `ConnectionError`: When Google Cloud STT service is unavailable
- `AudioException`: When microphone access fails

### Example Error Handling
```python
try:
    results = search_images("red car")
except FileNotFoundError:
    print("Image index not found. Run create_index.py first.")
except Exception as e:
    print(f"Search failed: {e}")
```

## Configuration

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to GCP service account key
- `SAMPLE_RATE`: Audio sample rate (default: 16000)
- `CHUNK_SIZE`: Audio chunk size (default: 1024)

### File Paths
- `image_index.faiss`: FAISS vector index file
- `image_map.pkl`: Image metadata mapping file
- `images/`: Directory containing image files

---

For more information, see the [README.md](README.md) or [CONTRIBUTING.md](CONTRIBUTING.md).
