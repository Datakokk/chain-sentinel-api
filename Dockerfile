# Lightweight base image with Python 3.11
FROM python:3.13-slim

# Install the necesary tools (include Rust and Cargo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && export PATH="/root/.cargo/bin:$PATH" \
    && rm -rf /var/lib/apt/lists/*


# Upgrade pip to the latest version
RUN pip install --upgrade pip
RUN pip install maturin

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Intall dependencies
ENV PATH="/root/.cargo/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the standard Cloud Run port
EXPOSE 8080

# Command to start FastAPI with Uvicorn from main.py using the "app" object
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
