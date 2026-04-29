function startSign() {
    fetch("/start_sign");
}

function startSpeech() {
    fetch("/start_speech");
}

function updateStatus() {
    fetch("/status")
        .then(res => res.json())
        .then(data => {
            document.getElementById("mode").innerText = data.mode;
            document.getElementById("status").innerText = data.status;
            document.getElementById("detected").innerText = data.detected_text || "---";
            document.getElementById("final").innerText = data.final_sentence || "---";
        });
}

setInterval(updateStatus, 1000);
