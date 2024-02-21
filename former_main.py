import sounddevice as sd
import wave
import threading
import queue
import whisper 
import os
import keyboard
import numpy as np

from STT import record_audio
from STT import transcribe_audio

from LLM import send_post


import threading
import queue
import os
import keyboard

from STT import record_audio
from STT import transcribe_audio

from LLM import send_post

# ...rest of your main function...

def main():
    audio_directory = "recorded_audio"
    os.makedirs(audio_directory, exist_ok=True)

    model = whisper.load_model("base")

    audio_queue = queue.Queue()
    stop_recording_event = threading.Event()

    recording_thread = threading.Thread(target=record_audio, args=(audio_queue, stop_recording_event, audio_directory))
    transcription_thread = threading.Thread(target=transcribe_audio, args=(audio_queue, stop_recording_event, model, audio_directory))
     
    print("Press spacebar to start recording.")
    keyboard.wait('space')
    transcription_thread.start()
    recording_thread.start()

    print("Recording... Press spacebar to stop.")
    keyboard.wait('space')  # This will block until the spacebar is pressed 
    stop_recording_event.set()  # Signal the recording to stop

    # Signal the transcription thread to finish by putting None in the queue
    audio_queue.put(None)

    # Wait for both threads to finish
    recording_thread.join()
    transcription_thread.join()

    #collect transcription
    full_transcription = ""
    while not audio_queue.empty():
        full_transcription += audio_queue.get

    #not transcription thread
    print("Recording and transcription have finished.")
    print("is the audio here:",full_transcription )

    ##########################    

    #api endpoint
    url = "http://127.0.0.1:5000/v1/chat/completions"
 
    #location of transcription.txt 
    file_directory = os.path.join(os.getcwd(),'recorded_audio', 'transcription.txt')

    send_post(url, file_directory)

 
if __name__ == "__main__":
    main()  
    