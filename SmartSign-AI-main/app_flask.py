from flask import Flask, render_template, Response, jsonify
import cv2
import gc

from utils.threaded_camera import ThreadedCamera
from sign_to_text.realtime_predict import predict_from_roi
from ai_ollama.sentence_builder import build_sentence
from text_to_speech.speak import speak

app = Flask(__name__)

camera = ThreadedCamera(src=0, width=640, height=480).start()

detected_text = ""
current_letter = ""


@app.route("/")
def index():
    return render_template("index.html")


def generate_frames():
    global detected_text, current_letter
    frame_count = 0

    while True:
        ret, frame = camera.read()
        if not ret or frame is None:
            continue
            
        frame_count += 1

        h, w, _ = frame.shape
        x1, y1 = int(w * 0.55), int(h * 0.25)
        x2, y2 = int(w * 0.9), int(h * 0.75)

        if frame_count % 2 == 0:
            roi = frame[y1:y2, x1:x2]
            letter = predict_from_roi(roi)

            if letter:
                current_letter = letter

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 3)
        cv2.putText(frame, f"Current: {current_letter}", (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Text: {detected_text}", (10,80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        if frame_count % 30 == 0:
            gc.collect()


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/finalize")
def finalize():
    global detected_text
    sentence = build_sentence(detected_text)
    speak(sentence)

    response = {
        "detected": detected_text,
        "sentence": sentence
    }
    detected_text = ""
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=False)
