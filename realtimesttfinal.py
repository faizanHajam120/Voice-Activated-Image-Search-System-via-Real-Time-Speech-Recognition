import queue
import re
import sys
import threading
# Add this new import for the credentials
from google.oauth2 import service_account

import numpy as np
import sounddevice as sd
from google.cloud import speech
import spacy
from search_engine import search_images

# Load the spaCy model once when the script starts.
print("Loading NLP model...")
nlp = spacy.load("en_core_web_sm")
print("NLP model loaded.")

# Audio recording parameters
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms


class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = sd.InputStream(
            samplerate=self._rate,
            channels=1,
            dtype=np.int16,
            blocksize=self._chunk,
            callback=self._fill_buffer,
        )
        self._audio_interface.start()
        self.closed = False
        print("🎙️  Microphone stream opened. Start speaking!")
        return self

    def __exit__(self, type, value, traceback):
        self._audio_interface.stop()
        self._audio_interface.close()
        self.closed = True
        self._buff.put(None)
        print("🎤 Microphone stream closed.")

    def _fill_buffer(self, indata, frames, time, status):
        """Continuously collect data from the audio stream into the buffer."""
        if status:
            print(status, file=sys.stderr)
        self.put(indata.tobytes())

    def put(self, data):
        """Adds data to the buffer."""
        self._buff.put(data)

    def generator(self):
        """A generator function that yields audio chunks from the buffer."""
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)



def listen_print_loop(responses, callback):  # <-- MODIFIED: Add a callback parameter
    """
    Iterates through server responses, prints them, and calls a callback
    on the final transcript.
    """
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            # Display the final transcript and clean up the line.
            sys.stdout.write(f"\r{transcript}\n")

            # --- NEW PART ---
            # Instead of just printing, send the final transcript to our processor
            callback(transcript)
            # ----------------
        else:
            # Display the partial transcript
            sys.stdout.write(f"\r{transcript}" + " " * 20)
            sys.stdout.flush()


# --- NEW FUNCTION ---
def listen_print_loop(responses, callback):  # <-- MODIFIED: Add a callback parameter
    """
    Iterates through server responses, prints them, and calls a callback
    on the final transcript.
    """
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        if result.is_final:
            # Display the final transcript and clean up the line.
            sys.stdout.write(f"\r{transcript}\n")

            # --- NEW PART ---
            # Instead of just printing, send the final transcript to our processor
            callback(transcript)
            # ----------------
        else:
            # Display the partial transcript
            sys.stdout.write(f"\r{transcript}" + " " * 20)
            sys.stdout.flush()


# --- NEW FUNCTION ---
def process_voice_command(transcript):
    """
    This is the "brain" of our application. It takes the voice command,
    processes it, and triggers the image search.
    """
    print(f"🤖 Processing command: '{transcript}'")
    doc = nlp(transcript.lower())
    keywords = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            keywords.append(token.lemma_)

        if not keywords:
            print("Could not extract any meaningful keywords.")
            return
    print(f"🔑 Extracted Keywords: {keywords}")
    # find_and_display_images(keywords) will be called from here later
    # --- INTEGRATION POINT ---
    # Join the keywords to form a clean search query.
    search_query = " ".join(keywords)
    print(f"🔎 Performing semantic search for: '{search_query}'")

    # Call your new search function!
    found_images = search_images(search_query, top_k=5)

    print("\n--- Search Results ---")
    for image_path in found_images:
        print(f"-> {image_path}")

    # FUTURE STEP: Call the image search function with these keywords.
    # find_and_display_images(keywords)


# --------------------
def main():
    """Start a streaming speech recognition request."""
    credentials_path = "/Users/faizanhajam/PycharmProjects/PythonProject3/realtimestt-473705-2f082486c0a4.json"
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = speech.SpeechClient(credentials=credentials)
    language_code = "en-US"

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    try:
        with MicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests)

            # --- MODIFIED FUNCTION CALL ---
            # We now pass our new 'process_voice_command' function as the callback.
            listen_print_loop(responses, process_voice_command)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()