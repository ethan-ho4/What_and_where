import os
import queue
import whisper

def concat_audio_transcription(current_transcription, text_to_add):
    return current_transcription + f"{text_to_add}\n"

# Transcribe audio files
def transcribe_audio(audio_queue, stop_recording_event, model, result_queue):
    full_transcription = ""
    # Initialize a string to hold all transcriptions

    while not stop_recording_event.is_set() or not audio_queue.empty():
        print("Transcription thread is polling the queue...")  # Debug print
        filename = audio_queue.get()

        # Check for the sentinel value to end the loop
        if filename is None:
            # Signal that there are no more files to process
            # Don't put None into the result_queue
            break

        print(f"Attempting to transcribe file: {filename}")  # Debug print
        if os.path.getsize(filename) > 44:  # Check if file is not just a header
            try:
                print(f"Transcribing {filename}")
                result = model.transcribe(filename)
                transcription_text = result['text']
                print(f"Transcription for {filename} complete.")  # Debug print
                
                # Append the transcription text to the full_transcription string
                full_transcription = concat_audio_transcription(full_transcription, transcription_text)

            except Exception as e:
                print(f"An error occurred while transcribing {filename}: {e}")

            print("this is the audio input per file:", full_transcription)

        else:
            print(f"File {filename} is empty or invalid and will be skipped.")

        audio_queue.task_done()

    # Once all transcriptions are done, put the full transcription into the result queue
    result_queue.put(full_transcription)
