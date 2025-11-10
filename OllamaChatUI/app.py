import os
import subprocess
import time
import requests
from flask import Flask, request, jsonify, send_from_directory
import threading

app = Flask(__name__, static_folder='static')

OLLAMA_URL = "http://localhost:11434"
ollama_process = None

def start_ollama_server():
    """Start Ollama server in the background"""
    global ollama_process
    print("Starting Ollama server...")
    try:
        ollama_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(5)
        print("Ollama server started")
        return True
    except Exception as e:
        print(f"Error starting Ollama server: {e}")
        return False

def pull_default_model():
    """Pull a default model if none exists"""
    print("Pulling default model (llama3.2:1b)...")
    try:
        subprocess.run(
            ["ollama", "pull", "llama3.2:1b"],
            check=True,
            timeout=600
        )
        print("Model pulled successfully")
        return True
    except Exception as e:
        print(f"Error pulling model: {e}")
        return False

def initialize_ollama():
    """Initialize Ollama in a background thread"""
    if start_ollama_server():
        pull_default_model()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": user_message,
                "stream": False,
                "system": "You are a helpful, concise AI assistant. Give brief, direct answers without extra elaboration.",
                "options": {
                    "temperature": 0.7,
                    "num_predict": 100,
                    "stop": ["\n\nUser:", "User:", "\nUser"]
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', 'No response from AI')
            
            ai_response = ai_response.split('\n\n')[0]
            ai_response = ai_response.split('User:')[0]
            ai_response = ai_response.split('Question:')[0]
            
            sentences = ai_response.split('.')
            if len(sentences) > 3:
                ai_response = '. '.join(sentences[:3]) + '.'
            
            return jsonify({'response': ai_response.strip()})
        else:
            return jsonify({'error': 'Failed to get response from Ollama'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error communicating with Ollama: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if response.status_code == 200:
            return jsonify({'status': 'ready'})
    except:
        pass
    return jsonify({'status': 'initializing'}), 503

if __name__ == '__main__':
    threading.Thread(target=initialize_ollama, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
