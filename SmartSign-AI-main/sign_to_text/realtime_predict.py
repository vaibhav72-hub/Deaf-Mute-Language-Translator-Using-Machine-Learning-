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
        
    hand_landmarks = result.hand_landmarks[0]
    
    # Simple finger counting logic
    fingers = 0
    # Thumb (landmark 4 compared to 3 for x-axis)
    if hand_landmarks[4].x < hand_landmarks[3].x:
        fingers += 1
    # 4 Fingers (tip vs pip y-axis)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
            
    for tip, pip in zip(tips, pips):
        if hand_landmarks[tip].y < hand_landmarks[pip].y:
            fingers += 1
            
    mapping = {0: "SPACE", 1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
    return mapping.get(fingers, "SPACE")
