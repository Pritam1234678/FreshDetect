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

# Expose port for Render (uses PORT environment variable)
EXPOSE $PORT
CMD uvicorn backend.main:app --host 0.0.0.0 --port $PORT
