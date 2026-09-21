import time

def predict_from_roi(roi):
    # Dummy prediction to allow the pipeline to run without TensorFlow
    # In a real scenario, we would use Mediapipe or a TFLite model here
    # Return "A" occasionally just to simulate detection
    if int(time.time()) % 5 == 0:
        return "A"
    return ""
