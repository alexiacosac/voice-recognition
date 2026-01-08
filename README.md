Voice Recognition Web Assistant

This project is a web-based voice interaction application that allows users to communicate with an AI assistant using their microphone. The user speaks a question, the spoken input is transcribed and displayed on the screen and the assistant responds both in text and spoken audio.

The application runs entirely as a web app and is deployed on Vercel. It combines browser-based voice recording and speech synthesis with a Python backend that handles AI processing.

Features

- Voice input using the device microphone
- Speech-to-text transcription displayed in real time
- AI-generated responses
- Text-to-speech playback of the AI response
- Visual display of both user input and assistant output
- Continuous conversational context stored in memory

Technologies Used

Frontend
- HTML, CSS, JavaScript
- MediaRecorder API for audio capture
- Web Speech API for text-to-speech

Backend
- Python
- Flask

AI and Voice Processing
- OpenAI Whisper API for speech-to-text
- OpenAI GPT model for response generation

Deployment
- Vercel

System Overview

The user interacts with the application through a browser interface. When the microphone is activated, audio is recorded and sent to the backend server. The backend transcribes the audio using Whisper, generates a response using an AI language model, and returns the result to the frontend. The frontend then displays the response and reads it aloud using text-to-speech.

Project Flow

1. User activates the microphone
2. Audio is recorded in the browser
3. Audio is sent to the backend
4. Speech is transcribed using AI
5. AI generates a response
6. The response is displayed and spoken aloud
