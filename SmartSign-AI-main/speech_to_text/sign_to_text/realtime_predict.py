import cv2
import numpy as np
import tensorflow as tf
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "asl_cnn_model_v2.h5")

model = tf.keras.models.load_model(MODEL_PATH)

LABELS = [
    'A','B','C','D','E','F','G','H','I','J',
    'K','L','M','N','O','P','Q','R','S','T',
    'U','V','W','X','Y','Z',
    'del','nothing','space'
]

def predict_from_roi(roi):
    roi = cv2.resize(roi, (64, 64))
    roi = roi / 255.0
    roi = np.reshape(roi, (1, 64, 64, 3))

    preds = model.predict(roi, verbose=0)
    idx = int(np.argmax(preds))
    confidence = preds[0][idx]

    if confidence > 0.85 and idx < len(LABELS):
        label = LABELS[idx]

        if label == "nothing":
            return ""

        if label == "space":
            return " "

        if label == "del":
            return "DEL"

        return label

    return ""
