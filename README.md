# 🧏‍ Deaf-Mute Language Translator Using Machine Learning

## 📌 Overview
This project aims to bridge communication gaps for the deaf and mute community by translating **sign language gestures into text and speech** using machine learning.  
It combines **computer vision** and **deep learning models** with a simple web interface to provide real-time translation.

---

## 🚀 Features
- Real-time gesture recognition using webcam input.
- Machine Learning model (CNN/Transfer Learning) for sign classification.
- Web-based interface (HTML, CSS, JavaScript) for user interaction.
- Output in both **text** and **speech** formats.
- Scalable design for adding more gestures and languages.

---

## 🛠️ Tech Stack
- **Python** (Core ML logic, OpenCV, TensorFlow/Keras/PyTorch)
- **HTML, CSS, JavaScript** (Front-end interface)
- **Flask/Streamlit** (Backend integration – optional)
- **Dataset**: Sign language gesture dataset (e.g., ASL, ISL)

---

## 📂 Project Structure
SmartSign-AI-main/
│── models/              # Trained ML models
│── dataset/             # Gesture dataset (not included in repo)
│── static/              # CSS, JS files
│── templates/           # HTML files
│── app.py               # Main application script
│── requirements.txt     # Dependencies

---

## 🛡️ Best Practices & Optimization

### 1. Environment Stability
- **Virtual Environment**: Always run inside a virtual environment (`venv`) to avoid global conflicts.
- **Dependencies Audit**: Keep `requirements.txt` lean (only necessary libraries).

### 2. Model Efficiency
- **Lightweight Models**: Prefer Mediapipe landmarks over heavy CNNs for real-time gesture detection where possible.
- **Quantization**: Use TensorFlow Lite or PyTorch quantized models to reduce memory usage.
- **GPU Utilization**: Ensure CUDA/cuDNN is enabled if you have an NVIDIA GPU for faster processing.

### 3. System Hygiene
- **Background Apps**: Close browsers, IDEs, and heavy apps before running to free up resources.
- **Power Settings**: Switch laptop to "High Performance" mode.
- **Memory Cleanup**: The application automatically performs memory cleanup using `gc.collect()`.

---

## ✅ Verification Ritual

Before deploying or presenting, run through these checks:

1. **Run Desktop App**: `python app.py` 
   - Check webcam activation and ensure there is no lag.
2. **Run Web App**: `python app_flask.py`
   - Verify the Flask server is running smoothly at `http://127.0.0.1:5000`.
3. **Pipeline Check**: Verify the entire flow: `Gesture → Text → Speech → AI Sentence Builder (via Ollama)`.
