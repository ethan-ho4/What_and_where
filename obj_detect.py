from groundingdino.util.inference import load_model, load_image, predict, annotate
import supervision as sv
import cv2
import os

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


    #annotate image
    annotated_image = annotate(image_source = image_source, boxes = detected_boxes, logits = accuracy, phrases = obj_name)
    print(annotated_image.shape)

    #display images using supervision
    sv.plot_image(annotated_image, (16,16))
