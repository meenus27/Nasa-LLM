<!DOCTYPE html>
<html>
<head><title>Voice Input</title></head>
<body>
  <h2>🎤 Speak your query</h2>
  <button onclick="startDictation()">Start Voice Input</button>
  <p id="status"></p>

  <script>
    function startDictation() {
      if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(event) {
          const transcript = event.results[0][0].transcript;
          document.getElementById("status").innerText = "You said: " + transcript;

          fetch("http://localhost:5000/voice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: transcript })
          }).then(res => {
            if (res.ok) {
              document.getElementById("status").innerText += " ✅ Sent to Streamlit";
            }
          });
        };

        recognition.onerror = function(event) {
          console.error("Speech recognition error:", event.error);
        };
      } else {
        alert("Speech recognition not supported in this browser.");
      }
    }
  </script>
</body>
</html>

