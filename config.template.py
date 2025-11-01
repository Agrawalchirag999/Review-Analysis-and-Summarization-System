# Configuration Template for Review Analysis and Summarization System
# Copy this file to 'config.py' and fill in your actual credentials

# ==================================================
# OXYLABS API CONFIGURATION
# ==================================================
# Get your credentials from: https://oxylabs.io/
OXYLABS_USERNAME = "your_username_here"  # Replace with your Oxylabs username
OXYLABS_PASSWORD = "your_password_here"  # Replace with your Oxylabs password
OXYLABS_API_URL = "https://realtime.oxylabs.io/v1/queries"

# ==================================================
# API USAGE LIMITS (FOR FREE TRIAL)
# ==================================================
# Limit the number of pages to scrape (1 page = ~10 reviews)
# Free trial typically allows limited requests
MAX_PAGES_TO_SCRAPE = 2  # Reduced from 10 to 2 for free trial (will get ~20 reviews)

# ==================================================
# OLLAMA CONFIGURATION
# ==================================================
# Ollama server URL (default is localhost:11434)
# Make sure Ollama is running: ollama serve
OLLAMA_HOST = "localhost"  # Change if running on different machine
OLLAMA_PORT = "11434"      # Default Ollama port
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
OLLAMA_MODEL = "deepseek-llm:7b"  # Model name (must be pulled first)

# ==================================================
# FLASK SERVER CONFIGURATION
# ==================================================
FLASK_HOST = "127.0.0.1"  # Use 127.0.0.1 for local development
FLASK_PORT = 5000         # Default Flask port
FLASK_DEBUG = True        # Set to False in production

# ==================================================
# SESSION SECRET
# ==================================================
# Change this to a random string for security
SESSION_SECRET = "your-secret-key-here-change-this-in-production"
