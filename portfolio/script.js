import { HandLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0";

const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");
const loader = document.getElementById("loader");

const currentLetterEl = document.getElementById("currentLetter");
const detectedTextEl = document.getElementById("detectedText");

let handLandmarker = undefined;
let webcamRunning = false;
let lastVideoTime = -1;
let currentPrediction = "";
let builtSentence = "";

// Initialize Mediapipe
async function createHandLandmarker() {
    const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
    );
    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`,
            delegate: "GPU"
        },
        runningMode: "VIDEO",
        numHands: 1
    });
    
    loader.style.display = "none";
    enableCam();
}
createHandLandmarker();

// Start Webcam
function enableCam() {
    if (!handLandmarker) return;

    const constraints = { video: true };
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
    });
}

// Distance helper
function dist(lm1, lm2) {
    return Math.sqrt(Math.pow(lm1.x - lm2.x, 2) + Math.pow(lm1.y - lm2.y, 2));
}

// Predict Loop
async function predictWebcam() {
    canvasElement.style.width = video.videoWidth;
    canvasElement.style.height = video.videoHeight;
    canvasElement.width = video.videoWidth;
    canvasElement.height = video.videoHeight;

    let startTimeMs = performance.now();
    if (lastVideoTime !== video.currentTime) {
        lastVideoTime = video.currentTime;
        const results = handLandmarker.detectForVideo(video, startTimeMs);

        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

        currentPrediction = "";

        if (results.landmarks && results.landmarks.length > 0) {
            const landmarks = results.landmarks[0];
            const wrist = landmarks[0];

            // Draw landmarks
            for (const lm of landmarks) {
                canvasCtx.beginPath();
                canvasCtx.arc(lm.x * canvasElement.width, lm.y * canvasElement.height, 4, 0, 2 * Math.PI);
                canvasCtx.fillStyle = "#3b82f6";
                canvasCtx.fill();
            }

            // Heuristic Engine
            const fingers_open = [
                dist(wrist, landmarks[8]) > dist(wrist, landmarks[6]),   // Index
                dist(wrist, landmarks[12]) > dist(wrist, landmarks[10]), // Middle
                dist(wrist, landmarks[16]) > dist(wrist, landmarks[14]), // Ring
                dist(wrist, landmarks[20]) > dist(wrist, landmarks[18])  // Pinky
            ];

            const thumb_open = dist(landmarks[4], landmarks[17]) > dist(landmarks[3], landmarks[17]);
            const thumb_index_dist = dist(landmarks[4], landmarks[8]);

            if (thumb_index_dist < 0.05 && fingers_open.slice(1).every(v => v === true)) {
                currentPrediction = "F";
            } else if (thumb_index_dist < 0.05 && fingers_open.slice(1).every(v => v === false)) {
                currentPrediction = "O";
            } else {
                const state = fingers_open.map(f => f ? "1" : "0").join("");
                
                if (state === "0000") {
                    currentPrediction = thumb_open ? "A" : "E";
                } else if (state === "1111") {
                    currentPrediction = "B";
                } else if (state === "1000") {
                    currentPrediction = thumb_open ? "L" : "D";
                } else if (state === "0001") {
                    currentPrediction = thumb_open ? "Y" : "I";
                } else if (state === "1100") {
                    currentPrediction = "V";
                } else if (state === "1110") {
                    currentPrediction = "W";
                }
            }
        }
        
        currentLetterEl.innerText = currentPrediction || "-";
        canvasCtx.restore();
    }
    
    window.requestAnimationFrame(predictWebcam);
}

// Controls
function updateText() {
    detectedTextEl.innerText = builtSentence || "Start signing...";
}

document.getElementById("acceptBtn").addEventListener("click", () => {
    if (currentPrediction) {
        builtSentence += currentPrediction;
        updateText();
    }
});

document.getElementById("spaceBtn").addEventListener("click", () => {
    builtSentence += " ";
    updateText();
});

document.getElementById("deleteBtn").addEventListener("click", () => {
    builtSentence = builtSentence.slice(0, -1);
    updateText();
});

document.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    if (key === 'a') document.getElementById("acceptBtn").click();
    if (key === 's') document.getElementById("spaceBtn").click();
    if (key === 'd') document.getElementById("deleteBtn").click();
});
