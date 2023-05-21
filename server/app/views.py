from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from PIL import Image
import numpy as np
import joblib

# Load your trained model
model = joblib.load('./trained_models/HGBR.sav')

def predict(request):
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image found'})

    image = request.FILES['image']
    # Load the image
    img = Image.open(image)

    # Resize the image to 64x64
    resized_image = img.resize((64, 64))

    # Convert the resized image to RGB
    rgb_image = resized_image.convert('RGB')

    # Convert the RGB image to a 1D array
    array_1d = np.array(rgb_image).reshape(12288)
    prediction = model.predict([array_1d])
    print(prediction)
    # Perform further processing on the prediction if needed
    return JsonResponse({'prediction': prediction.tolist()})
