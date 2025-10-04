# Voice-Activated Image Search System via Real-Time Speech Recognition

A sophisticated image search system that allows users to search through image collections using voice commands powered by Google Cloud Speech-to-Text API and real-time speech recognition.

## 🎨 Interactive Canvas

**Visual Project Overview**: [View Interactive Canvas](https://g.co/gemini/share/e37e38328f2e) - Explore the project architecture, features, and system design through an interactive Gemini-generated webpage.

## 🚀 Features

- **Real-time Speech Recognition**: Convert spoken queries to text using Google Cloud STT
- **Image Search Engine**: Semantic search through image collections using FAISS indexing
- **Voice-Activated Interface**: Hands-free image search using natural language
- **FastAPI Backend**: RESTful API for seamless integration
- **Scalable Architecture**: Efficient vector-based image similarity search

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Platform account with Speech-to-Text API enabled
- GCP service account credentials

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/faizanHajam120/Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio.git
   cd Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/keys/<your-key>.json"
   ```

## 🚀 Quickstart

```bash
# Start the GUI application
python main_app.py

# Or run the real-time speech recognition directly
python realtimesttfinal.py
```

## 📁 Project Structure

```
├── main_app.py              # Tkinter GUI application
├── search_engine.py         # Image search functionality
├── realtimesttfinal.py      # Real-time speech recognition
├── create_index.py          # FAISS index creation
├── image_index.faiss        # Pre-built image index
├── image_map.pkl           # Image metadata mapping
└── README.md               # This file
```

## 🔧 Configuration

### Google Cloud Setup
1. Create a GCP project and enable Speech-to-Text API
2. Create a service account and download the JSON key
3. Place the key file in `$HOME/.gcp/keys/`
4. Set the environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/keys/your-key.json"
   ```

### Image Index Creation
To create a new image index:
```bash
python create_index.py
```

## 🎯 Usage

### GUI Application
The main application provides a Tkinter-based GUI interface:
- **Voice Input**: Click to start voice recognition
- **Text Search**: Type queries directly
- **Image Results**: Visual display of search results
- **Real-time Processing**: Live speech-to-text conversion

### Command Line Usage
```bash
# Run the GUI application
python main_app.py

# Run speech recognition only
python realtimesttfinal.py

# Create image index
python create_index.py
```

## 🔍 How It Works

1. **Speech Recognition**: Captures audio input and converts to text using Google Cloud STT
2. **Query Processing**: Processes the text query for semantic understanding
3. **Vector Search**: Uses FAISS to find similar images based on embeddings
4. **Results Ranking**: Returns ranked results based on similarity scores

## 🛡️ Security

- GCP credentials are stored securely outside the repository
- Sensitive files are excluded via `.gitignore`
- API endpoints can be secured with authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Speech-to-Text API
- FAISS for efficient similarity search
- FastAPI for the web framework
- The open-source community

## 🎨 Project Showcase

### Interactive Canvas
Explore the project through our interactive Gemini canvas:
- **Architecture Diagrams**: Visual system design
- **Feature Walkthrough**: Interactive feature demonstration  
- **Technology Stack**: Visual technology overview
- **User Journey**: Step-by-step user experience

[**🚀 View Interactive Canvas**](https://g.co/gemini/share/e37e38328f2e)

### Visual Documentation
- [Canvas Documentation](docs/CANVAS.md) - Detailed canvas guide
- [API Documentation](API.md) - Complete API reference
- [Project Roadmap](ROADMAP.md) - Future development plans

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for the voice-activated future**
