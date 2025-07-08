# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install code-server (for development, optional)
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://code-server.dev/install.sh | sh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose code-server port (optional)
EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["game"]
