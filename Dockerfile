# Lightweight base image with Python 3.11
FROM python:3.11-slim


# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Intall dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the standard Cloud Run port
EXPOSE 8080

# Add the root directory to PYTHONPATH to avoid import errors
ENV PYTHONPATH=/app
# Command to start FastAPI with Uvicorn from main.py using the "app" object
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
