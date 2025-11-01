"""
Configuration Template
Copy this file to config.py and fill in your actual credentials
DO NOT commit config.py to version control
"""

# ============================================================================
# OXYLABS WEB SCRAPER API CONFIGURATION
# ============================================================================
# Sign up at https://oxylabs.io/ to get your credentials
OXYLABS_USERNAME = "your_oxylabs_username_here"
OXYLABS_PASSWORD = "your_oxylabs_password_here"

# ============================================================================
# OLLAMA LLM CONFIGURATION (OPTIONAL)
# ============================================================================
# Ollama is used as a fallback summarization method
# Install from https://ollama.com/ and pull a model like:
# ollama pull llama3.2:1b
# If you don't want to use Ollama, the system will use custom summarizer
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"  # or "deepseek-llm:7b", "llama3.2:3b", etc.

# ============================================================================
# FLASK APPLICATION CONFIGURATION
# ============================================================================
# Generate a secure secret key using: python -c "import secrets; print(secrets.token_hex(32))"
SESSION_SECRET = "change-this-to-a-random-secret-key"

# Debug mode (set to False in production)
DEBUG = True

# Server configuration
HOST = "127.0.0.1"
PORT = 5000
