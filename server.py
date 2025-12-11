from flask import Flask, request, jsonify
from openai import OpenAI
import os, json

# Flask app nu trebuie să ruleze, doar pentru handler
app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
CONVO_FILE = "conversation.json"

# Încarcă conversația existentă
if os.path.exists(CONVO_FILE):
    with open(CONVO_FILE, "r", encoding="utf-8") as f:
        conversation_history = json.load(f)
else:
    conversation_history = []

SYSTEM_PROMPT = """You are a friendly AI assistant. 
Remember all previous conversations with the user.
"""

@app.route("/voice", methods=["POST"])
def voice():
    global conversation_history
    audio_file = request.files["audio"]

    # Whisper API de la OpenAI
    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    user_text = result.text

    # Pregătește mesajele pentru ChatGPT
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_history
    messages.append({"role": "user", "content": user_text})

    # Chat completions
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    ai_answer = response.choices[0].message.content

    # Salvează conversația
    conversation_history.append({"role": "user", "content": user_text})
    conversation_history.append({"role": "assistant", "content": ai_answer})

    with open(CONVO_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=2)

    return jsonify({"transcript": user_text, "answer": ai_answer})
