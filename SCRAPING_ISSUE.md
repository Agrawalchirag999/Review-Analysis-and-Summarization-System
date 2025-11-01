# IMPORTANT NOTE ABOUT SCRAPING

## Issue with Oxylabs Free Trial

Your Oxylabs free trial account does NOT support the `amazon_reviews` source, which is required for this project.

### Error Message:
```
{"message":"Unsupported source: amazon_reviews"}
```

## Workaround Options:

### Option 1: Use Sample Data (Quick Test)
I've updated the scraper to create sample review data so you can test the fake review detection and summarization features without actual scraping.

### Option 2: Upgrade Oxylabs Plan
The `amazon_reviews` source requires a paid Oxylabs plan. Visit https://oxylabs.io/ to upgrade.

### Option 3: Use Alternative Scraping Method
Direct scraping from Amazon.in is being blocked. You would need:
- Residential proxies
- Or scraping service that supports Amazon India reviews
- Or manual data collection

## Current Solution

The scraper now generates sample review data when it detects scraping failures, allowing you to:
✅ Test fake review detection
✅ Test sentiment analysis  
✅ Test AI summarization
✅ See the complete workflow

## To Use Real Data:

1. **Manually collect reviews** from Amazon and save to `data/input_reviews.csv` in this format:
   ```csv
   text,rating
   "Review text here",5
   "Another review",4
   ```

2. **Upgrade Oxylabs** to a plan that supports `amazon_reviews` source

3. **Use alternative API** like:
   - ScraperAPI (supports Amazon)
   - Bright Data
   - Apify Amazon Scraper

## Testing the System

Even with sample data, you can fully test:
- Machine learning fake review detection
- Sentiment analysis (positive/neutral/negative)
- AI-powered summarization with DeepSeek
- PDF report generation
- Web interface functionality

The ML models will work exactly the same with real or sample data!
