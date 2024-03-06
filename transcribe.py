import os
import queue
import whisper

#Concatenates to a string
#Input: String
#Output: String

def concat_audio_transcription(current_transcription, text_to_add):
    return current_transcription + f"{text_to_add}\n"


#Asynchronously calls whisper AI python library to transcribe input audio and concatenates to a string
#Input: Audio
#Output: string
def transcribe_audio(audio_queue, stop_recording_event, model, result_queue):
    full_transcription = ""

    while not stop_recording_event.is_set() or not audio_queue.empty():
        print("Transcription thread is polling the queue...")
        filename = audio_queue.get()

        if filename is None:
            break

        print(f"Attempting to transcribe file: {filename}")
        if os.path.getsize(filename) > 44:
            try:
                print(f"Transcribing {filename}")
                result = model.transcribe(filename)
                transcription_text = result['text']
                print(f"Transcription for {filename} complete.")
                
                full_transcription = concat_audio_transcription(full_transcription, transcription_text)

            except Exception as e:
                print(f"An error occurred while transcribing {filename}: {e}")

            print("this is the audio input per file:", full_transcription)

        else:
            print(f"File {filename} is empty or invalid and will be skipped.")

        audio_queue.task_done()

    result_queue.put(full_transcription)
