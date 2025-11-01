# Custom Review Summarization System

## Overview
This project now includes a **custom-built summarization model** (`custom_summarizer.py`) that provides intelligent, structured summaries of product reviews without relying on external LLM APIs like Ollama.

## Features

### ✅ Current Implementation (Production-Ready)

1. **TF-IDF Based Extractive Summarization**
   - Uses sklearn's TfidfVectorizer to identify important keywords and phrases
   - Extracts key themes from reviews (e.g., "easy to use", "great gift", "creative")
   - Works with n-grams (unigrams to trigrams)

2. **Aspect-Based Analysis**
   - Automatically detects and counts mentions of key aspects:
     - Quality (durable, build, material)
     - Price (cost, value, affordable)
     - Delivery (shipping, packaging)
     - Performance (works, efficient, speed)
     - Features (functionality, options)
     - Design (look, appearance, style)
     - Customer Service (support, help)

3. **Sentiment Distribution Analysis**
   - Breaks down reviews by sentiment (positive/neutral/negative)
   - Calculates percentages for each sentiment category
   - Uses confidence scores from the ML model

4. **Representative Review Extraction**
   - Selects the most representative reviews for each sentiment
   - Prioritizes reviews with highest confidence scores
   - Displays sample positive and negative reviews with ratings

5. **Comprehensive Summary Generation**
   - Overall statistics (total reviews, average rating)
   - Sentiment breakdown with percentages
   - Most discussed aspects
   - Key themes and phrases
   - Sample reviews from different sentiments
   - Smart conclusion based on overall sentiment

## Usage

### Standalone Execution
```bash
python scripts/custom_summarizer.py
```

### Integration with Main System
The custom summarizer is automatically integrated into `summary.py` with a priority system:

1. **Priority 1**: Custom Summarizer (uses structured CSV data)
2. **Priority 2**: Ollama LLM (if available)
3. **Priority 3**: Simple fallback summarization

To use in your code:
```python
from scripts.custom_summarizer import CustomSummarizer

summarizer = CustomSummarizer()
summarizer.load_reviews_from_csv("data/real_reviews.csv")
summary = summarizer.generate_summary()
print(summary)
```

## Example Output

```
**Summary of 10 Customer Reviews**
Average Rating: 4.7/5 stars

**Sentiment Breakdown:**
- Positive: 9 reviews (90.0%)
- Neutral: 1 reviews (10.0%)
- Negative: 0 reviews (0.0%)

**Most Discussed Aspects:**
- Design: mentioned 7 times
- Price: mentioned 6 times
- Delivery: mentioned 2 times
- Performance: mentioned 2 times
- Customer Service: mentioned 2 times

**Key Themes:** use, easy, like, loved, creative, great, gift, just

**Sample Positive Review:**
"Easy to clean creative craft. Very creative craft that is easy to clean..." - 5⭐

**Conclusion:** Overall, customers are highly satisfied with this product.
```

## Architecture

### Class: `CustomSummarizer`

#### Methods:
- `load_reviews_from_csv(csv_path)`: Load reviews from structured CSV
- `load_reviews_from_pdf(pdf_path)`: Fallback to extract from PDF
- `extract_key_phrases(reviews, top_n)`: TF-IDF based keyword extraction
- `extract_aspects(reviews)`: Detect aspect mentions
- `analyze_sentiment_distribution()`: Calculate sentiment statistics
- `extract_representative_reviews(n)`: Select best examples
- `generate_summary()`: Create comprehensive summary

## Dependencies

### Required:
- `pandas`: Data manipulation
- `PyMuPDF (fitz)`: PDF processing
- `numpy`: Numerical operations

### Optional (Enhanced Features):
- `scikit-learn`: TF-IDF vectorization and advanced text processing
- `textblob`: Enhanced sentiment analysis (currently not used, reserved for future)

## Future Enhancements

### 🔄 Planned Features (Not Yet Implemented)

1. **Advanced NLP Models**
   - Integrate transformer-based models (BERT, RoBERTa)
   - Fine-tune on review data for better understanding
   - Use sentence transformers for semantic similarity

2. **Abstractive Summarization**
   - Train a sequence-to-sequence model (T5, BART)
   - Generate human-like summaries instead of extractive
   - Use pre-trained models like `facebook/bart-large-cnn`

3. **Multi-Document Summarization**
   - Implement clustering of similar reviews
   - Generate hierarchical summaries
   - Handle very large review datasets (>1000 reviews)

4. **Aspect-Based Sentiment Analysis**
   - Determine sentiment for each specific aspect
   - Example: "Price is good (positive) but quality is poor (negative)"
   - Use dependency parsing and opinion mining

5. **Review Ranking & Helpfulness**
   - Score reviews by informativeness
   - Identify most helpful reviews
   - Use readability metrics and information density

6. **Comparative Analysis**
   - Compare with competitor products
   - Track sentiment trends over time
   - Generate differential summaries

## Testing

Test the custom summarizer with sample data:

```bash
# Make sure you have reviews in data/real_reviews.csv
python scripts/predict.py  # Generate reviews first
python scripts/custom_summarizer.py  # Test summarizer
```

Verify output:
- Check `data/custom_summary.txt` for saved summary
- Console output should show structured summary
- Verify all sections are present (stats, aspects, themes, samples)

## Performance

### Current Performance:
- **Speed**: ~1-2 seconds for 10-50 reviews
- **Accuracy**: Based on TF-IDF and rule-based logic
- **Scalability**: Works well up to ~100 reviews
- **Dependencies**: Minimal (only pandas required)

### Optimization Tips:
- For large datasets (>100 reviews), consider sampling
- Cache TF-IDF vectorizer for repeated analyses
- Use parallel processing for aspect extraction

## Troubleshooting

### Issue: "sklearn not available"
**Solution**: Install scikit-learn: `pip install scikit-learn`

### Issue: "No reviews found"
**Solution**: Run prediction first: `python scripts/predict.py`

### Issue: Basic summarization instead of TF-IDF
**Solution**: Ensure scikit-learn is installed and reviews CSV exists

### Issue: Empty aspects or themes
**Solution**: Check if reviews contain enough text (>20 characters each)

## Contributing

To add new features to the custom summarizer:

1. Add new methods to `CustomSummarizer` class
2. Update `generate_summary()` to include new insights
3. Test with various review datasets
4. Document new features in this README

## License

Same as the main project.

## Credits

- TF-IDF implementation: scikit-learn
- PDF processing: PyMuPDF
- Aspect extraction: Custom rule-based implementation
- Sentiment analysis: Integrated with existing ML model
