import os
import queue
import threading
import keyboard
import whisper
from record import record_audio
from transcribe import transcribe_audio
from word_search import contains_word
from mistral_api import send_post_mistral
from obj_detect import object_detect
from cv_live import camera_feed  # Ensure this is the correct import for your camera_feed function

URL = "http://127.0.0.1:5000/v1/chat/completions"

def main():
    audio_directory = "recorded_audio"
    os.makedirs(audio_directory, exist_ok=True)

    if not os.path.exists('feed_images'):
        os.makedirs('feed_images')

    model = whisper.load_model("base")

    audio_queue = queue.Queue()
    result_queue = queue.Queue()
    stop_recording_event = threading.Event()
    capture_event = threading.Event()  # Define capture event for the camera feed

    # Pass the result queue to the transcription thread
    transcription_thread = threading.Thread(target=transcribe_audio, args=(audio_queue, stop_recording_event, model, result_queue))
    recording_thread = threading.Thread(target=record_audio, args=(audio_queue, stop_recording_event, audio_directory))
    camera_thread = threading.Thread(target=camera_feed, args=(capture_event, 'feed_images', 'capture.png'))  # Add capture event and image info

    print("Press spacebar to start recording and live cam.")
    keyboard.wait('space')  
    transcription_thread.start()
    recording_thread.start()
    camera_thread.start()

    print("Recording and camera feed active... Press spacebar to capture image and stop.")
    keyboard.wait('space')
    capture_event.set() 
    stop_recording_event.set()
    audio_queue.put(None)

    # Wait for threads to finish
    recording_thread.join()
    transcription_thread.join()
    camera_thread.join()

    # Retrieve the full transcription from the result queue after both threads have finished
    full_transcription = result_queue.get()
    if full_transcription is None:
        print("No transcription was produced.")
        return  # Exit if there was no transcription

    print("User transcribed audio:", full_transcription)    

    image_path = r"feed_images/capture.png"

    # Process the transcription
    # if contains_word(full_transcription, "what") and contains_word(full_transcription, "where"):
        # # print("following what and where path")
        # # #print("[debug] following what and where path")

        # what_prompt = 'With the following text, determine if the sentence is more similar to a "what" or "where" question? if the answer is "what", remove "where" and create a meaningful question.'

        # # what_prompt = 'With the following text, isolate and return the "what" question:'

        # what = send_post_mistral(URL, full_transcription, what_prompt)
        # #print("[debug] what: {what}")
        # #print(f"[info] what: {what}")
        # prompt = "please answer the question:  "
        # send_post_mistral(URL, what, prompt)

        # where_prompt = 'With the following text, isolate and return the "where" question:'  
        # where = send_post_mistral(URL, full_transcription, where_prompt)
        # print(where)
        # object_detect(image_path, where)


    if contains_word(full_transcription, "what"):
        print("following what path")
        prompt = ""
        send_post_mistral(URL, full_transcription, prompt)

    elif contains_word(full_transcription, "where"):
        print("following where path")
        object_detect(image_path, full_transcription)    
    
    else:
        print("following what path")
        prompt = ""
        send_post_mistral(URL, full_transcription, prompt)

if __name__ == "__main__":
    main()
  