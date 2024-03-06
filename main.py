import os
import queue
import threading
import keyboard
import whisper
import supervision as sv
import cv2
import os
import io
import base64
import re
import numpy as np
from PIL import Image as im 
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

from io import BytesIO
from PIL import Image
from record import record_audio
from transcribe import transcribe_audio
from word_search import contains_word  
from mistral_api import send_post_mistral
from obj_detect import object_detect
from cv_live import camera_feed 
from dino_api import send_post_dino


MISTRAL_SERVER_URL = "http://127.0.0.1:5000/v1/chat/completions"
DINO_SERVER_URL = "http://127.0.0.1:8000/items/"
IMAGE_PATH = "feed_images/capture.png"

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
    camera_thread = threading.Thread(target=camera_feed, args=(capture_event, 'feed_images', 'image.png'))  # Add capture event and image info

    print("Press spacebar to start recording and live cam.")
    keyboard.wait('space')  
    transcription_thread.start()
    recording_thread.start()
    camera_thread.start()

    print("Recording and camera feed starting, please wait a moment before speaking...")
    keyboard.wait('space')
    capture_event.set() 
    stop_recording_event.set()
    audio_queue.put(None)
    print("Recording and camera feed active... Press spacebar when finished.")

    # Wait for threads to finish
    recording_thread.join()
    transcription_thread.join()
    camera_thread.join()

    # Retrieve the full transcription from the result queue after both threads have finished
    full_transcription = result_queue.get()
    if full_transcription is None:
        print("No transcription was produced.")
        return

    print("User transcribed audio:", full_transcription)    

    image_path = r"feed_images/image.png"

    # full_transcription = "where is the person"

    if contains_word(full_transcription, "what"):
        print("following what path")
        content, user_transcription = send_post_mistral(MISTRAL_SERVER_URL, full_transcription)
        print("User audio input prompt:", user_transcription)
        print("LLM response:", content)
        

    elif contains_word(full_transcription, "where"):  
        print("following where path")
        boxes, accuracy, object_names, annotated_image_list,annotated_image_shape= send_post_dino(DINO_SERVER_URL, full_transcription, image_path)
        confidence = (boxes, accuracy, object_names)    
        print(confidence)

        reconstructed_image_array = np.array(annotated_image_list, dtype=np.uint8)
        reconstructed_image_array = reconstructed_image_array.reshape(annotated_image_shape)

        data = im.fromarray(reconstructed_image_array) 
        data.save('feed_images/image_annotated.png')         
    
    else:  
        print("following what path")
        prompt = ""
        content, user_transcription = send_post_mistral(MISTRAL_SERVER_URL, full_transcription, prompt)
        print("User audio input prompt:", user_transcription)
        print("LLM response:", content)


if __name__ == "__main__":
    main()
  