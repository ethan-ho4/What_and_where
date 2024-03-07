from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from io import BytesIO
from PIL import Image
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from groundingdino.util.inference import load_model, predict, annotate

import uvicorn
import base64
import numpy as np
import groundingdino.datasets.transforms as T
import torch

#Grounding Dino Fast API server
#Input: Base64 string representing the image, and prompt for what to look for
#Output: Confidence values, array and array shape to recrate the original image

<<<<<<< HEAD
=======
#Grounding Dino Fast API server
#Input: Base64 string representing the image, and prompt for what to look for
#Output: Confidence values, array and array shape to recrate the original image

>>>>>>> origin/main
class Item(BaseModel):
    prompt: str
    image: str

app = FastAPI()

CONFIG_PATH = "groundingdino/config/GroundingDINO_SwinT_OGC.py"
CHECK_POINT_PATH = "weights/weights.pth"
model = load_model(CONFIG_PATH, CHECK_POINT_PATH)

@app.post("/items/", response_model=Dict[str, object])
async def annotate_image(item: Item):
    transform = T.Compose([
        T.RandomResize([800], max_size=1333),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    image_data = base64.b64decode(item.image)
    image_source = Image.open(BytesIO(image_data)).convert("RGB")
    print(type(image_source))

    image = np.asarray(image_source)
    image_tensor, _ = transform(image_source, None)

    detected_boxes, accuracy, obj_names = predict(
        model=model,
        image=image_tensor,
        caption=item.prompt,
        box_threshold=0.35,
        text_threshold=0.25,
    )

    annotated_image_np = annotate(image_source = image, boxes = detected_boxes, logits = accuracy, phrases = obj_names)
    annotated_image_list = annotated_image_np.tolist(),
    annotated_image_shape = annotated_image_np.shape

    response_data = {
        "confidence": {
            "boxes": detected_boxes.tolist(), 
            "accuracy": accuracy.tolist(),
            "object_names": obj_names,
        },
        "annotated_image":{
            "array": annotated_image_list,
            "shape": annotated_image_shape,
        }
    }

    json_compatible_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_compatible_data)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
