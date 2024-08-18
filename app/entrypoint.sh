#!/bin/sh

# Step 1: Check if the API_KEY is set
if [ -z "$API_KEY" ]; then
    echo "Error: API_KEY is not set."
    exit 1
fi

# Obfuscate and print the API_KEY to confirm it's set
echo "API_KEY: ${API_KEY:0:2}******"

# Step 2: Create the .env file dynamically
echo "Creating .env file..."
cat <<EOF > /app/.config
API_KEY=${API_KEY}
LOG_LEVEL=${LOG_LEVEL}
EOF

# Step 3: Run the FastAPI application
echo "Starting FastAPI application..."
exec poetry run uvicorn alpha_api.main:app --host 0.0.0.0 --port 8000