# --------------------------------------------------------------------------
#               Voice-Activated Image Search - Interactive Dashboard
# --------------------------------------------------------------------------
#
# INSTRUCTIONS:
# 1. Save this code as `dashboard.py`.
# 2. Make sure you have the following files in the SAME FOLDER:
#    - image_index.faiss
#    - image_map.pkl
#    - realtimestt-473705-2f082486c0a4.json (Your Google Cloud credentials)
# 3. Run the dashboard with the command: streamlit run dashboard.py
#
# --------------------------------------------------------------------------

import streamlit as st
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import Image
import spacy
import plotly.express as px
import pandas as pd
import os
from streamlit_mic_recorder import mic_recorder
from google.cloud import speech

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Voice Image Search Dashboard",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- MODEL AND DATA LOADING ---
@st.cache_resource
def load_models_and_clients():
    """
    Loads all necessary AI models, clients, and the FAISS index.
    """
    nlp = spacy.load("en_core_web_sm")
    model = SentenceTransformer('clip-ViT-B-32')
    index = faiss.read_index('image_index.faiss')
    # Add Google Cloud Speech Client initialization
    # It will look for your credentials file.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "realtimestt-473705-2f082486c0a4.json"
    speech_client = speech.SpeechClient()
    return nlp, model, index, speech_client


@st.cache_data
def load_image_map():
    """
    Loads the mapping from index ID to image file path.
    """
    with open('image_map.pkl', 'rb') as f:
        image_map = pickle.load(f)
    return image_map


# Load all resources.
with st.spinner('Loading AI models and index... This may take a moment.'):
    nlp, model, index, speech_client = load_models_and_clients()
    image_map = load_image_map()


# --- BACKEND FUNCTIONS ---
def transcribe_audio_data(audio_bytes):
    """
    Sends audio data to Google Cloud Speech-to-Text API for transcription.
    This uses the non-streaming recognition for audio files/bytes.
    """
    try:
        audio = speech.RecognitionAudio(content=audio_bytes)
        # FINAL FIX: Explicitly set the encoding to WEBM_OPUS and the sample rate
        # to 48000 Hz, which matches the format provided by the browser component.
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            use_enhanced=True
        )
        response = speech_client.recognize(config=config, audio=audio)
        if response.results:
            return response.results[0].alternatives[0].transcript
        else:
            return None
    except Exception as e:
        st.error(f"Error with Google Speech API: {e}")
        return None


def process_query_nlp(text_query):
    """Processes the raw text query using spaCy."""
    doc = nlp(text_query.lower())
    keywords = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(keywords)


def search_images(text_query, top_k=9):
    """Performs the semantic search."""
    query_embedding = model.encode([text_query])
    faiss.normalize_L2(query_embedding)
    distances, indices = index.search(query_embedding, top_k)
    results = [image_map[i] for i in indices[0]]
    return results


# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🖼️ Voice Image Search")
    st.write("A Project by [Your Name]")

    page = st.radio(
        "Navigate",
        ("About the Project", "Interactive Demo", "Dataset Explorer", "Architecture Explained"),
        label_visibility="hidden"
    )
    st.info("This dashboard showcases the functionality of a semantic image search system built with Python and AI.")

# --- PAGE 1: ABOUT THE PROJECT ---
if page == "About the Project":
    # ... (Content remains the same as before)
    st.header("About the Project")
    st.write(
        "This project demonstrates a complete system for searching an image dataset using natural language voice commands.")
    st.subheader("Problem Statement")
    st.info(
        "Searching for images traditionally is slow. This project aims to create a more intuitive, hands-free search experience.")
    st.subheader("Technology Stack")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("**AI & Machine Learning**")
        st.markdown("- Sentence-Transformers (CLIP)\n- FAISS (Vector Search)\n- spaCy (NLP)")
    with col2:
        st.success("**Backend & Framework**")
        st.markdown("- Python 3\n- Streamlit\n- Google Cloud Speech")
    with col3:
        st.success("**Data & Visualization**")
        st.markdown("- COCO 2017 Dataset\n- Plotly Express")


# --- PAGE 2: INTERACTIVE DEMO (NOW WITH VOICE!) ---
elif page == "Interactive Demo":
    st.header("🚀 Interactive Search Demo")
    st.write(
        "Click the microphone icon to start recording your voice command. The browser will ask for microphone permission.")

    # Display the microphone recorder widget.
    audio = mic_recorder(start_prompt="Click to Speak 🎙️", stop_prompt="Stop Recording", key='recorder')

    if audio:
        # If audio has been recorded, show a spinner and process it.
        with st.spinner("Transcribing your voice..."):
            # Get the audio bytes from the recorder
            audio_bytes = audio['bytes']
            # Send to Google API for transcription
            transcript = transcribe_audio_data(audio_bytes)

        if transcript:
            st.success(f"**You said:** {transcript}")

            with st.spinner("Processing your query and searching the dataset..."):
                # Process and search using the transcribed text
                processed_query = process_query_nlp(transcript)
                st.write(f"**Processed Keywords:** `{processed_query}`")

                results = search_images(processed_query, top_k=9)

                st.subheader("Search Results")
                cols = st.columns(3)
                for i, image_path in enumerate(results):
                    if os.path.exists(image_path):
                        image = Image.open(image_path)
                        with cols[i % 3]:
                            st.image(image, caption=f"Result {i + 1}", use_column_width=True)
                    else:
                        with cols[i % 3]:
                            st.warning("Image not found")
        else:
            st.error("Could not transcribe audio. Please try speaking again.")


# --- PAGE 3: DATASET EXPLORER ---
elif page == "Dataset Explorer":
    # ... (Content remains the same as before)
    st.header("📊 Dataset Explorer: COCO 2017")
    st.write("The model was trained on the COCO (Common Objects in Context) dataset.")
    common_objects_data = {
        'Object': ['person', 'car', 'chair', 'bottle', 'cup', 'bowl', 'dining table', 'book', 'traffic light', 'boat',
                   'bird', 'cat', 'dog', 'bench', 'backpack'],
        'Frequency': [262465, 43956, 38674, 23792, 21873, 20984, 20385, 18919, 18698, 16998, 16304, 15993, 15822, 15486,
                      14282]
    }
    df = pd.DataFrame(common_objects_data)
    num_objects = st.slider("Select number of top objects to display:", 5, 15, 10)
    fig = px.bar(df.head(num_objects).sort_values(by='Frequency', ascending=True), x='Frequency', y='Object',
                 orientation='h', title=f'Top {num_objects} Most Common Objects in COCO Dataset')
    st.plotly_chart(fig, use_container_width=True)


# --- PAGE 4: ARCHITECTURE EXPLAINED ---
elif page == "Architecture Explained":
    # ... (Content remains the same as before)
    st.header("🏗️ Project Architecture")
    with st.expander("Stage 1: Voice Input & Speech-to-Text", expanded=True):
        st.markdown(
            "- **Input:** User speaks a command.\n- **Process:** Audio is recorded in the browser and sent to the **Google Cloud Speech-to-Text API**.\n- **Output:** A text transcript.")
    with st.expander("Stage 2: Natural Language Processing (NLP)"):
        st.markdown(
            "- **Input:** Raw text transcript.\n- **Process:** The text is cleaned and analyzed using **spaCy**.\n- **Output:** A clean list of meaningful keywords.")
    with st.expander("Stage 3: Semantic Search"):
        st.markdown(
            "- **Input:** Cleaned keywords.\n- **Process:** The **CLIP** model converts the query to a vector. **FAISS** finds the most similar image vectors.\n- **Output:** A list of matching image file paths.")
    with st.expander("Stage 4: GUI & User Display"):
        st.markdown(
            "- **Input:** A list of image file paths.\n- **Process:** The **Streamlit** application displays the images in a user-friendly gallery.\n- **Details:** The web architecture handles user interaction, replacing the multi-threading needed in the original Tkinter app.")

