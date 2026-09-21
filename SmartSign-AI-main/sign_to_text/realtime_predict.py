import time

def predict_from_roi(roi):
    # Dummy prediction because Mediapipe's legacy solutions API is not available
    # in this Python environment. This cycles through A-E every few seconds.
    letters = ["A", "B", "C", "D", "E"]
    idx = int(time.time() / 2) % len(letters)
    return letters[idx]

