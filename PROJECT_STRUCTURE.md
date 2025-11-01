# Project Structure - Updated

```
Review-Analysis-and-Summarization-System/
│
├── 📱 MAIN APPLICATION
│   ├── app.py                          # Flask web application (UPDATED)
│   └── config.py                       # Configuration file (NEW - ADD CREDENTIALS HERE!)
│
├── 🤖 ML MODELS & UTILITIES
│   ├── model/                          # Fake review detection model
│   │   ├── saved_model.pb
│   │   ├── variables/
│   │   └── assets/
│   ├── char_vectorizer_model/          # Character embedding model
│   │   ├── saved_model.pb
│   │   └── variables/
│   └── utils/                          # Preprocessing scalers
│       ├── scaler_polarity.pkl
│       ├── scaler_subjectivity.pkl
│       ├── scaler_burstiness.pkl
│       └── scaler_perplexity.pkl
│
├── 📜 SCRIPTS
│   ├── scraper.py                      # Amazon review scraper (UPDATED)
│   ├── predict.py                      # Fake review detection
│   └── summary.py                      # AI summarization (UPDATED)
│
├── 🌐 WEB INTERFACE
│   ├── templates/
│   │   └── index.html                  # Main web page
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css              # Styles
│   │   ├── js/
│   │   │   └── script.js              # Frontend logic
│   │   ├── animations/                # Lottie animations
│   │   │   ├── analyzing.json
│   │   │   ├── scraping.json
│   │   │   └── summarizing.json
│   │   └── images/                    # Screenshots
│
├── 📊 DATA (Generated at Runtime)
│   ├── input_reviews.csv              # Scraped reviews
│   ├── real_reviews.csv               # Filtered real reviews
│   ├── real_reviews.pdf               # PDF report
│   └── sentiment_stats.json           # Statistics
│
├── 📖 DOCUMENTATION (NEW)
│   ├── README.md                       # Original project README
│   ├── QUICK_START.md                 # 5-minute setup guide (NEW)
│   ├── SETUP_INSTRUCTIONS.md          # Detailed setup guide (NEW)
│   ├── CONFIG_README.md               # Configuration overview (NEW)
│   ├── CHANGES_SUMMARY.md             # What changed (NEW)
│   └── CHECKLIST.txt                  # Setup checklist (NEW)
│
├── ⚙️ CONFIGURATION (NEW)
│   ├── config.py                       # Active config (ADD YOUR CREDENTIALS!)
│   ├── config.template.py              # Template (safe to share) (NEW)
│   └── .gitignore                      # Prevent committing secrets (NEW)
│
├── 🔧 HELPER SCRIPTS (NEW)
│   ├── validate_config.py              # Validate your configuration (NEW)
│   ├── check_setup.bat                 # Windows: Check prerequisites (NEW)
│   └── start_app.bat                   # Windows: Start application (NEW)
│
├── 📦 DEPENDENCIES
│   └── requirements.txt                # Python packages (NEW)
│
└── 📄 OTHER
    └── LICENSE                         # Project license

```

## 🎯 Key Files to Know

### 🔴 MUST EDIT (Before Running):
1. **`config.py`** - Add your Oxylabs credentials here!

### 🟢 READY TO USE:
2. **`start_app.bat`** - Double-click to start the app
3. **`check_setup.bat`** - Verify everything is installed
4. **`validate_config.py`** - Check if config is correct

### 📘 READ FIRST:
5. **`QUICK_START.md`** - Get started in 5 minutes
6. **`CHECKLIST.txt`** - Step-by-step setup checklist
7. **`CHANGES_SUMMARY.md`** - See what was updated

## 📂 What's in Each Folder?

### `/model/` - Pre-trained ML Model
- TensorFlow saved model for fake review detection
- Uses BERT + custom embeddings
- **Don't modify** - pre-trained weights

### `/char_vectorizer_model/` - Character Embeddings
- Character-level text representations
- Part of the hybrid model
- **Don't modify** - pre-trained

### `/utils/` - Preprocessing Tools
- Scikit-learn scalers for features
- Normalizes polarity, subjectivity, etc.
- **Don't modify** - fitted to training data

### `/scripts/` - Core Processing
- **scraper.py**: Calls Oxylabs API, saves reviews
- **predict.py**: Detects fake reviews, sentiment analysis
- **summary.py**: Calls Ollama/DeepSeek for summarization

### `/templates/` & `/static/` - Web Interface
- HTML, CSS, JavaScript for the web UI
- Lottie animations for loading states
- **Can customize** if you want to change the look

### `/data/` - Generated Files
- Created when you run the analysis
- CSV files: review data
- PDF: formatted report
- JSON: statistics
- **Auto-generated** - don't create manually

## 🔄 Workflow Through the Files

```
User enters Amazon URL
        ↓
    app.py receives request
        ↓
    scraper.py fetches reviews (using config.py)
        ↓
    Saves to data/input_reviews.csv
        ↓
    predict.py loads reviews
        ↓
    Uses model/ and char_vectorizer_model/
        ↓
    Applies scalers from utils/
        ↓
    Classifies real vs fake
        ↓
    Saves to data/real_reviews.csv
        ↓
    Generates data/real_reviews.pdf
        ↓
    summary.py reads PDF
        ↓
    Calls Ollama (using config.py)
        ↓
    Returns summary to app.py
        ↓
    Saves stats to data/sentiment_stats.json
        ↓
    Display results in browser
```

## 🛠️ File Modification Guide

### ✅ Safe to Edit:
- `config.py` - Your settings
- `templates/index.html` - UI customization
- `static/css/style.css` - Styling
- `static/js/script.js` - Frontend behavior

### ⚠️ Edit Carefully:
- `app.py` - Main application logic
- `scripts/*.py` - Core processing scripts

### ❌ Don't Edit:
- `model/*` - Pre-trained weights
- `char_vectorizer_model/*` - Pre-trained weights
- `utils/*.pkl` - Fitted scalers
- `.gitignore` - Security protection

## 📝 Files by Purpose

### Configuration:
- `config.py` ← **YOU EDIT THIS**
- `config.template.py`
- `.gitignore`

### Documentation:
- `README.md`
- `QUICK_START.md`
- `SETUP_INSTRUCTIONS.md`
- `CONFIG_README.md`
- `CHANGES_SUMMARY.md`
- `CHECKLIST.txt`

### Application:
- `app.py`
- `scripts/scraper.py`
- `scripts/predict.py`
- `scripts/summary.py`

### Web Interface:
- `templates/index.html`
- `static/css/style.css`
- `static/js/script.js`
- `static/animations/*.json`

### Dependencies:
- `requirements.txt`

### Helpers:
- `validate_config.py`
- `check_setup.bat`
- `start_app.bat`

## 💾 Storage Requirements

- **Models**: ~500 MB (model/ + char_vectorizer_model/)
- **Dependencies**: ~2 GB (Python packages)
- **DeepSeek Model**: ~4 GB (Ollama)
- **Runtime Data**: ~1-5 MB (per analysis)

**Total**: ~7 GB disk space needed

## 🔒 Security Note

Files containing sensitive data (protected by .gitignore):
- ❌ `config.py` - Contains your API credentials
- ❌ `data/*.csv` - May contain user data
- ❌ `data/*.pdf` - Generated reports

Safe to share:
- ✅ All documentation files
- ✅ Source code (app.py, scripts/)
- ✅ `config.template.py`
- ✅ Web interface files

---

**Legend:**
- 📱 = Application
- 🤖 = Machine Learning
- 📜 = Scripts
- 🌐 = Web Interface
- 📊 = Data
- 📖 = Documentation
- ⚙️ = Configuration
- 🔧 = Utilities
- 📦 = Dependencies
