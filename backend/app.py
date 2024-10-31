import logging
import sys
import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (Restrict origins in production)
CORS(app, resources={r"/*": {"origins": "*"}})

# vLLM server configuration
VLLM_SERVER_URL = "http://localhost:8000/v1/completions"  # Adjust if vllm is running on a different host/port
API_KEY = "token-what-a-day"  # Ensure this matches your vllm server's API key

# ===========================
# Generate Endpoint
# ===========================

@app.route('/api/generate', methods=['POST'])
def generate_response():
    """
    Endpoint to generate text based on a given prompt.
    Expects JSON payload with 'prompt' and optional 'max_tokens'.
    """
    logger.info("Received request to /api/generate")

    data = request.get_json()
    prompt = data.get("prompt", "")
    max_tokens = data.get("max_tokens", 1000)  # Default to 1000 tokens if not provided

    logger.info(f"Prompt received: {prompt}")
    logger.info(f"Max tokens requested: {max_tokens}")

    if not prompt:
        logger.warning("No prompt provided in the request.")
        return make_response(jsonify({"error": "No prompt provided."}), 400)

    try:
        # Define the payload for vllm server
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }

        # Send request to vllm server
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        response = requests.post(VLLM_SERVER_URL, json=payload, headers=headers)

        if response.status_code == 200:
            generated_text = response.json().get("generated_text", "")
            logger.info(f"Generated response: {generated_text}")
            return jsonify({"generated_text": generated_text})
        else:
            logger.error(f"vLLM server error: {response.text}")
            return make_response(jsonify({"error": "vLLM server error."}), 500)

    except Exception as e:
        logger.error(f"Error communicating with vLLM server: {e}")
        return make_response(jsonify({"error": "Error generating response."}), 500)

# ===========================
# Root Endpoint
# ===========================

@app.route('/', methods=['GET'])
def root():
    """
    Root endpoint to verify that the API is running.
    """
    return jsonify({"message": "Welcome to the vLLM Flask API server!"})

# ===========================
# Run the Flask App
# ===========================

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

