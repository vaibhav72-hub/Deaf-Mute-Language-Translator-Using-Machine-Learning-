const currentLetterEl = document.getElementById("currentLetter");
const detectedTextEl = document.getElementById("detectedText");

function acceptLetter(){
    fetch("/accept", {method: "POST"})
    .then(res => res.json())
    .then(data => {
        detectedTextEl.innerText = data.detected || "Start signing...";
    });
}

function finalize(){
    fetch("/finalize")
    .then(res => res.json())
    .then(data => {
        detectedTextEl.innerText = data.sentence || data.detected || "Start signing...";
    });
}

document.getElementById("acceptBtn").addEventListener("click", () => {
    acceptLetter();
});

document.getElementById("spaceBtn").addEventListener("click", () => {
    fetch("/keypress/s", {method: "POST"})
    .then(res => res.json())
    .then(data => {
        detectedTextEl.innerText = data.detected || "Start signing...";
    });
});

document.getElementById("deleteBtn").addEventListener("click", () => {
    fetch("/keypress/d", {method: "POST"})
    .then(res => res.json())
    .then(data => {
        detectedTextEl.innerText = data.detected || "Start signing...";
    });
});

document.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    if (key === 'a') document.getElementById("acceptBtn").click();
    if (key === 's') document.getElementById("spaceBtn").click();
    if (key === 'd') document.getElementById("deleteBtn").click();
    if (key === 'q') finalize();
});

// Polling for status update (current letter and detected text)
setInterval(() => {
    fetch("/status")
    .then(res => res.json())
    .then(data => {
        currentLetterEl.innerText = data.current_letter || "-";
        if (data.detected_text) {
             detectedTextEl.innerText = data.detected_text;
        } else if (detectedTextEl.innerText !== "Start signing...") {
            if (data.detected_text === "") {
                detectedTextEl.innerText = "Start signing...";
            }
        }
    }).catch(err => console.log(err));
}, 500);
