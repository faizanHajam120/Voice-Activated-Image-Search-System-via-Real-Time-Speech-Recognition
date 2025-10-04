# main_app.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import queue
import spacy

# --- IMPORT YOUR EXISTING MODULES ---
# These are your completed .py files that act as tools for this main app.
from realtimesttfinal import MicrophoneStream, listen_print_loop, SAMPLE_RATE, CHUNK_SIZE
from search_engine import search_images

# These are for the voice recognition part
from google.oauth2 import service_account
from google.cloud import speech

# --- GLOBAL SETUP ---
# Load the NLP model once at the start.
print("Loading NLP model...")
nlp = spacy.load("en_core_web_sm")
print("NLP model loaded.")

# A queue is a safe way to pass messages from the background voice thread to the main GUI thread.
gui_queue = queue.Queue()


# --- BACKGROUND LOGIC ---
# This section defines the work that happens behind the scenes.

def process_voice_command(transcript):
    """
    This is the "brain" that connects voice to search. It runs in the background.
    """
    doc = nlp(transcript.lower())
    keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

    if not keywords:
        gui_queue.put(("status", "Could not find keywords. Please try again."))
        return

    search_query = " ".join(keywords)
    # Send a status update to the GUI
    gui_queue.put(("status", f"Searching for: '{search_query}'..."))

    # Perform the search
    found_images = search_images(search_query, top_k=9)

    # Send the results and a final status update back to the GUI
    gui_queue.put(("results", found_images))
    gui_queue.put(("status", "Ready. Speak your next command."))


def voice_recognition_thread():
    """
    This function runs the entire Google Speech-to-Text loop in a background thread
    so that the GUI does not freeze while listening.
    """
    # Define audio parameters directly inside the thread
    SAMPLE_RATE = 16000
    CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
    language_code = "en-US"
    try:
        credentials_path = "realtimestt-473705-2f082486c0a4.json"  # Make sure this filename is correct
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = speech.SpeechClient(credentials=credentials)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Use the constant, not a string
            sample_rate_hertz=SAMPLE_RATE,
            language_code=language_code
        )

        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

        with MicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
            responses = client.streaming_recognize(streaming_config, requests)
            # This loop will now send its results to our new process_voice_command function
            listen_print_loop(responses, process_voice_command)
    except Exception as e:
        print(f"FATAL ERROR in voice thread: {e}")
        gui_queue.put(("status", f"VOICE ERROR: {e}"))


# --- GUI APPLICATION ---
# This section defines the user interface.

class ImageSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voice-Activated Image Search")
        self.geometry("800x600")

        # A label at the top to show the current status
        self.status_label = ttk.Label(self, text="Initializing...", font=("Helvetica", 14), anchor="center")
        self.status_label.pack(pady=10)

        # A frame that will contain the grid of images
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.image_labels = []

        # Start a recurring check of the message queue
        self.process_queue()

    def process_queue(self):
        """Checks the queue for messages from the background thread and updates the GUI."""
        try:
            message_type, data = gui_queue.get(block=False)
            if message_type == "status":
                self.status_label.config(text=data)
            elif message_type == "results":
                self.display_images(data)
        except queue.Empty:
            # If the queue is empty, do nothing
            pass
        finally:
            # Schedule this function to run again after 100ms
            self.after(100, self.process_queue)

    def display_images(self, image_paths):
        """Clears the old images and displays the new ones found from the search."""
        # Clear any previous images
        for label in self.image_labels:
            label.destroy()
        self.image_labels.clear()

        # Display the new set of images in a 3-column grid
        for i, path in enumerate(image_paths):
            try:
                img = Image.open(path)
                img.thumbnail((150, 150))  # Create a thumbnail
                photo = ImageTk.PhotoImage(img)

                label = ttk.Label(self.results_frame, image=photo, padding=5)
                label.image = photo  # Important: Keep a reference to avoid garbage collection!

                row, col = divmod(i, 3)  # Arrange in a grid
                label.grid(row=row, column=col, padx=5, pady=5)
                self.image_labels.append(label)
            except Exception as e:
                print(f"Error displaying image {path}: {e}")


# --- APPLICATION LAUNCH ---
if __name__ == '__main__':
    # 1. Create the main application window
    app = ImageSearchApp()

    # 2. Create and start the background thread for voice recognition
    voice_thread = threading.Thread(target=voice_recognition_thread, daemon=True)
    voice_thread.start()

    # 3. Start the GUI event loop (this makes the window appear and become interactive)
    app.mainloop()