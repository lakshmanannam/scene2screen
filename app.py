import os
import requests
import json
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, send_file

app = Flask(__name__)
app.secret_key = 'super-secret-cinema-key'

# Ollama Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "granite4:micro"

def generate_with_ollama(prompt, max_tokens=2000):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7, 
            "num_predict": max_tokens
        }
    }
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', '').strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.json
    # Matches the 'storyline' key sent by the updated script.js
    storyline = data.get('storyline', '') 

    if not storyline:
        return jsonify({'error': 'No storyline provided'}), 400

    # 1. Screenplay Generation
    screenplay_prompt = f"Write a professional screenplay based ONLY on this idea: {storyline}. Use INT/EXT headings, character names centered, and dialogue."
    screenplay = generate_with_ollama(screenplay_prompt, 2500)
    
    # 2. Character Profile Generation
    char_prompt = f"Based on this script: {screenplay}\n\nCreate detailed character profiles including motivations and arcs."
    characters = generate_with_ollama(char_prompt, 2000)

    # 3. Sound Design Generation
    sound_prompt = f"Based on this script: {screenplay}\n\nCreate a detailed sound design and music plan for each scene."
    sound_design = generate_with_ollama(sound_prompt, 2000)
    
    # Store in session
    session['storyline'] = storyline
    session['screenplay'] = screenplay
    session['characters'] = characters
    session['sound_design'] = sound_design
    
    return jsonify({'success': True})

@app.route('/get_generated_content', methods=['GET'])
def get_generated_content():
    return jsonify({
        'storyline': session.get('storyline', ''),
        'screenplay': session.get('screenplay', ''),
        'characters': session.get('characters', ''),
        'sound_design': session.get('sound_design', '')
    })

if __name__ == '__main__':
    # Ensure port 5000 is used as expected by the user
    app.run(debug=True, port=5000)