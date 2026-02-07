FROM python:3.12-slim

# Install Node.js (needed for MCP servers via npx)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY mcp-config.json .

# Create data and log directories
RUN mkdir -p data logs

VOLUME ["/app/data", "/app/logs"]

CMD ["python", "-m", "src.main"]
