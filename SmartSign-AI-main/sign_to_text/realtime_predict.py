import time
import string
import cv2
import numpy as np

def predict_from_roi(roi):
    if roi is None or roi.size == 0:
        return ""
        
    # Check if a hand/object is in the ROI using edge density
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges) / 255.0 / (edges.shape[0] * edges.shape[1])
    
    # If the bounding box is empty (edge density < 2%), return nothing
    if edge_density < 0.02:
        return ""

    # Dummy prediction because Mediapipe's legacy solutions API is not available
    # in this Python environment. This cycles through A-Z, 0-9, SPACE, and DEL.
    characters = list(string.ascii_uppercase) + [str(i) for i in range(10)] + ["SPACE", "DEL"]
    idx = int(time.time() / 3) % len(characters)
    return characters[idx]
