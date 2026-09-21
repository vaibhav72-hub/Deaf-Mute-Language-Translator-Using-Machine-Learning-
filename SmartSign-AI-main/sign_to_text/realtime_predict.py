import time
import string

def predict_from_roi(roi):
    # Dummy prediction because Mediapipe's legacy solutions API is not available
    # in this Python environment. This cycles through A-Z, 0-9, SPACE, and DEL.
    characters = list(string.ascii_uppercase) + [str(i) for i in range(10)] + ["SPACE", "DEL"]
    idx = int(time.time()) % len(characters)
    return characters[idx]


