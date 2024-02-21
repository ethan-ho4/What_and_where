import sounddevice as sd
import wave
import threading
import queue
import whisper
import os
import keyboard
import numpy as np

# Define constants
THRESHOLD_DB = -40  # Threshold in decibels
SILENCE_THRESHOLD = 10  # Number of consecutive silent chunks to trigger a new file
SAMPLE_DURATION = 0.1  # Duration of each audio chunk in seconds
FS = 44100  # Sample rate in Hz
CHANNELS = 1  # Number of audio channels
SILENCE_DURATION = SILENCE_THRESHOLD * SAMPLE_DURATION

# Calculate Root Mean Square (RMS) of audio data
def calculate_rms(audio_data):
    return np.sqrt(np.mean(np.square(audio_data), axis=0))

# Convert RMS amplitude to decibels
def amp_to_db(rms):
    return 20 * np.log10(rms)

#Detect keyboard interrupt crtl c
interrupt = False

# Record audio chunk
def record_chunk(duration, fs, channels):
    sd.wait()  # Wait for the recording to finish
    return sd.rec(int(duration * fs), samplerate=fs, channels=channels, dtype='float32')

# Write audio data to WAV file
def write_wave(filename, data, fs, channels):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes for 'int16' dtype
        wf.setframerate(fs)
        wf.writeframes(data.tobytes())

# Handle audio recording logic
def record_audio(audio_queue, stop_recording_event, audio_directory):
    file_number = 1
    silence_count = 0  # Count consecutive silent chunks
    with sd.InputStream(samplerate=FS, channels=CHANNELS, dtype='float32') as stream:
        while not stop_recording_event.is_set():
            audio_data = np.empty((0, CHANNELS), dtype='float32')
            print(f"Starting new recording segment {file_number}")

            while not stop_recording_event.is_set():
                audio_chunk, overflowed = stream.read(int(FS * SAMPLE_DURATION))
                if overflowed:
                    print("Warning: audio input overflowed")

                rms_value = calculate_rms(audio_chunk)
                db_value = amp_to_db(rms_value)

                if db_value < THRESHOLD_DB: 
                    silence_count += SAMPLE_DURATION
                    if silence_count >= SILENCE_DURATION:
                        silence_count = 0
                        print(f"Silence detected for {SILENCE_DURATION} seconds. Starting a new segment.")
                        break
                else:
                    silence_count = 0
                    audio_data = np.concatenate((audio_data, audio_chunk), axis=0)
 
                if keyboard.is_pressed('space'):
                    print("Spacebar pressed, stopping recording.")
                    stop_recording_event.set()

            if audio_data.size > 0:
                audio_data_int16 = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
                filename = os.path.join(audio_directory, f'segment_{file_number}.wav')
                write_wave(filename, audio_data_int16, FS, CHANNELS)
                audio_queue.put(filename)
                print(f"Finished segment {file_number}, saved to file.")
                file_number += 1

# Transcribe audio files
def transcribe_audio(audio_queue, stop_recording_event, model, audio_directory):
    # Initialize a string to hold all transcriptions
    all_transcriptions = ""

    while not stop_recording_event.is_set() or not audio_queue.empty():
        print("Transcription thread is polling the queue...")  # Debug print
        filename = audio_queue.get()
        if filename is None:
            continue

        print(f"Attempting to transcribe file: {filename}")  # Debug print
        if os.path.getsize(filename) > 44:  # Check if file is not just a header
            try:
                print(f"Transcribing {filename}")
                result = model.transcribe(filename)
                transcription_text = result['text']
                print(f"Transcription for {filename} complete.")  # Debug print
                
                # Append the transcription text to the all_transcriptions string
                all_transcriptions += f"{transcription_text}\n"

            except Exception as e:
                print(f"An error occurred while transcribing {filename}: {e}")
        else:
            print(f"File {filename} is empty or invalid and will be skipped.")

        audio_queue.task_done()
    
    # At this point, all_transcriptions contains all the transcribed text.
    # You can return it or print it out.
    print(all_transcriptions)
    return all_transcriptions
