# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive README with installation and usage instructions
- Docker support with Dockerfile and docker-compose.yml
- GitHub Actions CI/CD pipeline
- Contributing guidelines
- Environment configuration template
- MIT License

### Changed
- Enhanced project documentation
- Improved code organization

### Security
- Moved GCP credentials to secure location
- Added .gitignore for sensitive files

## [1.0.0] - 2024-09-30

### Added
- Initial release of Voice-Activated Image Search System
- Real-time speech recognition using Google Cloud STT
- FAISS-based image similarity search
- Tkinter GUI interface
- FastAPI backend for API access
- Support for multiple image formats
- NLP-based query processing with spaCy
- Audio streaming and processing capabilities

### Features
- Voice command processing
- Image search with semantic understanding
- Real-time audio capture and transcription
- Configurable search parameters
- Batch image indexing
- RESTful API endpoints

### Technical Details
- Python 3.8+ support
- Google Cloud Speech-to-Text integration
- FAISS vector database for efficient similarity search
- spaCy NLP for text processing
- PyAudio for audio capture
- PIL/Pillow for image processing
