import cv2
import mediapipe as mp
import numpy as np

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='models/hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1)

landmarker = HandLandmarker.create_from_options(options)

def predict_from_roi(roi):
    if roi is None or roi.size == 0:
        return ""
        
    rgb_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    result = landmarker.detect(mp_image)
    
    if not result.hand_landmarks:
        return ""
        
    landmarks = result.hand_landmarks[0]
    wrist = landmarks[0]
    
    def dist(lm1, lm2):
        return np.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)
    
    # Finger states: True if open/straight, False if curled
    # We now check if the tip is further from the wrist than the pip joint!
    fingers_open = [
        dist(wrist, landmarks[8]) > dist(wrist, landmarks[6]),   # Index
        dist(wrist, landmarks[12]) > dist(wrist, landmarks[10]), # Middle
        dist(wrist, landmarks[16]) > dist(wrist, landmarks[14]), # Ring
        dist(wrist, landmarks[20]) > dist(wrist, landmarks[18])  # Pinky
    ]
    
    # Thumb state: check if thumb tip is further from pinky base than its IP joint
    thumb_open = dist(landmarks[4], landmarks[17]) > dist(landmarks[3], landmarks[17])
    
    # Calculate distance between thumb tip and index tip for letters like F, O
    thumb_index_dist = dist(landmarks[4], landmarks[8])
    
    # ASL Heuristics Mapping
    if thumb_index_dist < 0.05 and all(fingers_open[1:]): 
        return "F"
    elif thumb_index_dist < 0.05 and not any(fingers_open[1:]):
        return "O"
    
    # Convert bool array to string for easy matching e.g. [True, False, False, False] -> "1000"
    state = "".join(["1" if f else "0" for f in fingers_open])
    
    if state == "0000":
        if thumb_open:
            return "A"
        else:
            return "E" # or S depending on thumb position
    elif state == "1111":
        return "B"
    elif state == "1000":
        if thumb_open:
            return "L"
        else:
            return "D"
    elif state == "0001":
        if thumb_open:
            return "Y"
        else:
            return "I"
    elif state == "1100":
        return "V" # Or 2
    elif state == "1110":
        return "W" # Or 3
        
    return "" # Unknown gesture
