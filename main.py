import os
import queue
import threading
import keyboard
import whisper

from record import record_audio
from transcribe import transcribe_audio
from word_search import contains_word
from LLM import send_post

def main():
    audio_directory = "recorded_audio"
    os.makedirs(audio_directory, exist_ok=True)

    model = whisper.load_model("base")

    audio_queue = queue.Queue()
    result_queue = queue.Queue()  # Create a queue to get results from the transcription thread
    stop_recording_event = threading.Event()

    # Pass the result queue to the transcription thread
    transcription_thread = threading.Thread(target=transcribe_audio, args=(audio_queue, stop_recording_event, model, result_queue))
    recording_thread = threading.Thread(target=record_audio, args=(audio_queue, stop_recording_event, audio_directory))

    print("Press spacebar to start recording.")
    keyboard.wait('space')
    transcription_thread.start()
    recording_thread.start()

    print("Recording... Press spacebar to stop.")
    keyboard.wait('space')
    stop_recording_event.set()

    audio_queue.put(None)  # Signal the transcription thread to stop

    recording_thread.join()
    transcription_thread.join()

    # Retrieve the full transcription from the result queue after both threads have finished
    full_transcription = result_queue.get()
    if full_transcription is None:

        print("No transcription was produced.")
        return  # Exit if there was no transcription

    print("User transcribed audio:", full_transcription)

    # Process the transcription
    if contains_word(full_transcription, "what") and contains_word(full_transcription, "where"):
        print("following what and where path")

    elif contains_word(full_transcription, "what"):
        print("following what path")
        url = "http://127.0.0.1:5000/v1/chat/completions"
        send_post(url, full_transcription)

    elif contains_word(full_transcription, "where"):
        print("following where path")
    
    else:
        print("I'm not sure what you're asking")

if __name__ == "__main__":
    main()
