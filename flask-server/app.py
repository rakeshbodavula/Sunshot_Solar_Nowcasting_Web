from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import joblib
from flask_cors import CORS
import os
from waitress import serve

app = Flask(__name__)
CORS(app)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

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

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
