import requests
import json
import os

def send_post_mistral(api_url, transcription, prompt):
    user_transcription = prompt + transcription
        

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


    else:
        print("Error:", response.status_code, response.text)

    return content, user_transcription
