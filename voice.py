from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
import json
import base64

# Load environment variables
load_dotenv()

# NVIDIA API key
NVIDIA_API_KEY = os.getenv('./api.env')

# NVIDIA NIM API endpoints (replace with actual endpoints)
NIM_ASR_URL = "https://api.nvidia.com/v1/speech:recognize"
NIM_TTS_URL = "https://api.nvidia.com/v1/speech:synthesize"
NIM_CHAT_URL = "https://api.nvidia.com/v1/chat:completion"

app = Flask(__name__)

conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['message']
    response = process_input(user_input)
    return jsonify({'response': response})

@app.route('/voice_input', methods=['POST'])
def voice_input():
    audio_data = request.files['audio'].read()
    text = transcribe_audio(audio_data)
    if text.strip():
        response = process_input(text)
        return jsonify({'text': text, 'response': response})
    return jsonify({'error': 'No speech detected'})

def process_input(text):
    global conversation_history
    conversation_history.append({"role": "user", "content": text})
    response = get_ai_response(text)
    conversation_history.append({"role": "assistant", "content": response})
    return response

def transcribe_audio(audio):
    try:
        audio_base64 = base64.b64encode(audio).decode('utf-8')
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": 16000,
                "languageCode": "en-US",
            },
            "audio": {
                "content": audio_base64
            }
        }
        response = requests.post(NIM_ASR_URL, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()
        return result['results'][0]['alternatives'][0]['transcript']
    except (requests.exceptions.HTTPError, KeyError) as e:
        print(f"Error transcribing audio: {e}")
        return ""

def get_ai_response(text):
    try:
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": conversation_history,
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024
        }
        response = requests.post(NIM_CHAT_URL, headers=headers, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        result = response.json()
        return result['choices'][0]['message']['content']
    except (requests.exceptions.HTTPError, KeyError) as e:
        print(f"Error getting AI response: {e}")
        return "Sorry, I couldn't process that."

if __name__ == '__main__':
    app.run(debug=True)
