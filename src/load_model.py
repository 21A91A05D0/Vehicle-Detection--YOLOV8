# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 23:26:57 2024

@author: PRAVEEN
"""

import onnxruntime as ort
from PIL import Image
import numpy as np
import io

# Load your model
ort_session = ort.InferenceSession("D:/tmp/vehicle-detection-yolov8-main/tmp/last.onnx")

def preprocess(image: Image.Image):
    # Resize and normalize the image (based on YOLOv8 input requirements)
    image = image.resize((640, 640))
    image = np.array(image).astype(np.float32) / 255.0
    image = np.transpose(image, (2, 0, 1))  # Convert to (channels, height, width)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

def predict(image: Image.Image):
    # Preprocess the image
    input_data = preprocess(image)
    
    # Run the model
    outputs = ort_session.run(None, {"images": input_data})
    
    # Process outputs (bounding boxes, labels, etc.)
    return outputs
