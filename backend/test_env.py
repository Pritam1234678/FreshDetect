
import sys
import os

print("--- DIAGNOSTIC START ---")
print(f"CWD: {os.getcwd()}")

try:
    import numpy
    print("[OK] numpy imported")
except ImportError as e:
    print(f"[FAIL] numpy: {e}")

try:
    import cv2
    print("[OK] cv2 imported")
except ImportError as e:
    print(f"[FAIL] cv2: {e}")

try:
    import onnxruntime as ort
    print("[OK] onnxruntime imported")
    
    model_path = "../food_freshness_model.onnx"
    if os.path.exists(model_path):
        print(f"[OK] Model found at {model_path}")
        try:
            sess = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
            print("[OK] Model loaded successfully")
        except Exception as e:
            print(f"[FAIL] Model load error: {e}")
    else:
        print(f"[FAIL] Model NOT found at {model_path}")
        print(f"Dir listing of ..: {os.listdir('..')}")

except ImportError as e:
    print(f"[FAIL] onnxruntime: {e}")

try:
    from fastapi import FastAPI
    print("[OK] fastapi imported")
except ImportError as e:
    print(f"[FAIL] fastapi: {e}")

print("--- DIAGNOSTIC END ---")
