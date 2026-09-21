import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands if hasattr(mp, 'solutions') else mp.python.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

def predict_from_roi(roi):
    if roi is None or roi.size == 0:
        return ""
    
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if not results.multi_hand_landmarks:
        return ""
        
    hand_landmarks = results.multi_hand_landmarks[0]
    
    # Simple finger counting logic
    fingers = 0
    # Thumb
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        fingers += 1
    # 4 Fingers
    tips = [mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, 
            mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]
    pips = [mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, 
            mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.PINKY_PIP]
            
    for tip, pip in zip(tips, pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            fingers += 1
            
    # Map fingers to letters for demonstration
    mapping = {0: "SPACE", 1: "A", 2: "B", 3: "C", 4: "D", 5: "E"}
    return mapping.get(fingers, "")
