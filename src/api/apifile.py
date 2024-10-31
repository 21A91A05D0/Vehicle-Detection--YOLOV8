# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 00:26:53 2024

@author: PRAVEEN
"""



from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import onnxruntime as ort
import io

# Initialize the FastAPI app
app = FastAPI()

# Load your YOLOv8 model in .onnx format
ort_session = ort.InferenceSession("D:/tmp/vehicle-detection-yolov8-main/tmp/last.onnx")

# Function to preprocess the image (resize, normalize, etc.)
def preprocess(image: Image.Image):
    # Resize the image to the expected YOLOv8 input size (e.g., 640x640)
    image = image.resize((640, 640))
    # Convert the image to a NumPy array and normalize pixel values
    image = np.array(image).astype(np.float32) / 255.0
    # Rearrange dimensions to (batch, channels, height, width)
    image = np.transpose(image, (2, 0, 1))
    # Add a batch dimension
    image = np.expand_dims(image, axis=0)
    return image

# Function to make predictions
def predict(image: Image.Image):
    # Preprocess the input image
    input_data = preprocess(image)
    
    # Run inference with the ONNX model
    outputs = ort_session.run(None, {"images": input_data})
    
    # Extract the output (the model's predictions)
    # Modify this part based on the output format of your YOLOv8 model
    boxes = outputs[0]
    
    return boxes

# Endpoint for image upload and inference
@app.post("/predict")
async def predict_vehicle(file: UploadFile = File(...)):
    # Read the image file
    image = Image.open(io.BytesIO(await file.read()))
    
    # Perform prediction on the uploaded image
    results = predict(image)
    
    # Return the predictions as a JSON response
    return JSONResponse({"predictions": results.tolist()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
