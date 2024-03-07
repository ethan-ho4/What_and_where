import requests
# import os
import io
# from io import BytesIO
from PIL import Image
import base64

# import re
# import numpy as np
# from PIL import Image as im 
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

#Send post to Grounding Dino server
#Input: Server address, Audio transcription, and file path to image
#Output: Returns confidence, accuracy, numerical information about the bounding box, and information about the annotated image so it can be recreated

def send_post_dino(api_url, prompt, image_path):
    with Image.open(image_path) as image:
        original_rgb_image = image.convert('RGB')
        buffered = io.BytesIO()
        original_rgb_image.save(buffered, format="JPEG")
        original_img_byte = buffered.getvalue()
        original_base64 = base64.b64encode(original_img_byte)
        original_base64_img = original_base64.decode('utf-8')

        data = {
                "prompt": prompt,
                "image": original_base64_img,
        }
        
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            response_data = response.json()
            boxes = response_data["confidence"]["boxes"]
            accuracy = response_data["confidence"]["accuracy"]
            object_names = response_data["confidence"]["object_names"]
            annotated_image_list = response_data["annotated_image"]["array"]
            annotated_image_shape = response_data["annotated_image"]["shape"]
            
            return(boxes, accuracy, object_names, annotated_image_list, annotated_image_shape)

