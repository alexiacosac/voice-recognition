from flask import Flask, request, jsonify, send_from_directory
import whisper
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)
load_dotenv()  # încarcă variabilele din .env

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

model = whisper.load_model("small")

CONVO_FILE = "conversation.json"

# Încarcă istoricul conversației dacă există
if os.path.exists(CONVO_FILE):
    with open(CONVO_FILE, "r", encoding="utf-8") as f:
        conversation_history = json.load(f)
else:
    conversation_history = []

SYSTEM_PROMPT = """You are a friendly AI assistant. 
Remember all previous conversations with the user. 
Respond naturally and contextually, considering the full conversation history.
Always respond in a friendly, human-like way like the magic mirror in Snow White.
"""

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.post("/voice")
def voice():
    global conversation_history

    audio_file = request.files["audio"]
    audio_file.save("input.mp4")

    result = model.transcribe("input.mp4", language="en", fp16=False)
    user_text = result["text"]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_history
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    ai_answer = response.choices[0].message.content

    # Adaugă la istoricul conversației
    conversation_history.append({"role": "user", "content": user_text})
    conversation_history.append({"role": "assistant", "content": ai_answer})

    # Salvează conversația în fișier
    with open(CONVO_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=2)

    return jsonify({"transcript": user_text, "answer": ai_answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
