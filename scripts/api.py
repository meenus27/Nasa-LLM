from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

@app.route("/voice-ui")
def voice_ui():
    return send_from_directory(directory=os.path.abspath(os.path.dirname(__file__)), path="voice.html")

@app.route("/voice", methods=["POST"])
def receive_voice():
    data = request.get_json()
    query = data.get("query", "")
    if query:
        with open("latest_query.txt", "w", encoding="utf-8") as f:
            f.write(query)
        return {"status": "success"}
    return {"status": "error", "message": "No query provided"}, 400

if __name__ == "__main__":
    app.run(debug=True)



