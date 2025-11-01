import os
import logging
from flask import Flask, render_template, request, jsonify
import subprocess
import json
import re
import config
import threading
import uuid
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__, template_folder="templates")
app.secret_key = config.SESSION_SECRET

# In-memory job storage for background tasks
jobs = {}

def extract_product_url(url):
    """Extract and validate product URL from Walmart"""
    url = url.strip()
    
    # Check if it's a valid URL
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Support Walmart only (primary working scraper)
    supported_domains = ['walmart.com']
    
    if any(domain in url.lower() for domain in supported_domains):
        return url
    
    return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/reviews", methods=["GET"])
def get_reviews():
    """Endpoint to fetch analyzed reviews"""
    try:
        import pandas as pd
        reviews_path = "data/real_reviews.csv"
        
        if not os.path.exists(reviews_path):
            return jsonify({"error": "No reviews found. Please analyze some reviews first."}), 404
        
        # Read the CSV file
        df = pd.read_csv(reviews_path)
        
        # Convert to list of dictionaries
        reviews_list = []
        for _, row in df.iterrows():
            reviews_list.append({
                "text": row.get("text", ""),
                "rating": int(row.get("rating", 3)),
                "sentiment": row.get("sentiment", "neutral"),
                "confidence": float(row.get("confidence", 0.0))
            })
        
        # Load sentiment stats if available
        sentiment_stats = {}
        stats_path = "data/sentiment_stats.json"
        if os.path.exists(stats_path):
            with open(stats_path, 'r') as f:
                sentiment_stats = json.load(f)
        
        return jsonify({
            "reviews": reviews_list,
            "stats": sentiment_stats,
            "total": len(reviews_list)
        })
    except Exception as e:
        logging.error(f"Error fetching reviews: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        product_url = data.get("amazon_url")  # Keep same key for compatibility
        
        if not product_url:
            return jsonify({"error": "No product URL provided"}), 400
        
        validated_url = extract_product_url(product_url)
        if not validated_url:
            return jsonify({"error": "Invalid URL. Please provide a valid Walmart product URL (e.g., https://www.walmart.com/ip/product-name/12345)."}), 400
        
        logging.info(f"Validated URL: {validated_url}")
        return jsonify({"status": "success", "product_url": validated_url})
    
    except Exception as e:
        logging.error(f"Error in analyze endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()
        product_url = data.get("product_url")
        
        if not product_url:
            return jsonify({"error": "No product URL provided"}), 400

        command = ["python", "scripts/scraper.py", product_url]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            logging.error(f"Scraper error: {result.stderr}")
            return jsonify({"error": "Error during scraping", "details": result.stderr}), 500
        
        return jsonify({"status": "success", "message": "Reviews scraped successfully"})
    
    except Exception as e:
        logging.error(f"Error in scrape endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

def run_predict_background(job_id):
    """Background task to run prediction"""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["message"] = "Loading ML models and analyzing reviews..."
        logging.info(f"Job {job_id}: Starting prediction")
        
        result = subprocess.run(["python", "scripts/predict.py"], capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            logging.error(f"Job {job_id}: Prediction error: {result.stderr}")
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = f"Error during prediction: {result.stderr}"
        else:
            logging.info(f"Job {job_id}: Prediction completed successfully")
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["message"] = "Fake reviews identified successfully"
            jobs[job_id]["result"] = {"message": "Fake reviews identified successfully"}
    except subprocess.TimeoutExpired:
        logging.error(f"Job {job_id}: Prediction timed out")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = "Prediction timed out after 5 minutes"
    except Exception as e:
        logging.error(f"Job {job_id}: Error in prediction: {str(e)}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        job_id = str(uuid.uuid4())
        jobs[job_id] = {
            "status": "pending",
            "message": "Starting analysis...",
            "created_at": datetime.now().isoformat()
        }
        
        # Start background thread
        thread = threading.Thread(target=run_predict_background, args=(job_id,))
        thread.daemon = True
        thread.start()
        
        return jsonify({"status": "started", "job_id": job_id})
    
    except Exception as e:
        logging.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/predict_status/<job_id>", methods=["GET"])
def predict_status(job_id):
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404
    
    job = jobs[job_id]
    response = {
        "status": job["status"],
        "message": job.get("message", "")
    }
    
    if job["status"] == "completed":
        response["result"] = job.get("result", {})
    elif job["status"] == "failed":
        response["error"] = job.get("error", "Unknown error")
    
    return jsonify(response)

def run_summarize_background(job_id):
    """Background task to run summarization"""
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["message"] = "Generating intelligent summary with custom ML model..."
        logging.info(f"Job {job_id}: Starting summarization")
        
        import scripts.summary as summary_module
        summary_text = summary_module.run_summary()
        
        if not summary_text:
            logging.error(f"Job {job_id}: Failed to generate summary")
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = "Failed to generate summary"
            return
        
        sentiment_stats_path = "data/sentiment_stats.json"
        sentiment_stats = {
            "sentiment_counts": {"positive": 0, "neutral": 0, "negative": 0},
            "total_reviews": 0,
            "real_reviews_count": 0,
            "fake_reviews_count": 0
        }

        if os.path.exists(sentiment_stats_path):
            try:
                with open(sentiment_stats_path, 'r') as f:
                    sentiment_stats = json.load(f)
                logging.info(f"Job {job_id}: Loaded sentiment statistics")
            except Exception as e:
                logging.error(f"Job {job_id}: Error loading sentiment statistics: {str(e)}")
        
        logging.info(f"Job {job_id}: Summarization completed successfully")
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Summary generated successfully"
        jobs[job_id]["result"] = {
            "summary": summary_text,
            "sentiment_stats": sentiment_stats
        }
    except Exception as e:
        logging.error(f"Job {job_id}: Error in summarization: {str(e)}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        job_id = str(uuid.uuid4())
        jobs[job_id] = {
            "status": "pending",
            "message": "Starting summarization...",
            "created_at": datetime.now().isoformat()
        }
        
        # Start background thread
        thread = threading.Thread(target=run_summarize_background, args=(job_id,))
        thread.daemon = True
        thread.start()
        
        return jsonify({"status": "started", "job_id": job_id})
    
    except Exception as e:
        logging.error(f"Error in summarize endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/summarize_status/<job_id>", methods=["GET"])
def summarize_status(job_id):
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404
    
    job = jobs[job_id]
    response = {
        "status": job["status"],
        "message": job.get("message", "")
    }
    
    if job["status"] == "completed":
        response["result"] = job.get("result", {})
    elif job["status"] == "failed":
        response["error"] = job.get("error", "Unknown error")
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT, use_reloader=False)
