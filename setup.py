"""
Setup script for Voice-Activated Image Search System.
"""
from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="voice-image-search",
    version="1.0.0",
    author="faizanHajam120",
    author_email="your-email@example.com",  # Replace with your actual email
    description="A voice-activated image search system using real-time speech recognition",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/faizanHajam120/Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
        ],
        "gpu": [
            "faiss-gpu>=1.7.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "voice-image-search=main_app:ImageSearchApp",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.faiss", "*.pkl", "*.json"],
    },
    keywords="voice recognition, image search, speech-to-text, faiss, google-cloud, ai, ml",
    project_urls={
        "Bug Reports": "https://github.com/faizanHajam120/Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio/issues",
        "Source": "https://github.com/faizanHajam120/Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio",
        "Documentation": "https://github.com/faizanHajam120/Voice-Activated-Image-Search-System-via-Real-Time-Speech-Recognitio#readme",
    },
)
