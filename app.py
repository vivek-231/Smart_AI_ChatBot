from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import traceback
import urllib.request
import urllib.parse
import json
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Ollama Configuration for SPEED
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:1b"  # Fast 1B parameter model for quick responses

# Chat history storage
chat_history = {}

# 🎛️ RESPONSE MANAGEMENT CONFIGURATION
RESPONSE_CONFIG = {
    "max_length": 2000,  # Maximum words per response (increased for full content)
    "personality": "friendly",  # friendly, professional, casual, technical
    "response_style": "detailed",  # concise, detailed, creative
    "use_emojis": True,  # Add emojis to responses
    "language": "english",  # Response language
    "filter_inappropriate": True,  # Filter inappropriate content
    "add_context": True,  # Include conversation context
}

# 🎨 PERSONALITY TEMPLATES
PERSONALITY_PROMPTS = {
    "friendly": "You are a friendly, helpful AI assistant. Be warm, encouraging, and provide detailed, comprehensive answers. Explain things thoroughly and give examples when helpful. Use emojis occasionally to make responses engaging.",
    "professional": "You are a professional AI assistant. Be formal, precise, and provide detailed, well-structured responses. Include relevant details, examples, and explanations to give comprehensive answers.",
    "casual": "You are a casual, laid-back AI assistant. Be relaxed, use simple language, but still provide detailed and helpful responses. Explain things in an easy-to-understand way with plenty of context.",
    "technical": "You are a technical AI assistant. Be precise, use technical terms when appropriate, and provide detailed, comprehensive explanations. Include technical details, examples, and step-by-step guidance.",
    "creative": "You are a creative AI assistant. Be imaginative, use metaphors and analogies, and provide detailed, engaging responses. Explain concepts creatively while being thorough and informative."
}

# 🚫 INAPPROPRIATE CONTENT FILTER
INAPPROPRIATE_WORDS = [
    "hate", "stupid", "idiot", "dumb", "kill", "die", "suicide", "violence"
]

def filter_response(response):
    """Filter inappropriate content from responses"""
    if not RESPONSE_CONFIG["filter_inappropriate"]:
        return response
    
    response_lower = response.lower()
    for word in INAPPROPRIATE_WORDS:
        if word in response_lower:
            return "I prefer to keep our conversation positive and helpful. Could you rephrase that?"
    return response

def complete_response_naturally(response, max_words=500):
    """Complete response only when absolutely necessary"""
    words = response.split()
    
    # If response is within limit, return as is
    if len(words) <= max_words:
        return response
    
    # Only truncate if response is extremely long (over 2x the limit)
    if len(words) > max_words * 2:
        # Find a good breaking point only for extremely long responses
        truncated = " ".join(words[:max_words])
        
        # Look for paragraph breaks or major section breaks
        last_double_newline = truncated.rfind('\n\n')
        last_triple_newline = truncated.rfind('\n\n\n')
        
        # Use paragraph breaks if available
        if last_triple_newline > max_words * 0.8:
            response = truncated[:last_triple_newline]
        elif last_double_newline > max_words * 0.8:
            response = truncated[:last_double_newline]
        else:
            # Only add ellipsis if absolutely necessary
            response = truncated + "..."
    
    return response

def customize_response(response, user_message=""):
    """Apply customizations to the response"""
    # Complete response naturally
    response = complete_response_naturally(response, RESPONSE_CONFIG["max_length"])
    
    # Add emojis if enabled (more subtle for detailed responses)
    if RESPONSE_CONFIG["use_emojis"]:
        if "hello" in response.lower() or "hi" in response.lower():
            response = "👋 " + response
        elif "thank" in response.lower():
            response = response + " 😊"
        elif "help" in response.lower():
            response = "🤝 " + response
        elif "error" in response.lower() or "problem" in response.lower():
            response = "⚠️ " + response
        elif "great" in response.lower() or "excellent" in response.lower():
            response = response + " ✨"
        elif "idea" in response.lower() or "suggestion" in response.lower():
            response = response + " 💡"
    
    # Apply content filter
    response = filter_response(response)
    
    return response

def generate_fast_ollama_response(prompt, session_id):
    """Generate fast Ollama response with optimized settings"""
    try:
        # Get or create chat history for this session
        if session_id not in chat_history:
            chat_history[session_id] = []
        
        # Prepare messages with context using personality template
        personality = RESPONSE_CONFIG["personality"]
        system_prompt = PERSONALITY_PROMPTS.get(personality, PERSONALITY_PROMPTS["friendly"])
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add recent conversation history (last 3 messages for speed)
        recent_history = chat_history[session_id][-3:] if len(chat_history[session_id]) > 3 else chat_history[session_id]
        messages.extend(recent_history)
        
        # Add current user message
        messages.append({"role": "user", "content": prompt})
        
        # Optimized Ollama request for DETAILED responses
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,  # Higher temperature for more creative, detailed responses
                "top_p": 0.9,        # Focus on most likely tokens
                "top_k": 40,         # Allow more vocabulary for detailed responses
                "repeat_penalty": 1.1,
                "num_predict": 2000,  # Allow much longer responses
                "stop": []  # No stop parameters - let bot complete full responses
            }
        }
        
        start_time = time.time()
        
        # Prepare the request
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/chat",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Make the request with timeout
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    ai_response = data.get("message", {}).get("content", "I'm sorry, I couldn't generate a response.")
                    
                    # Update chat history
                    chat_history[session_id].append({"role": "user", "content": prompt})
                    chat_history[session_id].append({"role": "assistant", "content": ai_response})
                    
                    # Keep history manageable (last 10 messages)
                    if len(chat_history[session_id]) > 10:
                        chat_history[session_id] = chat_history[session_id][-10:]
                    
                    response_time = time.time() - start_time
                    print(f"⚡ Ollama response in {response_time:.2f}s: {ai_response[:50]}...")
                    
                    # Apply customizations to the response
                    customized_response = customize_response(ai_response, prompt)
                    
                    return customized_response
                else:
                    print(f"❌ Ollama error: {response.status}")
                    return "I'm having trouble connecting to my AI brain. Please try again."
        except urllib.error.URLError as e:
            if "timed out" in str(e):
                print("⏰ Ollama request timed out")
                return "Response taking too long. Please try a shorter question."
            else:
                print(f"❌ Ollama connection error: {e}")
                return "I'm having trouble connecting to Ollama. Please ensure it's running."
    except Exception as e:
        print(f"❌ Ollama error: {str(e)}")
        return "I'm having trouble connecting to Ollama. Please ensure it's running."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        session_id = data.get("sessionId", "default")
        
        if not user_message:
            return jsonify({"success": False, "error": "No message provided"}), 400
        
        # Generate fast AI response
        ai_response = generate_fast_ollama_response(user_message, session_id)
        
        return jsonify({
            "success": True,
            "response": ai_response,
            "sessionId": session_id
        })
        
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return jsonify({"success": False, "error": f"Failed to process message: {str(e)}"}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    try:
        data = request.json
        session_id = data.get("sessionId", "default")
        
        if session_id in chat_history:
            del chat_history[session_id]
        
        return jsonify({
            "success": True,
            "message": "Chat history cleared successfully!"
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to reset: {str(e)}"}), 500

# 🎛️ RESPONSE MANAGEMENT ENDPOINTS
@app.route('/config', methods=['GET'])
def get_config():
    """Get current response configuration"""
    return jsonify({
        "success": True,
        "config": RESPONSE_CONFIG,
        "available_personalities": list(PERSONALITY_PROMPTS.keys())
    })

@app.route('/config', methods=['POST'])
def update_config():
    """Update response configuration"""
    try:
        data = request.json
        updates = data.get("updates", {})
        
        # Update configuration
        for key, value in updates.items():
            if key in RESPONSE_CONFIG:
                RESPONSE_CONFIG[key] = value
        
        return jsonify({
            "success": True,
            "message": "Configuration updated successfully!",
            "config": RESPONSE_CONFIG
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to update config: {str(e)}"}), 500

@app.route('/personality/<personality>', methods=['POST'])
def set_personality(personality):
    """Change bot personality"""
    try:
        if personality in PERSONALITY_PROMPTS:
            RESPONSE_CONFIG["personality"] = personality
            return jsonify({
                "success": True,
                "message": f"Personality changed to {personality}",
                "personality": personality
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Invalid personality. Available: {list(PERSONALITY_PROMPTS.keys())}"
            }), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to change personality: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Quick Ollama health check
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=2) as response:
            ollama_status = "Connected" if response.status == 200 else "Disconnected"
    except:
        ollama_status = "Disconnected"
    
    return jsonify({
        "status": "OK",
        "ollama": {
            "url": OLLAMA_URL,
            "model": OLLAMA_MODEL,
            "status": ollama_status
        },
        "features": {
            "chat": "Available",
            "speech_recognition": "Available"
        }
    })

# Get list of available microphones
mic_list = sr.Microphone.list_microphone_names()
available_mics = [{"index": i, "name": name} for i, name in enumerate(mic_list)]

@app.route('/')
def index():
    return render_template('index.html', microphones=available_mics)

@app.route('/manage')
def manage():
    """Response management interface"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Response Management</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; text-align: center; }}
            .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            button {{ background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }}
            button:hover {{ background: #0056b3; }}
            select, input {{ padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 3px; }}
            .status {{ background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎛️ Bot Response Management</h1>
            
            <div class="section">
                <h3>🎭 Change Personality</h3>
                <select id="personality">
                    <option value="friendly">Friendly</option>
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="technical">Technical</option>
                    <option value="creative">Creative</option>
                </select>
                <button onclick="setPersonality()">Apply</button>
            </div>
            
            <div class="section">
                <h3>⚙️ Response Settings</h3>
                <label>Max Words: <input type="number" id="maxLength" value="50" min="10" max="200"></label><br>
                <label>Use Emojis: <input type="checkbox" id="useEmojis" checked></label><br>
                <label>Filter Content: <input type="checkbox" id="filterContent" checked></label><br>
                <button onclick="updateConfig()">Update Settings</button>
            </div>
            
            <div class="section">
                <h3>📊 Current Configuration</h3>
                <div id="currentConfig">Loading...</div>
                <button onclick="loadConfig()">Refresh</button>
            </div>
            
            <div class="section">
                <h3>🧪 Test Bot</h3>
                <input type="text" id="testMessage" placeholder="Type a test message..." style="width: 300px;">
                <button onclick="testBot()">Send Test</button>
                <div id="testResponse" style="margin-top: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px;"></div>
            </div>
        </div>
        
        <script>
            function setPersonality() {{
                const personality = document.getElementById('personality').value;
                fetch('/personality/' + personality, {{method: 'POST'}})
                .then(r => r.json())
                .then(data => {{
                    alert(data.message);
                    loadConfig();
                }});
            }}
            
            function updateConfig() {{
                const updates = {{
                    max_length: parseInt(document.getElementById('maxLength').value),
                    use_emojis: document.getElementById('useEmojis').checked,
                    filter_inappropriate: document.getElementById('filterContent').checked
                }};
                
                fetch('/config', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{updates}})
                }})
                .then(r => r.json())
                .then(data => {{
                    alert(data.message);
                    loadConfig();
                }});
            }}
            
            function loadConfig() {{
                fetch('/config')
                .then(r => r.json())
                .then(data => {{
                    document.getElementById('currentConfig').innerHTML = 
                        '<pre>' + JSON.stringify(data.config, null, 2) + '</pre>';
                }});
            }}
            
            function testBot() {{
                const message = document.getElementById('testMessage').value;
                if (!message) return;
                
                fetch('/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{sessionId: 'test', message}})
                }})
                .then(r => r.json())
                .then(data => {{
                    document.getElementById('testResponse').innerHTML = 
                        '<strong>Bot Response:</strong><br>' + data.response;
                }});
            }}
            
            // Load config on page load
            loadConfig();
        </script>
    </body>
    </html>
    """

@app.route('/record', methods=['POST'])
def record_audio():
    try:
        mic_index = request.form.get("mic_index")
        if not mic_index:
            return jsonify({"error": "No microphone selected"}), 400
        
        try:
            mic_index = int(mic_index)
        except ValueError:
            return jsonify({"error": "Invalid microphone index"}), 400
        
        if mic_index < 0 or mic_index >= len(mic_list):
            return jsonify({"error": "Microphone index out of range"}), 400
        
        print(f"Using microphone index: {mic_index}")

        recognizer = sr.Recognizer()
        
        # Open the microphone and record audio
        with sr.Microphone(device_index=mic_index) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster ambient noise adjustment
            print("Listening... Speak now!")
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)  # Shorter timeouts

        # Convert speech to text
        text = recognizer.recognize_google(audio)
        
        return jsonify({"text": text})

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio. Please try again."}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech Recognition request failed: {e}"}), 500
    except Exception as e:
        print("Unexpected error:", traceback.format_exc())
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Fast Chatbot Server starting...")
    print(f"🤖 Using Ollama: {OLLAMA_URL} with model: {OLLAMA_MODEL}")
    print("⚡ Optimized for speed - responses should be under 0.5 seconds!")
    app.run(debug=True, host='0.0.0.0', port=5000)