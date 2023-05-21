from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import joblib
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load('./trained_models/HGBR.sav')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found'})
    image = request.files['image']
    # Load the image
    image = Image.open(image)

    # Resize the image to 64x64
    resized_image = image.resize((64, 64))

    # Convert the resized image to RGB
    rgb_image = resized_image.convert('RGB')

    # Convert the RGB image to a 1D array
    array_1d = np.array(rgb_image).reshape(12288)
    prediction = model.predict([array_1d])
    # Perform further processing on the prediction if needed
    return jsonify({'prediction': list(prediction)})