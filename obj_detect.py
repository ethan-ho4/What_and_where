from groundingdino.util.inference import load_model, load_image, predict, annotate
import supervision as sv
import cv2
import os

from io import BytesIO
import base64
import numpy as np
import io

#Detects object using Grounding Dino Locally
#Input: Image path and what it should detect
#Output: Annotated image and values associated with the bounding box that was annotated on the iamge as well as confidence

def object_detect(image_path, search_prompt):
    CONFIG_PATH = r"groundingdino\config\GroundingDINO_SwinT_OGC.py"
    CHECK_POINT_PATH = r"weights\weights.pth"

    model = load_model(CONFIG_PATH, CHECK_POINT_PATH)

    IMAGE_PATH = image_path
    TEXT_PROMPT = search_prompt
    BOX_THRESHOLD = 0.35
    TEXT_THRESHOLD = 0.25

    image_source, myimage = load_image(IMAGE_PATH)

    detected_boxes, accuracy, obj_name = predict(
        model= model,
        image = myimage,
        caption = TEXT_PROMPT,
        box_threshold = BOX_THRESHOLD,
        text_threshold = TEXT_THRESHOLD,
    )

    print(detected_boxes, accuracy, obj_name)

    annotated_image = annotate(image_source = image_source, boxes = detected_boxes, logits = accuracy, phrases = obj_name)
    sv.plot_image(annotated_image, (16,16))
