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
    
    # Finger states: True if open/straight, False if curled
    # For index to pinky, we check if the tip is higher than the pip joint
    fingers_open = [
        landmarks[8].y < landmarks[6].y,   # Index
        landmarks[12].y < landmarks[10].y, # Middle
        landmarks[16].y < landmarks[14].y, # Ring
        landmarks[20].y < landmarks[18].y  # Pinky
    ]
    
    # Thumb state is trickier (depends on hand orientation, but we'll use a basic distance heuristic)
    thumb_open = landmarks[4].x < landmarks[3].x if landmarks[17].x > landmarks[5].x else landmarks[4].x > landmarks[3].x
    
    # Calculate distance between thumb tip and index tip for letters like F, O
    thumb_index_dist = np.sqrt((landmarks[4].x - landmarks[8].x)**2 + (landmarks[4].y - landmarks[8].y)**2)
    
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
