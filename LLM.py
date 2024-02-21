import requests
import json
import os

def send_post(api_url, transcription):

    # Read the file in binary mode, then decode with 'utf-8' and replace errors
    user_transcription = transcription

    data = {
        "Content-Type": "application/json",
        "messages": [
            {
            "role": "user",
            "content": user_transcription
            }
        ],
        "mode": "chat",
        "character": "Example"
        }

    # Sending a POST request to the API
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        content = response_data['choices'][0]['message']['content']
        # print("grab recording", os.getcwd())
        # file_directory = os.path.join(os.getcwd(),'recorded_audio', 'transcription.txt')
        
        # # r"C:\Users\ethan\Desktop\work\demos\gtc-demo1\recorded_audio\transcription.txt"
        # with open(file_directory, 'w') as file:
        #     pass

        print("User audio input prompt:", transcription)
        print("LLM response:", content)
    else:
        print("Error:", response.status_code, response.text)
