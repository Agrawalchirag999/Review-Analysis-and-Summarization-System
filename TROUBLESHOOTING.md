# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

## 🔴 Installation Issues

### Issue: "Python not recognized"
**Symptoms:** Command `python --version` fails
**Solutions:**
1. Install Python from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart terminal/command prompt
4. Alternative: Use `py --version` on Windows

---

### Issue: "Ollama not recognized"
**Symptoms:** Command `ollama --version` fails
**Solutions:**
1. Download from https://ollama.com/
2. Install for Windows
3. Restart terminal after installation
4. Check if `ollama.exe` is in `C:\Users\<YourName>\AppData\Local\Programs\Ollama\`

---

### Issue: "pip install fails with permission error"
**Symptoms:** Access denied during `pip install`
**Solutions:**
1. Run as administrator (right-click PowerShell → Run as administrator)
2. Or use: `pip install --user -r requirements.txt`
3. Or use virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

---

### Issue: "Can't install tensorflow"
**Symptoms:** TensorFlow installation fails
**Solutions:**
1. Check Python version: `python --version` (needs 3.8-3.11)
2. Use specific version: `pip install tensorflow==2.13.0`
3. For CPU-only: `pip install tensorflow-cpu`
4. May need Visual C++ Redistributable on Windows

---

## 🔴 Configuration Issues

### Issue: "Module 'config' not found"
**Symptoms:** `ImportError: No module named 'config'`
**Solutions:**
1. Make sure `config.py` exists in project root
2. If not, copy `config.template.py` to `config.py`
3. Fill in your credentials

---

### Issue: "Configuration validation fails"
**Symptoms:** `validate_config.py` shows errors
**Solutions:**
1. Open `config.py` in text editor
2. Replace ALL placeholder values:
   - `your_username_here` → your actual Oxylabs username
   - `your_password_here` → your actual Oxylabs password
3. Save file and run `python validate_config.py` again

---

### Issue: "Invalid credentials" or "401 Unauthorized"
**Symptoms:** Scraping fails with authentication error
**Solutions:**
1. Double-check username/password in `config.py`
2. Verify credentials work on Oxylabs dashboard
3. Check for extra spaces or quotes in config values
4. Ensure you're using correct quotes:
   ```python
   # Correct:
   OXYLABS_USERNAME = "myuser"
   
   # Wrong:
   OXYLABS_USERNAME = "myuser"  # (curly quotes)
   ```

---

## 🔴 Ollama Issues

### Issue: "Connection refused" to Ollama
**Symptoms:** Summary generation fails, connection error
**Solutions:**
1. Start Ollama server: `ollama serve`
2. Keep it running in separate terminal
3. Verify it's running: `curl http://localhost:11434/api/tags`
4. Check if port 11434 is available:
   ```powershell
   netstat -ano | findstr :11434
   ```

---

### Issue: "Model 'deepseek-llm:7b' not found"
**Symptoms:** Ollama can't find model
**Solutions:**
1. Pull the model: `ollama pull deepseek-llm:7b`
2. Wait for download to complete (~4GB)
3. Verify: `ollama list`
4. Should see `deepseek-llm:7b` in the list

---

### Issue: "Ollama server keeps stopping"
**Symptoms:** Server exits after a while
**Solutions:**
1. Check if another process is using port 11434
2. Try running with verbose logging: `ollama serve --verbose`
3. Check Windows Firewall settings
4. Try different port in `config.py`:
   ```python
   OLLAMA_PORT = "11435"  # Alternative port
   ```

---

## 🔴 API Issues

### Issue: "429 Too Many Requests" (Oxylabs)
**Symptoms:** Scraping fails after a few attempts
**Solutions:**
1. You've exceeded free trial limit
2. Wait for limit to reset (usually 24 hours)
3. Reduce `MAX_PAGES_TO_SCRAPE` in `config.py`:
   ```python
   MAX_PAGES_TO_SCRAPE = 1  # Only 1 page (~10 reviews)
   ```
4. Consider upgrading Oxylabs plan

---

### Issue: "No reviews found"
**Symptoms:** Scraper completes but 0 reviews
**Solutions:**
1. Check if ASIN is correct (10-character code)
2. Make sure product has reviews on Amazon.in
3. Try different product URL
4. Check if Oxylabs is blocking region/product

---

### Issue: "Invalid ASIN" error
**Symptoms:** Can't extract ASIN from URL
**Solutions:**
1. Use full Amazon URL format:
   - ✅ Good: `https://www.amazon.in/dp/B08L5TNJHG`
   - ✅ Good: `https://www.amazon.in/product-name/dp/B08L5TNJHG/`
   - ❌ Bad: `amzn.in/xyz` (shortened URL)
2. Copy URL directly from address bar
3. Make sure URL is for Amazon India (.in domain)

---

## 🔴 Runtime Issues

### Issue: "Model loading error"
**Symptoms:** Prediction fails, can't load model
**Solutions:**
1. Verify `model/` folder exists with:
   - `saved_model.pb`
   - `variables/` folder
2. Same for `char_vectorizer_model/`
3. Don't modify these folders
4. Re-download project if corrupted

---

### Issue: "Scaler file not found"
**Symptoms:** Error loading `.pkl` files
**Solutions:**
1. Check `utils/` folder contains:
   - `scaler_polarity.pkl`
   - `scaler_subjectivity.pkl`
   - `scaler_burstiness.pkl`
   - `scaler_perplexity.pkl`
2. Don't modify these files
3. Re-download if missing

---

### Issue: "CUDA/GPU errors"
**Symptoms:** TensorFlow GPU warnings/errors
**Solutions:**
1. These are usually safe to ignore
2. TensorFlow will fall back to CPU
3. To suppress warnings, add to top of scripts:
   ```python
   import os
   os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
   ```

---

### Issue: "Out of memory"
**Symptoms:** Process crashes during analysis
**Solutions:**
1. Close other applications
2. Reduce batch size in processing
3. Restart Python/system
4. Need at least 4GB RAM available

---

## 🔴 Web Interface Issues

### Issue: "Can't access http://127.0.0.1:5000"
**Symptoms:** Browser can't connect
**Solutions:**
1. Make sure Flask app is running: `python app.py`
2. Check console for errors
3. Try: `http://localhost:5000` instead
4. Check if port 5000 is already in use:
   ```powershell
   netstat -ano | findstr :5000
   ```
5. Change port in `config.py`:
   ```python
   FLASK_PORT = 5001  # Alternative port
   ```

---

### Issue: "Analysis stuck/not progressing"
**Symptoms:** UI shows loading forever
**Solutions:**
1. Check Flask console for errors
2. Check if Ollama is running
3. Verify all steps in checklist complete
4. Check browser console (F12) for JavaScript errors
5. Try refreshing page

---

### Issue: "Results not displaying"
**Symptoms:** Analysis completes but no results shown
**Solutions:**
1. Check if files were created in `data/` folder:
   - `input_reviews.csv`
   - `real_reviews.csv`
   - `real_reviews.pdf`
   - `sentiment_stats.json`
2. Check Flask console for errors
3. Verify file permissions (can read/write to `data/`)

---

## 🔴 NLTK Issues

### Issue: "NLTK data not found"
**Symptoms:** TextBlob errors, missing corpus
**Solutions:**
1. Download required data:
   ```python
   import nltk
   nltk.download('brown')
   nltk.download('punkt')
   ```
2. Or download all: `nltk.download('all')`
3. Default location: `C:\Users\<YourName>\AppData\Roaming\nltk_data`

---

## 🔴 Windows-Specific Issues

### Issue: "Script execution disabled" (PowerShell)
**Symptoms:** Can't run `.bat` files or activate venv
**Solutions:**
1. Run PowerShell as Administrator
2. Run: `Set-ExecutionPolicy RemoteSigned`
3. Confirm with 'Y'
4. Or right-click `.bat` file → Run as administrator

---

### Issue: "Path too long"
**Symptoms:** File operation errors on Windows
**Solutions:**
1. Move project to shorter path:
   - ❌ Bad: `C:\Users\chira\OneDrive\Desktop\SEM 7\NLP\Review-Analysis-and-Summarization-System-main`
   - ✅ Good: `C:\Projects\ReviewAnalysis`
2. Or enable long paths in Windows:
   - Run: `reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f`
   - Restart system

---

## 📊 Diagnostic Commands

Run these to gather information:

```powershell
# Check Python
python --version
pip list

# Check Ollama
ollama --version
ollama list

# Check ports in use
netstat -ano | findstr :5000
netstat -ano | findstr :11434

# Validate configuration
python validate_config.py

# Check setup
.\check_setup.bat

# Test Ollama
curl http://localhost:11434/api/tags

# Check if files exist
dir model\saved_model.pb
dir char_vectorizer_model\saved_model.pb
dir utils\*.pkl
```

---

## 🆘 Still Having Issues?

1. **Re-read documentation:**
   - `QUICK_START.md` - Setup steps
   - `SETUP_INSTRUCTIONS.md` - Detailed guide
   - `CHECKLIST.txt` - Verify each step

2. **Check logs:**
   - Flask console output
   - `ollama serve` output
   - Browser console (F12)

3. **Verify prerequisites:**
   - Run `check_setup.bat`
   - Run `python validate_config.py`

4. **Try fresh start:**
   - Close all terminals
   - Restart Ollama: `ollama serve`
   - Restart Flask: `python app.py`

5. **Test components individually:**
   ```powershell
   # Test scraper only
   python scripts/scraper.py B08L5TNJHG
   
   # Test prediction only (after scraping)
   python scripts/predict.py
   
   # Test Ollama
   ollama run deepseek-llm:7b "Hello"
   ```

---

## 📞 Getting Help

When reporting issues, include:
1. Operating System and version
2. Python version: `python --version`
3. Error message (full text)
4. What you were trying to do
5. Output of `python validate_config.py`
6. Flask console output
7. Whether Ollama is running

---

**Most Common Fixes:**
- ✅ Start Ollama: `ollama serve`
- ✅ Update config.py with real credentials
- ✅ Install all requirements: `pip install -r requirements.txt`
- ✅ Pull DeepSeek model: `ollama pull deepseek-llm:7b`
- ✅ Check file permissions in `data/` folder
