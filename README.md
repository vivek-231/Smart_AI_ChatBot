# 🤖 Smart AI Chatbot

A powerful, ChatGPT-like chatbot with advanced image analysis capabilities using **100% FREE, UNLIMITED AI** via Ollama.

## ✨ Features

- **🧠 Smart AI Chat**: Powered by Ollama (100% FREE, unlimited usage)
- **📷 Image Analysis**: Upload images and get AI-powered insights
- **🔍 OCR Technology**: Extract text from images using Tesseract.js
- **🎤 Voice Input**: Speech-to-text functionality
- **💾 Session Management**: Remember your chat history and uploaded images
- **🎨 Modern UI**: Beautiful, responsive design with smooth animations
- **📱 Mobile Friendly**: Works perfectly on all devices
- **💰 Zero Cost**: No API fees, no usage limits, no credit card required

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- **Ollama** (free AI tool that runs locally)

### 1. Install Ollama (100% FREE)
```bash
# Windows: Download from https://ollama.ai/download
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Setup Ollama
```bash
# Start Ollama service
ollama serve

# Download a model (in new terminal)
ollama pull llama2
```

### 3. Setup Backend
```bash
cd ChatBot/nodejs-backend
npm install
```

### 4. Environment Variables
Create a `.env` file in the `nodejs-backend` folder:
```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
PORT=5000
```

### 5. Start Backend
```bash
npm start
```

### 6. Open Frontend
Open `ChatBot/frontend/index.html` in your browser

## 🔧 How It Works

### Chat Flow
1. **Text Chat**: Type messages and get AI responses (100% free)
2. **Image Upload**: Click the file icon to upload images
3. **AI Analysis**: Each image gets OCR text extraction + AI insights
4. **Context Awareness**: Chatbot remembers all your images and provides context-aware responses

### Special Commands
- **"analyze images"** - Get comprehensive analysis of all uploaded images
- **"reset"** or **"clear"** - Clear chat and image history

### Image Processing
- Supports: JPG, PNG, GIF, BMP, TIFF
- OCR text extraction
- AI-powered content analysis
- Session-based storage

## 🎯 Use Cases

- **Document Analysis**: Upload receipts, forms, documents
- **Image Understanding**: Get descriptions and insights from photos
- **Text Extraction**: Convert image text to editable format
- **Content Analysis**: Understand what's in your images
- **Learning Assistant**: Ask questions about uploaded content

## 🛠️ Technical Stack

- **Backend**: Node.js + Express
- **AI**: **Ollama (100% FREE, unlimited, local)**
- **OCR**: Tesseract.js
- **Frontend**: Vanilla JavaScript + CSS3
- **Styling**: Modern CSS with gradients and animations

## 📁 Project Structure

```
ChatBot/
├── nodejs-backend/
│   ├── server.js          # Main backend server
│   ├── package.json       # Dependencies
│   ├── .env              # Environment variables
│   └── OLLAMA_SETUP.md   # Ollama setup guide
├── frontend/
│   ├── index.html        # Main HTML file
│   ├── styles.css        # Styling
│   ├── scripts.js        # Frontend logic
│   └── images/           # UI icons
└── README.md             # This file
```

## 🔑 API Endpoints

- `POST /chat` - Main chat endpoint
- `POST /extract-text` - Image upload and analysis
- `GET /image-history/:sessionId` - Get session images
- `POST /analyze-all-images` - Analyze all images together
- `POST /reset` - Clear session data
- `GET /health` - Health check with cost info

## 💰 Cost Comparison

| Service | Cost | Usage | Privacy |
|---------|------|-------|---------|
| **Ollama (This Bot)** | **$0** | **Unlimited** | **100% Local** |
| OpenAI GPT-4 | $0.03/1K tokens | Limited | Cloud-based |
| Google Gemini | $0.0025/1K tokens | Limited | Cloud-based |
| Anthropic Claude | $0.015/1K tokens | Limited | Cloud-based |

## 🎨 Customization

### AI Models
Change the AI model in `nodejs-backend/server.js`:
```javascript
const OLLAMA_MODEL = "llama3.2:1b"; // Fast 1B parameter model for quick responses
```

### Colors
Edit `frontend/styles.css` to change the color scheme:
```css
:root {
  --primary-color: #6c63ff;
  --secondary-color: #5a52d5;
  --background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 🐛 Troubleshooting

### Common Issues
1. **"Ollama connection error"**: Make sure Ollama is running (`ollama serve`)
2. **"Model not found"**: Download a model first (`ollama pull llama2`)
3. **"Port already in use"**: Change PORT in `.env` or kill existing process
4. **"Image processing failed"**: Ensure image format is supported

### Ollama Commands
```bash
ollama list          # Show installed models
ollama pull llama2   # Download Llama2 model
ollama run llama2    # Test the model
ollama serve         # Start Ollama service
```

## 🚀 Why Ollama?

- ✅ **100% FREE** - No hidden costs
- ✅ **UNLIMITED** - No rate limits or quotas
- ✅ **PRIVATE** - All data stays on your computer
- ✅ **OFFLINE** - Works without internet after setup
- ✅ **FAST** - No network delays
- ✅ **CUSTOMIZABLE** - Modify models and responses

## 📞 Support

If you encounter any issues:
1. Check the console for error messages
2. Ensure Ollama is running (`ollama serve`)
3. Verify you have a model downloaded (`ollama list`)
4. Check the network tab for API calls
5. Read `OLLAMA_SETUP.md` for detailed setup instructions

## 📄 License

This project is open source and available under the ISC License.

---

**🚀 Your chatbot now runs on 100% FREE, UNLIMITED AI with Ollama!** ✨

**No API keys, no credit cards, no usage limits - just pure, free AI power!** 🎉 