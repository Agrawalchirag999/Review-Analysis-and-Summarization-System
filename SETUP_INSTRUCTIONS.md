# Setup Instructions for Review Analysis and Summarization System

## Prerequisites

### 1. Install Ollama
1. Download Ollama from: https://ollama.com/
2. Install Ollama for Windows
3. Open PowerShell and verify installation:
   ```powershell
   ollama --version
   ```

### 2. Pull DeepSeek Model
```powershell
ollama pull deepseek-llm:7b
```
This will download the DeepSeek 7B model (~4GB). Wait for it to complete.

### 3. Start Ollama Server
```powershell
ollama serve
```
Keep this terminal window open while using the application.

### 4. Get Oxylabs API Credentials
1. Sign up for free trial at: https://oxylabs.io/
2. Get your username and password from the dashboard
3. Note: Free trial has limited requests, so we've configured the scraper to use only 2 pages (~20 reviews)

## Configuration Steps

### 1. Update config.py
Open `config.py` and fill in your details:

```python
# Oxylabs Credentials
OXYLABS_USERNAME = "your_actual_username"  # Your Oxylabs username
OXYLABS_PASSWORD = "your_actual_password"  # Your Oxylabs password

# Adjust scraping limits for free trial
MAX_PAGES_TO_SCRAPE = 2  # Keep this low for free trial (2 pages = ~20 reviews)

# Ollama Configuration (usually no change needed)
OLLAMA_HOST = "localhost"  # Change only if Ollama is on different machine
OLLAMA_PORT = "11434"      # Default port

# Flask Configuration (usually no change needed)
FLASK_HOST = "127.0.0.1"   # Localhost
FLASK_PORT = 5000          # Default port
```

### 2. Install Python Dependencies
```powershell
pip install flask pandas numpy tensorflow tensorflow-text torch transformers textblob reportlab requests PyMuPDF joblib
```

### 3. Download NLTK Data (for TextBlob)
Run Python and execute:
```python
import nltk
nltk.download('brown')
nltk.download('punkt')
```

## Running the Application

### 1. Make sure Ollama is running:
```powershell
ollama serve
```

### 2. Start the Flask application:
```powershell
python app.py
```

### 3. Open your browser and go to:
```
http://127.0.0.1:5000
```

## Usage Tips for Free Trial API

Since you're using a free trial Oxylabs API:

1. **Limit scraping to 2 pages** (already configured in config.py)
2. **Test with one product first** before analyzing multiple products
3. **Monitor your API usage** in the Oxylabs dashboard
4. The system will scrape approximately 20 reviews per product (2 pages × 10 reviews/page)

## Troubleshooting

### Ollama Issues:
- **Error: "Connection refused"**
  - Make sure `ollama serve` is running
  - Check if port 11434 is available
  - Try: `ollama list` to see installed models

- **Model not found**
  - Pull the model: `ollama pull deepseek-llm:7b`

### Oxylabs API Issues:
- **401 Unauthorized**
  - Double-check your username and password in config.py
  - Verify credentials in Oxylabs dashboard

- **429 Too Many Requests**
  - You've exceeded your free trial limit
  - Wait or upgrade your plan

### General Issues:
- **Module not found errors**
  - Install missing packages: `pip install <package-name>`
  
- **Model loading errors**
  - Ensure the `model/` and `char_vectorizer_model/` folders are present
  - Check if all model files are intact

## Project Workflow

1. Enter Amazon product URL in the web interface
2. System extracts ASIN (product ID)
3. Scrapes reviews using Oxylabs API (limited to 2 pages)
4. Analyzes reviews for fake detection using ML model
5. Performs sentiment analysis on real reviews
6. Generates summary using DeepSeek via Ollama
7. Displays results with statistics

## File Structure
```
├── app.py                      # Main Flask application
├── config.py                   # Configuration file (YOUR CREDENTIALS HERE)
├── scripts/
│   ├── scraper.py             # Oxylabs scraper
│   ├── predict.py             # Fake review detection
│   └── summary.py             # Summary generation
├── data/                      # Generated data files
├── model/                     # Pre-trained ML model
└── templates/                 # HTML templates
```

## Important Notes

1. **Never commit config.py with real credentials** to version control
2. Keep Ollama server running while using the application
3. Monitor your Oxylabs API usage to avoid exceeding limits
4. The first run might be slower as models load into memory
5. PDF generation requires real reviews to be detected first
