import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import CSS file for styling

const App = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
    setPreviewImage(URL.createObjectURL(file)); // Store image URL for preview
  };

  const handlePrediction = async () => {
    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      // const response = await axios.post('https://sunshot-solar-nowcasting-web-server.onrender.com/predict', formData, {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log(response.data); // Check response data in console
      setPrediction(response.data.prediction[0]); // Update prediction state
    } catch (error) {
      console.error('Error occurred during prediction:', error);
    }
  };

  return (
    <div className="app">
      <h1 className="app-title">Sunshot Solar Nowcasting</h1>
      <p><span>How it works: </span>
        Upload a sky image and you will get the PV value generated in Kilo Watts for that image.</p>
      <input type="file" onChange={handleImageUpload} className="file-input" />
      <button onClick={handlePrediction} className="predict-button">Predict</button>
      <h2>Uploaded Image: </h2>
      {previewImage && <img src={previewImage} alt="Uploaded" className="preview-image" />} {/* Display uploaded image */}
      {prediction && <p className="prediction">PV value Predicted: {prediction} KW</p>} {/* Render prediction value */}
    </div>
  );
};

export default App;
