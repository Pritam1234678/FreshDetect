
import sys

def check_import(module_name):
    try:
        __import__(module_name)
        print(f"[OK] {module_name}")
    except ImportError as e:
        print(f"[FAIL] {module_name}: {e}")

print("Checking dependencies...")
check_import("fastapi")
check_import("uvicorn")
check_import("onnxruntime")
check_import("cv2") # opencv-python-headless
check_import("PIL")
check_import("numpy")
print("Done.")
