# Quick Start Guide - Review Analysis and Summarization System

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Ollama
1. Download and install from: https://ollama.com/
2. Open PowerShell and pull the model:
   ```powershell
   ollama pull deepseek-llm:7b
   ```
3. Start Ollama server (keep it running):
   ```powershell
   ollama serve
   ```

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Download NLTK Data
Open Python and run:
```python
import nltk
nltk.download('brown')
nltk.download('punkt')
```

### Step 4: Configure API Credentials
1. Open `config.py` in a text editor
2. Add your Oxylabs credentials:
   ```python
   OXYLABS_USERNAME = "your_actual_username"
   OXYLABS_PASSWORD = "your_actual_password"
   ```
3. Save the file

### Step 5: Run the Application
```powershell
python app.py
```

### Step 6: Open Browser
Go to: http://127.0.0.1:5000

## 📝 How to Use

1. **Find an Amazon product URL**
   - Example: https://www.amazon.in/dp/B08L5TNJHG
   
2. **Paste the URL** in the web interface

3. **Click "Analyze Reviews"**
   - The system will scrape ~20 reviews (2 pages - optimized for free trial)
   - Detect fake reviews using ML
   - Analyze sentiment of real reviews
   - Generate summary using AI

4. **View Results**
   - Total reviews analyzed
   - Real vs Fake review count
   - Sentiment breakdown (Positive/Neutral/Negative)
   - AI-generated summary

## ⚠️ Important Notes

- **Free Trial Limitation**: Set to scrape only 2 pages (~20 reviews) to conserve API credits
- **Keep Ollama Running**: The `ollama serve` command must be running in a separate terminal
- **First Run**: May take longer as models load into memory
- **API Credits**: Monitor your Oxylabs dashboard to track usage

## 🔧 Troubleshooting

**"Connection refused" error**
- Make sure Ollama is running: `ollama serve`

**"401 Unauthorized" error**
- Check your credentials in `config.py`

**"Module not found" error**
- Install requirements: `pip install -r requirements.txt`

**"Model not found" error**
- Pull the model: `ollama pull deepseek-llm:7b`

## 📊 What Gets Generated

After analysis, you'll find these files in the `data/` folder:
- `input_reviews.csv` - Raw scraped reviews
- `real_reviews.csv` - Filtered real reviews with sentiment
- `real_reviews.pdf` - PDF of real reviews
- `sentiment_stats.json` - Statistics and counts

## 💡 Tips

1. Test with a popular product (more reviews = better analysis)
2. Start with 2 pages for testing (already configured)
3. Monitor your Oxylabs API usage in their dashboard
4. If summary generation is slow, it's normal - DeepSeek is processing

## 📞 Need Help?

Check the detailed SETUP_INSTRUCTIONS.md file for more information.
