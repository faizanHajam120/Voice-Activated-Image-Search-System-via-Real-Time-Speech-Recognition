# API Documentation

This document describes the API endpoints available in the Voice-Activated Image Search System.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API keys or OAuth.

## Endpoints

### Health Check

#### GET /
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Voice-Activated Image Search API is running",
  "version": "1.0.0"
}
```

### Search Images

#### POST /search
Search for images using a text query.

**Request Body:**
```json
{
  "query": "red car",
  "top_k": 9
}
```

**Parameters:**
- `query` (string, required): The search query
- `top_k` (integer, optional): Number of results to return (default: 9)

**Response:**
```json
{
  "query": "red car",
  "results": [
    {
      "image_path": "images/car1.jpg",
      "similarity_score": 0.95,
      "metadata": {
        "filename": "car1.jpg",
        "size": "1920x1080",
        "format": "JPEG"
      }
    }
  ],
  "total_results": 1,
  "search_time": 0.123
}
```

### Voice Search

#### POST /voice-search
Search for images using voice input.

**Request Body:**
```json
{
  "audio_data": "base64_encoded_audio",
  "language": "en-US",
  "top_k": 9
}
```

**Parameters:**
- `audio_data` (string, required): Base64 encoded audio data
- `language` (string, optional): Language code (default: "en-US")
- `top_k` (integer, optional): Number of results to return (default: 9)

**Response:**
```json
{
  "transcript": "red car",
  "confidence": 0.95,
  "query": "red car",
  "results": [
    {
      "image_path": "images/car1.jpg",
      "similarity_score": 0.95,
      "metadata": {
        "filename": "car1.jpg",
        "size": "1920x1080",
        "format": "JPEG"
      }
    }
  ],
  "total_results": 1,
  "search_time": 0.456
}
```

### Upload Images

#### POST /upload
Upload images to the search index.

**Request Body:**
```
multipart/form-data
```

**Parameters:**
- `images` (file[], required): Image files to upload
- `rebuild_index` (boolean, optional): Whether to rebuild the search index (default: false)

**Response:**
```json
{
  "uploaded_count": 5,
  "failed_count": 0,
  "message": "Images uploaded successfully",
  "index_rebuilt": false
}
```

### Get Image Metadata

#### GET /images/{image_id}
Get metadata for a specific image.

**Parameters:**
- `image_id` (string, required): The image identifier

**Response:**
```json
{
  "image_id": "img_123",
  "filename": "car1.jpg",
  "path": "images/car1.jpg",
  "size": "1920x1080",
  "format": "JPEG",
  "file_size": 245760,
  "upload_date": "2024-10-05T10:30:00Z",
  "tags": ["car", "red", "vehicle"]
}
```

### Search Statistics

#### GET /stats
Get search statistics and system information.

**Response:**
```json
{
  "total_images": 1000,
  "total_searches": 5000,
  "average_search_time": 0.123,
  "popular_queries": [
    "car",
    "dog",
    "landscape"
  ],
  "system_info": {
    "version": "1.0.0",
    "uptime": "2 days, 5 hours",
    "memory_usage": "512MB"
  }
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "details": "The 'query' parameter is required"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found",
  "details": "Image with ID 'img_123' not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "details": "Database connection failed"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. In production, consider implementing:
- 100 requests per minute per IP
- 1000 requests per hour per API key

## SDK Examples

### Python
```python
import requests

# Search for images
response = requests.post("http://localhost:8000/search", 
                        json={"query": "red car", "top_k": 5})
results = response.json()

# Voice search
with open("audio.wav", "rb") as f:
    audio_data = f.read()
    
response = requests.post("http://localhost:8000/voice-search",
                        json={"audio_data": audio_data.encode("base64")})
results = response.json()
```

### JavaScript
```javascript
// Search for images
const response = await fetch('http://localhost:8000/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'red car',
    top_k: 5
  })
});

const results = await response.json();

// Voice search
const audioFile = document.getElementById('audioFile').files[0];
const audioData = await audioFile.arrayBuffer();
const base64Audio = btoa(String.fromCharCode(...new Uint8Array(audioData)));

const voiceResponse = await fetch('http://localhost:8000/voice-search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    audio_data: base64Audio,
    language: 'en-US'
  })
});

const voiceResults = await voiceResponse.json();
```

### cURL
```bash
# Search for images
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "red car", "top_k": 5}'

# Voice search
curl -X POST "http://localhost:8000/voice-search" \
  -H "Content-Type: application/json" \
  -d '{"audio_data": "base64_encoded_audio", "language": "en-US"}'
```

## WebSocket Support (Future)

Planned WebSocket endpoints for real-time features:

### /ws/search
Real-time search updates and live results.

### /ws/voice
Real-time voice recognition and streaming.

## Changelog

### Version 1.0.0
- Initial API release
- Basic search functionality
- Voice search support
- Image upload capabilities

---

For more information, see the [README.md](README.md) or [CONTRIBUTING.md](CONTRIBUTING.md).
