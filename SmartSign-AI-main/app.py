import cv2
from sign_to_text.realtime_predict import predict_from_roi
from ai_ollama.sentence_builder import build_sentence
from text_to_speech.speak import speak

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

detected_text = ""
current_letter = ""

print("Controls:")
print("A = accept letter | S = space | D = delete | Q = quit & speak")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # ROI
    x1, y1 = int(w * 0.55), int(h * 0.25)
    x2, y2 = int(w * 0.9), int(h * 0.75)

    roi = frame[y1:y2, x1:x2]
    letter = predict_from_roi(roi)

    if letter:
        current_letter = letter

    # Draw UI
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.putText(frame, f"Current: {current_letter}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(frame, f"Text: {detected_text}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

    cv2.imshow("SmartSign AI", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):               # Accept letter
        if current_letter == "DEL":
            detected_text = detected_text[:-1]
        else:
            detected_text += current_letter
        current_letter = ""

    elif key == ord('s'):             # Space
        detected_text += " "

    elif key == ord('d'):             # Delete
        detected_text = detected_text[:-1]

    elif key == ord('q'):             # Quit + Speak
        break

# 🔻 AFTER CAMERA LOOP
cap.release()
cv2.destroyAllWindows()

# 🔊 FINAL OUTPUT
if detected_text.strip():
    print("\nDetected word:", detected_text)

    sentence = build_sentence(detected_text)
    print("AI sentence:", sentence)

    speak(sentence)
else:
    print("\nNo sign detected.")
