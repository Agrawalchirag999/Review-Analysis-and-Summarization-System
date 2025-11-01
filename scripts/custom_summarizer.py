"""
Custom Summarization Model for Review Analysis
Uses extractive and abstractive techniques to generate meaningful summaries
"""

import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from collections import Counter
import re
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try importing advanced NLP libraries
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️  scikit-learn not available. Using basic summarization.")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("⚠️  TextBlob not available. Using basic sentiment analysis.")


class CustomSummarizer:
    """
    Custom Review Summarizer using multiple techniques:
    1. TF-IDF based extractive summarization
    2. Sentiment-aware summary generation
    3. Key aspects extraction (quality, price, delivery, etc.)
    4. Rating-based insights
    """
    
    def __init__(self):
        self.reviews_data = None
        self.sentiment_stats = None
        
    def load_reviews_from_csv(self, csv_path="data/real_reviews.csv"):
        """Load reviews from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            self.reviews_data = df
            print(f"✅ Loaded {len(df)} reviews from {csv_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading reviews: {e}")
            return False
    
    def load_reviews_from_pdf(self, pdf_path="data/real_reviews.pdf"):
        """Extract reviews from PDF"""
        try:
            doc = fitz.open(pdf_path)
            text = "\n".join(page.get_text("text") for page in doc)
            doc.close()
            
            # Parse the text to extract reviews
            reviews = []
            lines = text.split('\n')
            
            current_review = ""
            for line in lines:
                line = line.strip()
                if len(line) > 20:  # Substantial text
                    current_review += line + " "
                elif current_review:
                    reviews.append(current_review.strip())
                    current_review = ""
            
            if current_review:
                reviews.append(current_review.strip())
            
            print(f"✅ Extracted {len(reviews)} reviews from PDF")
            return reviews
        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            return []
    
    def extract_key_phrases(self, reviews, top_n=10):
        """Extract key phrases using TF-IDF"""
        if not SKLEARN_AVAILABLE:
            return self._extract_key_phrases_basic(reviews)
        
        try:
            # Use TF-IDF to find important words/phrases
            vectorizer = TfidfVectorizer(
                max_features=100,
                ngram_range=(1, 3),  # unigrams to trigrams
                stop_words='english',
                min_df=2
            )
            
            tfidf_matrix = vectorizer.fit_transform(reviews)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            avg_scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
            top_indices = avg_scores.argsort()[-top_n:][::-1]
            
            key_phrases = [feature_names[i] for i in top_indices]
            return key_phrases
        except Exception as e:
            print(f"⚠️  TF-IDF extraction failed: {e}")
            return self._extract_key_phrases_basic(reviews)
    
    def _extract_key_phrases_basic(self, reviews, top_n=10):
        """Basic key phrase extraction without sklearn"""
        # Combine all reviews
        text = " ".join(reviews).lower()
        
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
                    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her',
                    'its', 'our', 'their', 'me', 'him', 'us', 'them'}
        
        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', text)
        words = [w for w in words if w not in stopwords]
        
        # Count frequency
        word_freq = Counter(words)
        return [word for word, _ in word_freq.most_common(top_n)]
    
    def extract_aspects(self, reviews):
        """Extract key aspects mentioned in reviews"""
        aspects = {
            'quality': ['quality', 'durable', 'build', 'material', 'construction', 'sturdy', 'solid', 'well-made'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'affordable', 'value', 'money', 'worth'],
            'delivery': ['delivery', 'shipping', 'arrived', 'package', 'delivered', 'received', 'packaging'],
            'performance': ['performance', 'works', 'working', 'efficient', 'fast', 'slow', 'speed'],
            'features': ['feature', 'features', 'functionality', 'option', 'options', 'capability'],
            'design': ['design', 'look', 'looks', 'appearance', 'aesthetic', 'style', 'color'],
            'customer_service': ['service', 'support', 'customer', 'help', 'helpline', 'response']
        }
        
        text = " ".join(reviews).lower()
        
        aspect_mentions = {}
        for aspect_name, keywords in aspects.items():
            count = sum(text.count(keyword) for keyword in keywords)
            if count > 0:
                aspect_mentions[aspect_name] = count
        
        # Sort by frequency
        sorted_aspects = sorted(aspect_mentions.items(), key=lambda x: x[1], reverse=True)
        return sorted_aspects
    
    def analyze_sentiment_distribution(self):
        """Analyze sentiment distribution from loaded reviews"""
        if self.reviews_data is None:
            return None
        
        sentiment_counts = {
            'positive': 0,
            'neutral': 0,
            'negative': 0
        }
        
        if 'sentiment' in self.reviews_data.columns:
            for sentiment in self.reviews_data['sentiment']:
                sentiment = str(sentiment).lower()
                if sentiment in sentiment_counts:
                    sentiment_counts[sentiment] += 1
        
        total = sum(sentiment_counts.values())
        sentiment_percentages = {
            k: (v / total * 100) if total > 0 else 0 
            for k, v in sentiment_counts.items()
        }
        
        return sentiment_counts, sentiment_percentages
    
    def extract_representative_reviews(self, n=3):
        """Extract most representative reviews for each sentiment"""
        if self.reviews_data is None or not SKLEARN_AVAILABLE:
            return self._extract_representative_basic(n)
        
        try:
            results = {'positive': [], 'neutral': [], 'negative': []}
            
            for sentiment in ['positive', 'neutral', 'negative']:
                sentiment_reviews = self.reviews_data[
                    self.reviews_data['sentiment'] == sentiment
                ]
                
                if len(sentiment_reviews) == 0:
                    continue
                
                # Get reviews with highest confidence
                top_reviews = sentiment_reviews.nlargest(n, 'confidence')
                
                for _, row in top_reviews.iterrows():
                    results[sentiment].append({
                        'text': row['text'][:200] + '...' if len(row['text']) > 200 else row['text'],
                        'rating': int(row.get('rating', 3)),
                        'confidence': float(row.get('confidence', 0))
                    })
            
            return results
        except Exception as e:
            print(f"⚠️  Representative extraction failed: {e}")
            return self._extract_representative_basic(n)
    
    def _extract_representative_basic(self, n=3):
        """Basic representative review extraction"""
        if self.reviews_data is None:
            return {'positive': [], 'neutral': [], 'negative': []}
        
        results = {'positive': [], 'neutral': [], 'negative': []}
        
        for sentiment in ['positive', 'neutral', 'negative']:
            sentiment_reviews = self.reviews_data[
                self.reviews_data['sentiment'] == sentiment
            ]
            
            for _, row in sentiment_reviews.head(n).iterrows():
                text = row['text']
                results[sentiment].append({
                    'text': text[:200] + '...' if len(text) > 200 else text,
                    'rating': int(row.get('rating', 3)),
                    'confidence': float(row.get('confidence', 0))
                })
        
        return results
    
    def generate_summary(self, format='html'):
        """
        Generate comprehensive summary
        
        Args:
            format: 'html' for web display (default) or 'text' for console/file
        """
        if self.reviews_data is None:
            return "No reviews data loaded."
        
        summary_parts = []
        
        # Choose separator and formatting based on format
        if format == 'html':
            line_break = '<br>'
            double_break = '<br><br>'
            bold_start = '<strong>'
            bold_end = '</strong>'
            italic_start = '<em>'
            italic_end = '</em>'
            bullet = '•'
        else:
            line_break = '\n'
            double_break = '\n\n'
            bold_start = '**'
            bold_end = '**'
            italic_start = '"'
            italic_end = '"'
            bullet = '-'
        
        # 1. Overall statistics
        total_reviews = len(self.reviews_data)
        avg_rating = self.reviews_data['rating'].mean() if 'rating' in self.reviews_data.columns else 0
        
        summary_parts.append(f"{bold_start}Summary of {total_reviews} Customer Reviews{bold_end}{line_break}")
        summary_parts.append(f"Average Rating: {avg_rating:.1f}/5 stars{double_break}")
        
        # 2. Sentiment analysis
        sentiment_counts, sentiment_pct = self.analyze_sentiment_distribution()
        summary_parts.append(f"{bold_start}Sentiment Breakdown:{bold_end}{line_break}")
        summary_parts.append(f"{bullet} Positive: {sentiment_counts['positive']} reviews ({sentiment_pct['positive']:.1f}%){line_break}")
        summary_parts.append(f"{bullet} Neutral: {sentiment_counts['neutral']} reviews ({sentiment_pct['neutral']:.1f}%){line_break}")
        summary_parts.append(f"{bullet} Negative: {sentiment_counts['negative']} reviews ({sentiment_pct['negative']:.1f}%){double_break}")
        
        # 3. Key aspects
        reviews_text = self.reviews_data['text'].tolist()
        aspects = self.extract_aspects(reviews_text)
        
        if aspects:
            summary_parts.append(f"{bold_start}Most Discussed Aspects:{bold_end}{line_break}")
            for aspect, count in aspects[:5]:
                summary_parts.append(f"{bullet} {aspect.replace('_', ' ').title()}: mentioned {count} times{line_break}")
            summary_parts.append(double_break.replace(line_break + line_break, '') if format == 'html' else double_break)
        
        # 4. Key phrases
        key_phrases = self.extract_key_phrases(reviews_text, top_n=8)
        if key_phrases:
            summary_parts.append(f"{bold_start}Key Themes:{bold_end} {', '.join(key_phrases)}{double_break}")
        
        # 5. Representative reviews
        repr_reviews = self.extract_representative_reviews(n=2)
        
        if repr_reviews['positive']:
            summary_parts.append(f"{bold_start}Sample Positive Review:{bold_end}{line_break}")
            review = repr_reviews['positive'][0]
            review_text = review["text"]
            review_rating = review["rating"]
            summary_parts.append(f'{italic_start}{review_text}{italic_end} - {review_rating}⭐{double_break}')
        
        if repr_reviews['negative']:
            summary_parts.append(f"{bold_start}Sample Negative Review:{bold_end}{line_break}")
            review = repr_reviews['negative'][0]
            review_text = review["text"]
            review_rating = review["rating"]
            summary_parts.append(f'{italic_start}{review_text}{italic_end} - {review_rating}⭐{double_break}')
        
        # 6. Conclusion
        if sentiment_pct['positive'] > 60:
            conclusion = "Overall, customers are highly satisfied with this product."
        elif sentiment_pct['positive'] > 40:
            conclusion = "Overall, customers have mixed feelings about this product."
        else:
            conclusion = "Overall, customers report significant concerns with this product."
        
        summary_parts.append(f"{bold_start}Conclusion:{bold_end} {conclusion}")
        
        return "".join(summary_parts)


def main():
    """Main function to generate summary"""
    print("=" * 70)
    print("Custom Review Summarizer")
    print("=" * 70)
    
    # Initialize summarizer
    summarizer = CustomSummarizer()
    
    # Load reviews from CSV (preferred)
    csv_path = "data/real_reviews.csv"
    if os.path.exists(csv_path):
        if summarizer.load_reviews_from_csv(csv_path):
            # Generate text format for console display
            summary = summarizer.generate_summary(format='text')
            print("\n" + "=" * 70)
            print(summary)
            print("=" * 70)
            
            # Save summary to file
            output_path = "data/custom_summary.txt"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            print(f"\n✅ Summary saved to {output_path}")
            
            return summary
    
    # Fallback to PDF
    pdf_path = "data/real_reviews.pdf"
    if os.path.exists(pdf_path):
        reviews = summarizer.load_reviews_from_pdf(pdf_path)
        if reviews:
            print("⚠️  Loaded from PDF, using basic summarization")
            # Create a simple DataFrame
            summarizer.reviews_data = pd.DataFrame({
                'text': reviews,
                'rating': [3] * len(reviews),
                'sentiment': ['neutral'] * len(reviews),
                'confidence': [0.5] * len(reviews)
            })
            summary = summarizer.generate_summary()
            print("\n" + "=" * 70)
            print(summary)
            print("=" * 70)
            return summary
    
    print("❌ No reviews found. Please run prediction first.")
    return None


if __name__ == "__main__":
    main()
