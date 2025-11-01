# 🔐 Configuration Guide - Updated for Easy Setup

## ✅ What Changed

Your project has been updated to use a centralized configuration system:

### New Files Created:
1. **`config.py`** - Main configuration file (add your credentials here)
2. **`config.template.py`** - Template for sharing without exposing credentials
3. **`SETUP_INSTRUCTIONS.md`** - Detailed setup guide
4. **`QUICK_START.md`** - Fast track setup (5 minutes)
5. **`requirements.txt`** - All Python dependencies
6. **`.gitignore`** - Prevents committing sensitive data
7. **`check_setup.bat`** - Windows script to verify setup
8. **`start_app.bat`** - Windows script to start the app easily

### Files Updated:
1. **`app.py`** - Now uses config.py for host, port, and session secret
2. **`scripts/scraper.py`** - Now uses config.py for Oxylabs credentials
3. **`scripts/summary.py`** - Now uses config.py for Ollama URL

## 🎯 Key Features for Free Trial

### Limited API Usage
The scraper is now configured to use only **2 pages** instead of 10:
- 2 pages = approximately 20 reviews
- Conserves your free trial API credits
- Still provides good analysis results

### Easy Configuration
All settings in one place (`config.py`):
```python
# Oxylabs API (your credentials)
OXYLABS_USERNAME = "your_username"
OXYLABS_PASSWORD = "your_password"

# Scraping limit (already optimized for free trial)
MAX_PAGES_TO_SCRAPE = 2

# Ollama settings (usually no change needed)
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"

# Flask settings (usually no change needed)
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
```

## 📋 Setup Checklist

### Before You Start:
- [ ] Python installed (3.8 or higher)
- [ ] Ollama downloaded from https://ollama.com/
- [ ] Oxylabs free trial account created

### Installation Steps:
1. [ ] Pull DeepSeek model: `ollama pull deepseek-llm:7b`
2. [ ] Install Python packages: `pip install -r requirements.txt`
3. [ ] Download NLTK data (see QUICK_START.md)
4. [ ] Update `config.py` with your Oxylabs credentials
5. [ ] Start Ollama: `ollama serve` (in separate terminal)
6. [ ] Run the app: `python app.py` or double-click `start_app.bat`
7. [ ] Open browser: http://127.0.0.1:5000

### Quick Verification:
Run `check_setup.bat` to verify all prerequisites are met!

## 🔒 Security Notes

### What NOT to Share:
- ❌ `config.py` (contains your credentials)
- ❌ Files in `data/` folder (contain scraped data)

### What IS Safe to Share:
- ✅ `config.template.py` (no credentials)
- ✅ All other project files
- ✅ `requirements.txt`

The `.gitignore` file is configured to prevent accidental commits of sensitive files.

## 🚀 Quick Commands

### Windows Users:
```powershell
# Check if everything is set up correctly
.\check_setup.bat

# Start the application
.\start_app.bat
```

### Manual Start:
```powershell
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Flask app
python app.py
```

## 💰 Free Trial Tips

Since you're using Oxylabs free trial:

1. **Monitor Usage**: Check your Oxylabs dashboard regularly
2. **Limited Scraping**: System is set to 2 pages (MAX_PAGES_TO_SCRAPE = 2)
3. **Test Smart**: Try with one product first before multiple analyses
4. **Review Count**: 2 pages typically gives you 15-20 reviews (enough for testing)

You can adjust `MAX_PAGES_TO_SCRAPE` in `config.py` if needed, but keep it low for free trial.

## 📊 What to Expect

### Per Analysis:
- Scrapes: ~20 reviews (2 pages)
- API Calls: 1 request to Oxylabs
- Processing Time: 
  - Scraping: 5-10 seconds
  - Fake Detection: 10-20 seconds
  - Summarization: 30-60 seconds (depends on Ollama/DeepSeek)
- Output: Summary, sentiment stats, real vs fake counts

### First Run:
- May take longer (models loading)
- Subsequent runs are faster

## 🛠️ Troubleshooting

### Issue: "Module 'config' not found"
**Solution**: Make sure `config.py` exists in the project root

### Issue: "401 Unauthorized" (Oxylabs)
**Solution**: Double-check credentials in `config.py`

### Issue: "Connection refused" (Ollama)
**Solution**: Start Ollama server: `ollama serve`

### Issue: "Model not found" (DeepSeek)
**Solution**: Pull the model: `ollama pull deepseek-llm:7b`

### Issue: Import errors
**Solution**: Install dependencies: `pip install -r requirements.txt`

## 📞 Need More Help?

- **Quick Start**: See `QUICK_START.md` for fast setup
- **Detailed Guide**: See `SETUP_INSTRUCTIONS.md` for comprehensive instructions
- **Check Setup**: Run `check_setup.bat` to diagnose issues

## 🎉 You're All Set!

Once configured, you can:
1. Run the app with `start_app.bat` or `python app.py`
2. Open http://127.0.0.1:5000 in your browser
3. Paste an Amazon product URL
4. Get AI-powered review analysis!

---

**Last Updated**: October 2025
**Optimized for**: Free Trial API Usage
