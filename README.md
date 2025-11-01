# Review Analysis and Summarization System

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

AI-powered system for detecting fake reviews, analyzing sentiment, and generating intelligent summaries from Walmart product reviews.

## 🌟 Features

### ✅ Real Review Extraction
- **Web Scraping**: Extracts reviews from Walmart products using Oxylabs API
- **JSON-LD Parsing**: Intelligently parses structured data from modern e-commerce sites
- **Multiple Products**: Supports analysis of any Walmart product URL

### ✅ Fake Review Detection
- **ML Model**: Logistic Regression classifier with 91.3% accuracy
- **TF-IDF Vectorization**: Uses bi-gram features (500 dimensions)
- **Confidence Scores**: Provides prediction confidence for each review
- **Trained on 10,000+ Amazon reviews**

### ✅ Sentiment Analysis
- **Polarity Detection**: Classifies reviews as Positive, Neutral, or Negative
- **TextBlob Integration**: Advanced sentiment scoring
- **Visual Analytics**: Pie charts and statistics

### ✅ Custom Summarization
- **TF-IDF-Based**: Extractive summarization using keyword extraction
- **Aspect Analysis**: Automatically detects mentions of quality, price, delivery, performance, design, features, and customer service
- **Representative Reviews**: Selects best examples for each sentiment
- **Structured Output**: Clean, organized summaries with HTML formatting

### ✅ Web Interface
- **Modern UI**: Bootstrap-based responsive design
- **Real-time Processing**: Background job processing with status updates
- **Individual Review Display**: Shows rating, sentiment, and confidence for each review
- **Animated Progress**: Visual feedback during scraping, analysis, and summarization

## 📸 Screenshots

![Analysis Interface](static/images/screenshot1.png)
*Main analysis interface*

![Results Display](static/images/screenshot2.png)
*Results with sentiment analysis and summary*

![Individual Reviews](static/images/screenshot3.png)
*Individual review cards with ratings and confidence*
<img width="1082" height="895" alt="image" src="https://github.com/user-attachments/assets/9028043e-66f7-4297-a73e-9f47631ea718" />


## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Oxylabs API account (for web scraping)
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Review-Analysis-and-Summarization-System.git
cd Review-Analysis-and-Summarization-System-main
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure credentials**

Create a `config.py` file in the root directory:

```python
# Oxylabs API Configuration
OXYLABS_USERNAME = "your_username_here"
OXYLABS_PASSWORD = "your_password_here"

# Ollama Configuration (optional - fallback summarization)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"

# Flask Configuration
SESSION_SECRET = "your-secret-key-here"
DEBUG = True
```

4. **Download the ML model**

Place your trained model file in:
```
snlp/saved_models/fake_review_detector_20251031_224832_complete_package.pkl
```

Or train your own using the training script in `snlp/`.

5. **Run the application**
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## 📁 Project Structure

```
Review-Analysis-and-Summarization-System-main/
├── app.py                          # Flask web application
├── config.py                       # Configuration (API keys, credentials)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── CUSTOM_SUMMARIZER_README.md    # Custom summarizer documentation
│
├── scripts/
│   ├── scraper.py                 # Web scraping with Oxylabs + JSON-LD parsing
│   ├── predict.py                 # Fake review detection with ML
│   ├── summary.py                 # Summary generation (orchestrator)
│   └── custom_summarizer.py       # Custom TF-IDF-based summarization
│
├── snlp/
│   └── saved_models/              # ML model files (.pkl)
│
├── data/
│   ├── input_reviews.csv          # Scraped reviews (generated)
│   ├── real_reviews.csv           # Filtered real reviews (generated)
│   ├── real_reviews.pdf           # PDF report (generated)
│   ├── sentiment_stats.json       # Statistics (generated)
│   └── custom_summary.txt         # Text summary (generated)
│
├── templates/
│   └── index.html                 # Web interface template
│
└── static/
    ├── css/
    │   └── style.css              # Custom styles
    ├── js/
    │   └── script.js              # Frontend logic
    ├── images/                    # UI images
    └── animations/                # Lottie animations
```

## 🔧 Usage

### Web Interface

1. **Enter Walmart Product URL**
   - Paste any Walmart product URL
   - Example: `https://www.walmart.com/ip/Product-Name/12345678`

2. **Click Analyze**
   - System will scrape reviews
   - Detect fake reviews
   - Generate summary
   - Display results with sentiment analysis

3. **View Results**
   - Summary with key insights
   - Sentiment breakdown (pie chart)
   - Individual reviews with ratings, sentiment, and confidence scores

### Command Line

**Scrape reviews:**
```bash
python scripts/scraper.py "https://www.walmart.com/ip/Product/12345"
```

**Analyze reviews:**
```bash
python scripts/predict.py
```

**Generate summary:**
```bash
python scripts/summary.py
```

**Custom summarizer (standalone):**
```bash
python scripts/custom_summarizer.py
```

## 🧠 How It Works

### 1. Web Scraping
- Fetches HTML from product page using Oxylabs Universal API
- Parses JSON-LD structured data (`<script type="application/ld+json">`)
- Extracts review text, ratings, author names from Product schema
- Saves to `data/input_reviews.csv`

### 2. Fake Review Detection
- Loads pre-trained Logistic Regression model
- Cleans text (lowercase, special char removal, whitespace normalization)
- Extracts features (exclamation/question marks, word/char counts, uppercase ratio)
- TF-IDF vectorization with bi-grams
- Predicts fake/real with confidence scores
- Saves real reviews to `data/real_reviews.csv` and generates PDF

### 3. Sentiment Analysis
- Uses TextBlob for polarity scoring
- Classifies as Positive (>0.1), Neutral (-0.1 to 0.1), Negative (<-0.1)
- Calculates statistics and saves to `data/sentiment_stats.json`

### 4. Summary Generation
- **Priority 1**: Custom TF-IDF summarizer (default)
  - Extracts key phrases using TF-IDF vectorization
  - Detects aspect mentions (quality, price, delivery, etc.)
  - Selects representative reviews for each sentiment
  - Generates structured HTML summary
- **Priority 2**: Ollama LLM (fallback if custom fails)
- **Priority 3**: Simple rule-based summarization (ultimate fallback)

## 📊 Model Performance

**Fake Review Detector:**
- Model: Logistic Regression
- Features: TF-IDF (bi-grams) + hand-crafted features
- Accuracy: 91.3%
- Training Data: 10,000 Amazon reviews
- Vector Dimensions: 500

## 🛠️ Technologies Used

### Backend
- **Flask**: Web framework
- **scikit-learn**: ML model and TF-IDF vectorization
- **pandas**: Data manipulation
- **NumPy**: Numerical operations
- **TextBlob**: Sentiment analysis
- **PyMuPDF (fitz)**: PDF generation
- **BeautifulSoup4**: HTML parsing
- **requests**: HTTP requests

### Frontend
- **Bootstrap 5**: UI framework
- **Chart.js**: Data visualization
- **Lottie**: Animations
- **Font Awesome**: Icons

### APIs
- **Oxylabs**: Web scraping API
- **Ollama**: LLM API (optional)

## ⚙️ Configuration

### Oxylabs Setup
1. Sign up at [Oxylabs](https://oxylabs.io/)
2. Get your API credentials
3. Add to `config.py`:
```python
OXYLABS_USERNAME = "your_username"
OXYLABS_PASSWORD = "your_password"
```

### Ollama Setup (Optional)
1. Install [Ollama](https://ollama.com/)
2. Pull a model: `ollama pull llama3.2:1b`
3. Start Ollama service
4. Update `config.py` with Ollama URL

## 📝 API Endpoints

- `GET /` - Main interface
- `POST /analyze` - Validate product URL
- `POST /scrape` - Scrape reviews
- `POST /predict` - Run fake detection
- `GET /predict_status/<job_id>` - Check prediction status
- `POST /summarize` - Generate summary
- `GET /summarize_status/<job_id>` - Check summary status
- `GET /reviews` - Get analyzed reviews (JSON)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

CHIRAG AGRAWAL - J016
JEET SHOREY - J024
KHUSH GADA - J029

## 🙏 Acknowledgments

- Oxylabs for web scraping API
- scikit-learn for ML tools
- TextBlob for sentiment analysis
- Bootstrap for UI components
- Ollama for LLM integration (optional)

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🔮 Future Enhancements

- [ ] Support for more e-commerce sites (Amazon, Flipkart, etc.)
- [ ] Advanced NLP models (BERT, transformers)
- [ ] Real-time review monitoring
- [ ] Comparative product analysis
- [ ] Review trend tracking over time
- [ ] Multi-language support
- [ ] Export results in multiple formats
- [ ] API for programmatic access

---

**Note**: Make sure to keep your `config.py` file secure and never commit it to version control. The `.gitignore` file is already configured to exclude it.
