// ===============================
// Copy Translation
// ===============================
function copyText() {

    const text = document.getElementById("translatedText").innerText;

    navigator.clipboard.writeText(text)
        .then(() => {
            alert("✅ Translation copied!");
        })
        .catch(err => {
            console.log(err);
        });
}

// ===============================
// Clear Text
// ===============================
function clearText() {

    document.getElementById("inputText").value = "";

    let output = document.getElementById("translatedText");

    if (output) {
        output.innerHTML = "";
    }

}

// ===============================
// Text To Speech
// ===============================
function speakText() {

    const text = document.getElementById("translatedText").innerText;

    if (text == "") {
        alert("Nothing to speak!");
        return;
    }

    const speech = new SpeechSynthesisUtterance(text);

    speech.rate = 1;

    speech.pitch = 1;

    speech.volume = 1;

    window.speechSynthesis.speak(speech);

}

// ===============================
// Voice Input
// ===============================
function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert("Speech Recognition is not supported in this browser.");

        return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onstart = function () {

        alert("🎤 Speak now...");

    };

    recognition.onresult = function (event) {

        const text = event.results[0][0].transcript;

        document.getElementById("inputText").value = text;

    };

    recognition.onerror = function () {

        alert("Voice Recognition Failed");

    };

}

// ===============================
// Swap Languages
// ===============================
function swapLanguage() {

    const target = document.getElementById("target");

    if (target.value == "te") {

        target.value = "en";

    }
    else {

        target.value = "te";

    }

}

// ===============================
// Theme Toggle
// ===============================
function toggleTheme() {

    document.body.classList.toggle("light");

}

// ===============================
// Search History
// ===============================
function searchTable() {

    let input = document.getElementById("search").value.toLowerCase();

    let rows = document.querySelectorAll("table tr");

    rows.forEach(function (row, index) {

        if (index == 0) return;

        if (row.innerText.toLowerCase().includes(input)) {

            row.style.display = "";

        }
        else {

            row.style.display = "none";

        }

    });

}

// ===============================
// Loading Animation
// ===============================
const form = document.getElementById("translateForm");

if (form) {

    form.addEventListener("submit", function () {

        const button = form.querySelector("button[type='submit']");

        button.innerHTML = "⏳ Translating...";

        button.disabled = true;

    });

}

// ===============================
// Character Counter
// ===============================
const textarea = document.getElementById("inputText");

if (textarea) {

    const counter = document.createElement("p");

    counter.style.marginTop = "10px";

    counter.style.color = "white";

    textarea.parentNode.insertBefore(counter, textarea.nextSibling);

    textarea.addEventListener("input", function () {

        counter.innerHTML =
            "Characters : " + textarea.value.length;

    });

}

// ===============================
// Auto Scroll to Result
// ===============================
window.onload = function () {

    const result = document.querySelector(".result");

    if (result) {

        result.scrollIntoView({

            behavior: "smooth"

        });

    }

};

// ===============================
// Download Notification
// ===============================
function downloadMessage() {

    alert("📥 Download Started");

}
function copyFavorite(id){

    let text = document.getElementById(id).innerText;

    navigator.clipboard.writeText(text);

    alert("Favorite Copied!");

}