FROM python:3.9

WORKDIR /app

# Copy Requirements
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy Backend Code
COPY ./backend /app/backend

# Copy Frontend Code
COPY ./frontend /app/frontend

# Copy Model
COPY ./food_freshness_model.onnx /app/food_freshness_model.onnx

# Expose port (Render defaults to 10000, Hugging Face to 7860, we'll use 8000 internally)
# We can override this in the CMD or via env vars
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
