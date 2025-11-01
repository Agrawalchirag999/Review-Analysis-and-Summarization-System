# 🎬 Getting Started - Your First Analysis

## Welcome! 👋

This guide will walk you through running your first review analysis from start to finish.

---

## ⏱️ Time Required: 10-15 minutes

---

## 📍 Step 1: Verify Prerequisites (2 minutes)

Open PowerShell in your project folder and run:

```powershell
.\check_setup.bat
```

✅ **If all checks pass**, continue to Step 2  
❌ **If checks fail**, see SETUP_INSTRUCTIONS.md

---

## 📍 Step 2: Configure Your Credentials (1 minute)

1. Open `config.py` in any text editor (Notepad, VS Code, etc.)

2. Find these lines:
   ```python
   OXYLABS_USERNAME = "your_username_here"
   OXYLABS_PASSWORD = "your_password_here"
   ```

3. Replace with your actual Oxylabs credentials:
   ```python
   OXYLABS_USERNAME = "john_doe"
   OXYLABS_PASSWORD = "SecurePass123"
   ```

4. Save the file (Ctrl+S)

5. Validate your configuration:
   ```powershell
   python validate_config.py
   ```

✅ **Should show**: "Configuration looks good!"

---

## 📍 Step 3: Start Ollama Server (30 seconds)

Open a **new** PowerShell window and run:

```powershell
ollama serve
```

**Keep this window open!** Don't close it.

You should see:
```
Ollama is running
...
```

---

## 📍 Step 4: Start the Application (30 seconds)

In your **original** PowerShell window (not the Ollama one), run:

```powershell
python app.py
```

Or simply double-click: `start_app.bat`

You should see:
```
* Running on http://127.0.0.1:5000
* Do not shut down the server
```

**Keep this window open too!**

---

## 📍 Step 5: Open the Web Interface (10 seconds)

1. Open your web browser (Chrome, Edge, Firefox, etc.)

2. Go to: **http://127.0.0.1:5000**

3. You should see the Review Analysis System interface

---

## 📍 Step 6: Find an Amazon Product (1 minute)

1. Go to **Amazon India** (amazon.in)

2. Search for any product with reviews (e.g., "wireless earbuds")

3. Open a product page

4. Copy the URL from your address bar

Example URLs that work:
- `https://www.amazon.in/dp/B08L5TNJHG`
- `https://www.amazon.in/Some-Product-Name/dp/B08L5TNJHG/ref=xyz`

---

## 📍 Step 7: Run Your First Analysis (2-3 minutes)

### A. Enter URL

1. Paste the Amazon URL in the text box

2. Click **"Analyze Reviews"**

3. Wait for "ASIN extracted" message

### B. Scraping Phase (~10 seconds)

You'll see an animation and:
- "Scraping reviews..."
- Progress indicator

**What's happening:**
- System connects to Oxylabs API
- Fetches ~20 reviews (2 pages)
- Saves to `data/input_reviews.csv`

### C. Analysis Phase (~30 seconds)

You'll see:
- "Analyzing reviews..."
- Progress indicator

**What's happening:**
- Loading ML models
- Detecting fake reviews
- Performing sentiment analysis
- Generating real_reviews.csv and PDF

### D. Summarization Phase (~60 seconds)

You'll see:
- "Generating summary..."
- Progress indicator

**What's happening:**
- DeepSeek AI reads reviews
- Generates comprehensive summary
- Extracts pros and cons

### E. Results! 🎉

You'll see:
- **Summary**: AI-generated overview of reviews
- **Statistics**:
  - Total reviews analyzed
  - Real vs Fake count
  - Sentiment breakdown (Positive/Neutral/Negative)
  - Percentages

---

## 📍 Step 8: Explore the Results

### View Files Generated

Open the `data/` folder to see:

1. **input_reviews.csv**
   - Raw scraped reviews
   - Open in Excel or Notepad

2. **real_reviews.csv**
   - Only real reviews with sentiment
   - Can be used for further analysis

3. **real_reviews.pdf**
   - Formatted report of real reviews
   - Open with any PDF reader

4. **sentiment_stats.json**
   - Statistics in JSON format
   - Can be used by other tools

---

## 📍 Step 9: Try Another Product (Optional)

Want to analyze another product?

1. Find another Amazon URL
2. Paste in the interface
3. Click "Analyze Reviews" again
4. Previous results will be overwritten

---

## 🎯 Understanding Your Results

### Summary Section
The AI-generated summary includes:
- Overall sentiment (positive, negative, neutral)
- Common themes in reviews
- Product strengths (pros)
- Product weaknesses (cons)
- Recurring issues or praises

### Statistics Section

**Total Reviews**: How many reviews were scraped  
**Real Reviews**: Reviews that passed fake detection  
**Fake Reviews**: Reviews flagged as potentially fake

**Sentiment Breakdown**:
- 🟢 **Positive**: Happy customers, good experiences
- 🟡 **Neutral**: Mixed or factual reviews
- 🔴 **Negative**: Unhappy customers, issues reported

---

## 💡 Tips for Best Results

### 1. Choose Products With Many Reviews
- More reviews = better analysis
- Minimum 10 reviews recommended
- Popular products work best

### 2. Monitor API Usage
- Check Oxylabs dashboard
- Free trial has limited credits
- 1 analysis = 1 API request
- 2 pages per request (configured)

### 3. Be Patient
- First run may be slower (models loading)
- Summary takes time (AI processing)
- Don't refresh page while processing

### 4. Check Logs for Issues
- Flask console shows errors
- Ollama window shows AI processing
- Browser console (F12) for frontend issues

---

## 🔄 Typical Workflow

```
Find Product → Copy URL → Paste in App
                    ↓
              Click Analyze
                    ↓
        Wait for Scraping (~10s)
                    ↓
        Wait for Analysis (~30s)
                    ↓
      Wait for Summarization (~60s)
                    ↓
             View Results! 🎉
                    ↓
     Download/Save if needed
                    ↓
        Try Another Product?
```

---

## ⏹️ Stopping the Application

When you're done:

1. **Close browser** or tab

2. **Stop Flask app**:
   - Go to PowerShell running `python app.py`
   - Press `Ctrl+C`
   - Type `Y` if asked

3. **Stop Ollama server**:
   - Go to PowerShell running `ollama serve`
   - Press `Ctrl+C`

4. **Close PowerShell windows**

---

## 🎊 Congratulations!

You've successfully:
- ✅ Set up the Review Analysis System
- ✅ Configured your credentials
- ✅ Ran your first analysis
- ✅ Generated AI-powered insights

### What You Can Do Now:
- Analyze any Amazon India product
- Compare different products
- Use results for research
- Export data for presentations
- Share insights with others

---

## 📊 Sample Expected Results

For a typical product with 20 reviews, you might see:

```
Total Reviews: 20
Real Reviews: 16 (80%)
Fake Reviews: 4 (20%)

Sentiment:
├── Positive: 10 (62.5%)
├── Neutral: 4 (25%)
└── Negative: 2 (12.5%)

Summary:
"Based on the reviews, customers generally appreciate the 
product's build quality and performance. The main pros 
include long battery life, good sound quality, and 
comfortable fit. However, some users reported connectivity 
issues and occasional lag. The price point is considered 
reasonable for the features offered..."
```

---

## 🆘 Something Not Working?

1. **Check TROUBLESHOOTING.md** - Common issues and fixes
2. **Re-run check_setup.bat** - Verify prerequisites
3. **Check both PowerShell windows** - Look for error messages
4. **Verify Ollama is running** - Should show in task manager
5. **Test individual components** - See if scraping works alone

---

## 📚 Next Steps

Now that you know the basics:
- Read **SETUP_INSTRUCTIONS.md** for advanced configuration
- Read **PROJECT_STRUCTURE.md** to understand the code
- Read **TROUBLESHOOTING.md** if you encounter issues
- Experiment with different products and categories

---

## 💬 Need Help?

Include this information when asking for help:
- What step you're on
- What you expected to happen
- What actually happened
- Error messages (copy exact text)
- Screenshots if possible

---

**Happy Analyzing! 🚀**

Remember: This tool helps you make informed decisions by filtering fake reviews and understanding genuine customer sentiment.
