import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import onnxruntime as ort
import numpy as np
import cv2
from PIL import Image
import io
import os

app = FastAPI()


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    import cv2
except ImportError:
    print("CRITICAL ERROR: Could not import cv2. Please install opencv-python.")
    sys.exit(1)

# Health Check
@app.get("/")
def home():
    return {"status": "online", "message": "Fruit Freshness Backend is Running"}

# ---------------------------------------------------
# MODEL LOADING
# ---------------------------------------------------
# Model path - works both locally and in Docker container
MODEL_PATH = os.environ.get("MODEL_PATH", "../food_freshness_model.onnx")
if not os.path.exists(MODEL_PATH):
    # Try Docker path
    MODEL_PATH = "/app/food_freshness_model.onnx"

try:
    session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    session = None

import base64

# ... (imports)

# ---------------------------------------------------
# PREPROCESS FUNCTION
# ---------------------------------------------------
def preprocess_image(img_pil, size=256):
    img_np_rgb = np.array(img_pil)
    img_bgr = cv2.cvtColor(img_np_rgb, cv2.COLOR_RGB2BGR)
    
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (size, size))

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_32F)
    lap = np.abs(lap)

    # Normalize Laplacian for visualization
    lap_norm = (lap - lap.min()) / (lap.max() - lap.min() + 1e-6)
    lap_vis = (lap_norm * 255).astype(np.uint8)
    
    # Create Heatmap (JET colormap)
    heatmap_img = cv2.applyColorMap(lap_vis, cv2.COLORMAP_JET)
    
    # Encode Heatmap to Base64
    _, buffer = cv2.imencode('.jpg', heatmap_img)
    heatmap_b64 = base64.b64encode(buffer).decode('utf-8')

    lap = lap_vis
    lap = np.expand_dims(lap, -1)

    fused = np.concatenate([img, hsv, lap], axis=-1).astype(np.float32) / 255.0
    fused = np.transpose(fused, (2, 0, 1))[None, :]
    
    return fused, heatmap_b64

# ---------------------------------------------------
# PREDICT ENDPOINT
# ---------------------------------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if session is None:
        return JSONResponse(content={"error": "Model not loaded"}, status_code=500)

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Get input tensor AND heatmap
        input_tensor, heatmap_b64 = preprocess_image(image)
        
        output = session.run(None, {input_name: input_tensor})[0][0]
        score = float(output)
        score = max(0, min(100, score))

        if score < 40:
            cls = "Rotten"
        elif score <= 60:
            cls = "Mid-Rotten"
        else:
            cls = "Fresh"

        return {
            "score": score,
            "class": cls,
            "heatmap": f"data:image/jpeg;base64,{heatmap_b64}"
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ---------------------------------------------------
# STATIC FILES (Frontend Hosting)
# ---------------------------------------------------
# This allows the backend to serve the frontend files directly.
# Access app at http://localhost:8000 or https://your-render-url.onrender.com
FRONTEND_PATH = "../frontend"
if not os.path.exists(FRONTEND_PATH):
    # Try Docker path
    FRONTEND_PATH = "/app/frontend"

if os.path.exists(FRONTEND_PATH):
    app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")
    print(f"✅ Frontend mounted from {FRONTEND_PATH}")
else:
    print("⚠️  Warning: Frontend directory not found. API only mode.")
    print(f"   Tried paths: ../frontend and /app/frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
