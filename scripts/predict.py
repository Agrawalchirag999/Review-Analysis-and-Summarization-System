import pandas as pd
import numpy as np
import pickle
import re
from textblob import TextBlob
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging
import os
import sys
import json

logging.basicConfig(level=logging.INFO)

# Define functions exactly as in the training script (must match for pickle to work)
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s!?.]', '', text)
    text = re.sub(r'!+', '!', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_features(text):
    # Count features that might indicate fake reviews
    exclamation_count = text.count('!')
    question_count = text.count('?')
    word_count = len(text.split())
    char_count = len(text)
    uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
    
    # Extreme words
    extreme_words = ['amazing', 'terrible', 'perfect', 'worst', 'best', 'incredible', 'awful', 'fantastic']
    extreme_count = sum(text.lower().count(word) for word in extreme_words)
    
    return [exclamation_count, question_count, word_count, char_count, uppercase_ratio, extreme_count]

# Load the complete package (includes models, vectorizer, best_model_name)
model_components = None
MODEL_PATH = "snlp/saved_models/fake_review_detector_20251031_224832_complete_package.pkl"

try:
    logging.info(f"Loading trained model from {MODEL_PATH}...")
    with open(MODEL_PATH, 'rb') as f:
        model_components = pickle.load(f)
    logging.info(f"✓ Model loaded successfully! Using {model_components['best_model_name']} model")
    
except Exception as e:
    logging.error(f"Could not load model at startup: {e}")
    import traceback
    traceback.print_exc()
    model_components = None

def generate_pdf(real_reviews, output_pdf_path):
    try:
        c = canvas.Canvas(output_pdf_path, pagesize=letter)
        width, height = letter

        y_position = height - 40
        for review in real_reviews:
            if y_position <= 40:
                c.showPage()
                y_position = height - 40 
            c.drawString(40, y_position, f"Text: {review['text']}")
            c.drawString(40, y_position - 20, f"Rating: {review['rating']}")
            y_position -= 40  

        c.save()
        return True
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        return False

def predict_fake_review(text, rating=5):
    """
    Predict if a review is fake or real
    Returns dict with prediction, probabilities, and sentiment
    """
    global model_components
    
    if model_components is None:
        raise ValueError("Model not loaded! Check model path.")
    
    try:
        # Clean the text
        cleaned = clean_text(text)
        
        # Vectorize using the saved vectorizer
        vectorized = model_components['vectorizer'].transform([cleaned])
        
        # Get the best model
        best_model = model_components['models'][model_components['best_model_name']]
        
        # Make prediction
        prediction = best_model.predict(vectorized)[0]
        probabilities = best_model.predict_proba(vectorized)[0]
        
        # Calculate sentiment using TextBlob
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        
        # Categorize sentiment
        if sentiment_score > 0.1:
            sentiment_category = "positive"
        elif sentiment_score < -0.1:
            sentiment_category = "negative"
        else:
            sentiment_category = "neutral"
        
        return {
            'is_fake': prediction == 1,
            'fake_probability': probabilities[1],
            'real_probability': probabilities[0],
            'confidence': max(probabilities),
            'sentiment': sentiment_category,
            'sentiment_score': sentiment_score,
            'model_used': model_components['best_model_name']
        }
        
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        raise

def main():
    """Main prediction function"""
    try:
        input_csv_path = "data/input_reviews.csv" 
        output_csv_path = "data/real_reviews.csv" 
        output_pdf_path = "data/real_reviews.pdf" 
        sentiment_stats_path = "data/sentiment_stats.json" 

        logging.info(f"Reading {input_csv_path}...")
        if not os.path.exists(input_csv_path):
            logging.error(f"Input file {input_csv_path} not found!")
            return False

        df = pd.read_csv(input_csv_path)
        logging.info(f"Loaded {len(df)} reviews for analysis")

        # Initialize counters
        real_reviews = []
        real_reviews_df = []
        sentiment_counts = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        total_reviews = 0
        real_reviews_count = 0
        fake_reviews_count = 0

        # Process each review
        logging.info("Starting review analysis...")
        for idx, row in df.iterrows():
            text = row['text']
            rating = row.get('rating', 5)  # Default to 5 if no rating
            total_reviews += 1

            try:
                # Predict using the trained model
                result = predict_fake_review(text, rating)
                
                logging.debug(f"Review {idx}: Fake={result['is_fake']}, "
                            f"Confidence={result['confidence']:.2%}, "
                            f"Sentiment={result['sentiment']}")
                
                # Only keep real reviews
                if not result['is_fake']:
                    real_reviews_count += 1
                    sentiment_counts[result['sentiment']] += 1
                    
                    real_reviews.append({
                        'text': text,
                        'rating': rating,
                        'sentiment': result['sentiment']
                    })
                    real_reviews_df.append({
                        'text': text,
                        'rating': rating,
                        'sentiment': result['sentiment'],
                        'confidence': result['confidence']
                    })
                else:
                    fake_reviews_count += 1
                    
            except Exception as e:
                logging.error(f"Error processing review {idx}: {str(e)}")
                continue

        # Save statistics
        sentiment_stats = {
            "sentiment_counts": sentiment_counts,
            "total_reviews": total_reviews,
            "real_reviews_count": real_reviews_count,
            "fake_reviews_count": fake_reviews_count,
            "fake_percentage": (fake_reviews_count / total_reviews * 100) if total_reviews > 0 else 0
        }
        
        with open(sentiment_stats_path, 'w') as f:
            json.dump(sentiment_stats, f, indent=2)
        logging.info(f"✓ Sentiment statistics saved to {sentiment_stats_path}")
        logging.info(f"  Total: {total_reviews}, Real: {real_reviews_count}, Fake: {fake_reviews_count}")

        # Save real reviews to CSV
        if real_reviews_df:
            pd.DataFrame(real_reviews_df).to_csv(output_csv_path, index=False)
            logging.info(f"✓ Real reviews saved to {output_csv_path}")
        else:
            logging.warning("No real reviews found!")
            return False

        # Generate PDF
        if real_reviews:
            success = generate_pdf(real_reviews, output_pdf_path)
            if success:
                logging.info(f"✓ PDF report saved to {output_pdf_path}")
                return True
            else:
                logging.error("Failed to generate PDF")
                return False
        else:
            logging.warning("No real reviews to generate PDF!")
            return False

    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
