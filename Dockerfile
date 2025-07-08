# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install code-server
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://code-server.dev/install.sh | sh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose code-server port
EXPOSE 8080

# Set up code-server (no password, bind to all interfaces for demo)
ENV PASSWORD="Password1"
CMD ["code-server", "--bind-addr", "0.0.0.0:8080", "."]
