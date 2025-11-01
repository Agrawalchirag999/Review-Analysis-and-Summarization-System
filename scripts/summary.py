import requests
import fitz  # PyMuPDF
import json
import sys
import os
from collections import Counter
import re

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Try importing custom summarizer
try:
    from scripts.custom_summarizer import CustomSummarizer
    CUSTOM_SUMMARIZER_AVAILABLE = True
except ImportError:
    CUSTOM_SUMMARIZER_AVAILABLE = False
    print("⚠️  Custom summarizer not available, using fallback methods.")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text("text") for page in doc)
    return text

def generate_simple_summary(text):
    """
    Generate a simple summary when Ollama is unavailable
    This extracts key information from reviews
    """
    # Split into individual reviews
    reviews = [r.strip() for r in text.split('\n') if len(r.strip()) > 20]
    
    # Count sentiment mentions
    positive_words = ['amazing', 'excellent', 'great', 'best', 'love', 'perfect', 'fantastic', 'wonderful', 'outstanding', 'good', 'happy', 'satisfied']
    negative_words = ['terrible', 'worst', 'horrible', 'bad', 'disappointed', 'poor', 'waste', 'awful', 'broke', 'unhelpful']
    
    text_lower = text.lower()
    positive_count = sum(text_lower.count(word) for word in positive_words)
    negative_count = sum(text_lower.count(word) for word in negative_words)
    
    # Extract common themes
    sentences = re.split(r'[.!?]', text)
    quality_mentions = [s for s in sentences if 'quality' in s.lower()]
    price_mentions = [s for s in sentences if any(w in s.lower() for w in ['price', 'money', 'value', 'expensive'])]
    delivery_mentions = [s for s in sentences if any(w in s.lower() for w in ['delivery', 'packaging', 'shipping'])]
    
    # Build summary
    summary_parts = []
    summary_parts.append(f"Based on {len(reviews)} reviews analyzed:")
    
    if positive_count > negative_count:
        summary_parts.append("Overall sentiment is positive.")
        summary_parts.append(f"Customers frequently mention positive aspects ({positive_count} positive keywords found).")
    elif negative_count > positive_count:
        summary_parts.append("Overall sentiment is negative.")
        summary_parts.append(f"Customers express concerns ({negative_count} negative keywords found).")
    else:
        summary_parts.append("Sentiment is mixed with both positive and negative feedback.")
    
    if quality_mentions:
        summary_parts.append("Product quality is a common topic of discussion.")
    
    if price_mentions:
        summary_parts.append("Price and value for money are frequently mentioned.")
    
    if delivery_mentions:
        summary_parts.append("Delivery and packaging experiences vary among customers.")
    
    summary_parts.append("Recommendations range from highly satisfied to disappointed customers.")
    
    return " ".join(summary_parts)

def run_summary(pdf_file="data/real_reviews.pdf"):
    # PRIORITY 1: Try custom summarizer with CSV (most detailed)
    if CUSTOM_SUMMARIZER_AVAILABLE:
        csv_path = "data/real_reviews.csv"
        if os.path.exists(csv_path):
            try:
                print("Using custom summarizer with structured data...")
                summarizer = CustomSummarizer()
                if summarizer.load_reviews_from_csv(csv_path):
                    summary = summarizer.generate_summary()
                    print("✅ Custom summarizer completed successfully")
                    return summary
            except Exception as e:
                print(f"⚠️  Custom summarizer failed: {e}")
                print("Falling back to Ollama/simple summarization...")
    
    # PRIORITY 2: Try Ollama (if available)
    file_content = extract_text_from_pdf(pdf_file)

    ollama_url = config.OLLAMA_URL
    ollama_model = config.OLLAMA_MODEL
    
    # Truncate content if too long to avoid token limits
    max_content_length = 4000
    if len(file_content) > max_content_length:
        file_content = file_content[:max_content_length] + "..."
    
    try:
        print("Trying Ollama summarization...")
        response = requests.post(
            ollama_url,
            json={
                "model": ollama_model,
                "prompt": (
                    "Summarize these reviews into a single paragraph, "
                    "highlighting the pros and cons of the product:\n\n" + file_content
                ),
                "stream": True
            },
            stream=True,
            timeout=120
        )
        
        # Check for HTTP errors
        if response.status_code != 200:
            error_msg = f"Ollama API error: {response.status_code} - {response.text}"
            print(error_msg)
            print("Falling back to simple summarization...")
            return generate_simple_summary(file_content)
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        print("Falling back to simple summarization...")
        return generate_simple_summary(file_content)

    full_response = ""
    try:
        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line)
                    full_response += json_line.get("response", "")
                    
                    # Check if generation is done
                    if json_line.get("done", False):
                        break
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    continue
    except Exception as e:
        print(f"Error processing response: {e}")
        if full_response:
            return full_response.strip()
        return f"Summary generation partially failed: {str(e)}"

    return full_response.strip() if full_response else "No summary generated"


if __name__ == "__main__":
    print("=" * 70)
    print("Review Summarizer")
    print("=" * 70)
    summary = run_summary()
    print("\n" + summary)
    print("\n" + "=" * 70)
