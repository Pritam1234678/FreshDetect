# 🍏 FreshDetect - AI-Powered Fruit Freshness Detector

[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7.svg)](https://freshdetect.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![ONNX](https://img.shields.io/badge/ONNX-Runtime-orange.svg)](https://onnxruntime.ai/)

**FreshDetect** is an AI-powered web application that analyzes fruit images to determine their freshness level using deep learning. Upload an image, and get instant freshness scores with visual heatmap analysis!

## 🌐 Live Demo

**🚀 Access the app:** [https://freshdetect.onrender.com](https://freshdetect.onrender.com)

> **Note:** The app is hosted on Render's free tier, so it may take 30-60 seconds to wake up if idle.

## ✨ Features

- 🎯 **Real-time Analysis** - Instant fruit freshness detection
- 📊 **Freshness Score** - Get a score from 0-100
- 🌡️ **Visual Heatmap** - See which areas affect freshness
- 🎨 **Modern UI** - Beautiful, responsive interface
- 🚀 **Fast API** - Built with FastAPI for high performance
- 🔍 **Three Categories** - Fresh, Mid-Rotten, or Rotten

## 🏗️ Architecture

```
FreshDetect/
├── backend/
│   ├── main.py              # FastAPI backend
│   ├── requirements.txt     # Python dependencies
│   └── runtime.txt          # Python version
├── frontend/
│   ├── index.html          # Main UI
│   ├── script.js           # Frontend logic
│   └── style.css           # Styling
├── food_freshness_model.onnx  # AI Model (ONNX format)
├── Dockerfile              # Container configuration
└── render.yaml            # Render deployment config
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance web framework
- **ONNX Runtime** - Optimized model inference
- **OpenCV** - Image processing
- **Uvicorn** - ASGI server

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework overhead
- **Responsive Design** - Works on all devices

### AI/ML
- **ONNX Model** - Optimized neural network
- **Image Processing** - HSV, Laplacian, fusion techniques

## 🚀 Deployment

### Deployed on Render

The app is deployed on Render using Docker:

1. **Automatic Deployment** - Connected to GitHub
2. **Docker Container** - Isolated environment
3. **Free Tier** - No cost hosting
4. **Auto-redeploy** - Updates on git push

### Deploy Your Own

1. **Fork this repository**
2. **Sign up on [Render](https://render.com)**
3. **Create a new Web Service**
4. **Connect your GitHub repo**
5. **Render will auto-detect the configuration**
6. **Click "Deploy"** ✅

## 💻 Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Pritam1234678/FreshDetect.git
cd FreshDetect
```

2. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the backend**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. **Open in browser**
```
http://localhost:8000
```

### Using Docker

```bash
# Build the image
docker build -t freshdetect .

# Run the container
docker run -p 8000:8000 freshdetect
```

## 📡 API Endpoints

### `GET /`
Returns the frontend web interface

### `POST /predict`
Analyzes fruit freshness from uploaded image

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "score": 75.5,
  "class": "Fresh",
  "heatmap": "data:image/jpeg;base64,..."
}
```

### `GET /docs`
Interactive API documentation (Swagger UI)

## 🎯 How It Works

1. **Upload Image** - User uploads a fruit image
2. **Preprocessing** - Image is resized and normalized
3. **Feature Extraction** - RGB, HSV, and Laplacian features
4. **AI Inference** - ONNX model predicts freshness
5. **Score Calculation** - Returns 0-100 score
6. **Classification** - Categorizes as Fresh/Mid-Rotten/Rotten
7. **Heatmap** - Generates visual attention map

## 📊 Freshness Categories

| Score | Category | Color |
|-------|----------|-------|
| 60-100 | 🟢 Fresh | Green |
| 40-60 | 🟡 Mid-Rotten | Orange |
| 0-40 | 🔴 Rotten | Red |

## 🔧 Configuration

### Environment Variables
- `PORT` - Server port (default: 8000)
- `MODEL_PATH` - Path to ONNX model

### Render Configuration
See `render.yaml` for deployment settings.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Pritam**
- GitHub: [@Pritam1234678](https://github.com/Pritam1234678)

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- ONNX Runtime for model optimization
- Render for free hosting

---

**⭐ Star this repo if you find it useful!**

Made with ❤️ and Python
