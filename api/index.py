from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'), 
            static_folder=os.path.join(base_dir, 'static'))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = []

SYSTEM_PROMPT = "You are a friendly AI assistant like the magic mirror in Snow White. Respond as if you were the Magic Mirror from Snow White movie."

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/voice")
def voice():
    global conversation_history
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]

    if os.name == 'nt':  # 'nt' înseamnă Windows
        temp_path = "input_temp.mp4" # Salvează direct în folderul proiectului pe laptop
    else:
        temp_path = "/tmp/input.mp4" # Salvează în folderul temporar pe Vercel

    audio_file.save(temp_path)

    try:
        with open(temp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=f
            )
        user_text = transcript.text

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += conversation_history[-6:] # Ultimele 6 replici
        messages.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        ai_answer = response.choices[0].message.content

        conversation_history.append({"role": "user", "content": user_text})
        conversation_history.append({"role": "assistant", "content": ai_answer})

        return jsonify({"transcript": user_text, "answer": ai_answer})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


app = app 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
