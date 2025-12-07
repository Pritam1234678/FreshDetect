import streamlit as st
import onnxruntime as ort
import numpy as np
import cv2
from PIL import Image

# ---------------------------------------------------
# MODEL PATH
# ---------------------------------------------------
MODEL_PATH = "food_freshness_model.onnx"

# Load ONNX model
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

# Get input name
input_name = session.get_inputs()[0].name


# ---------------------------------------------------
# PREPROCESS FUNCTION (from your predict.py)
# ---------------------------------------------------
def preprocess_image(img, size=256):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (size, size))

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_32F)
    lap = np.abs(lap)

    lap = (lap - lap.min()) / (lap.max() - lap.min() + 1e-6)
    lap = (lap * 255).astype(np.uint8)
    lap = np.expand_dims(lap, -1)

    fused = np.concatenate([img, hsv, lap], axis=-1).astype(np.float32) / 255.0
    fused = np.transpose(fused, (2, 0, 1))[None, :]
    return fused


# ---------------------------------------------------
# PREDICT FUNCTION (Merged)
# ---------------------------------------------------
def predict_freshness(image_np):

    input_tensor = preprocess_image(image_np)
    output = session.run(None, {input_name: input_tensor})[0][0]

    score = float(output)
    score = max(0, min(100, score))

    if score < 40:
        cls = "Rotten"
    elif score <= 60:
        cls = "Mid-Rotten"
    else:
        cls = "Fresh"

    return score, cls


# ---------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------
st.set_page_config(page_title="Fruit Freshness Detector", layout="centered")
st.title("🍎 Fruit Freshness Prediction (ONNX Model)")

uploaded = st.file_uploader("Upload a Fruit Image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    if st.button("Analyze Freshness"):

        score, cls = predict_freshness(img_cv)

        st.subheader("🔍 Prediction Result")
        st.write(f"**Freshness Score:** {score:.2f} / 100")
        st.write(f"**Category:** {cls}")

        st.progress(int(score))
