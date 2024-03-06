import requests
import json
import os

#sends post request to Mistral API
#Input: API address and audio transcription
#returns audio transcription and LLM response



def send_post_mistral(api_url, transcription):
        

    data = {
        "Content-Type": "application/json",
        "messages": [
            {
            "role": "user",
            "content":transcription
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

    return content, transcription
