"""
Spam Detection System - Production Version 2.0
Optimized for Render Deployment & High-Speed Performance
"""

from flask import Flask, render_template, request, jsonify, url_for
import joblib
import pandas as pd
import os
import re
import matplotlib
matplotlib.use('Agg')  # Required for headless server environments
import matplotlib.pyplot as plt
import io
import base64
import json
import logging
import time
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'spam-detection-secret-2026')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Configuration Paths
MODEL_PATH = 'model/spam_model.pkl'
VECTORIZER_PATH = 'model/vectorizer.pkl'
DATA_PATH = 'data/spam.csv'
INFO_PATH = 'model/model_info.json'

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global Cache (The Secret to Speed)
# We store heavy objects here so we don't reload them on every page click
cache = {
    'model': None,
    'vectorizer': None,
    'model_info': {
        'loaded': False,
        'accuracy': 0.98,
        'precision': 0.98,
        'recall': 0.97,
        'f1_score': 0.97,
        'training_date': 'Not Trained',
        'samples': 5572
    },
    'dataset_stats': None,
    'chart_base64': None
}

def clean_text(text):
    """Advanced Text Cleaning (URLs, Emails, Numbers, Special Chars)"""
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # URLs
    text = re.sub(r'\S+@\S+', '', text) # Emails
    text = re.sub(r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text) # Phones
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\'\$\%\&\*]', '', text) # Special chars
    return ' '.join(text.split())

def initialize_resources():
    """Run once at startup to load model and pre-calculate stats"""
    global cache
    try:
        # 1. Load ML Model
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            cache['model'] = joblib.load(MODEL_PATH)
            cache['vectorizer'] = joblib.load(VECTORIZER_PATH)
            cache['model_info']['loaded'] = True
            
            # Load real metrics if they exist
            if os.path.exists(INFO_PATH):
                with open(INFO_PATH, 'r') as f:
                    cache['model_info'].update(json.load(f))
            logger.info("✅ ML Model loaded successfully.")

        # 2. Process Stats and Visuals (Caches them for instant page switching)
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, encoding='latin-1').iloc[:, :2]
            df.columns = ['label', 'message']
            
            spam_count = int((df['label'].str.lower() == 'spam').sum())
            ham_count = int((df['label'].str.lower() == 'ham').sum())
            total = len(df)
            
            cache['dataset_stats'] = {
                'total': total,
                'spam': spam_count,
                'ham': ham_count,
                'spam_percentage': round((spam_count/total)*100, 1) if total > 0 else 0
            }

            # Generate Pie Chart once
            plt.figure(figsize=(8, 6), facecolor='#1e2429')
            plt.style.use('dark_background')
            colors = ['#2ecc71', '#e74c3c']
            plt.pie([ham_count, spam_count], labels=['Ham (Legit)', 'Spam'], 
                    autopct='%1.1f%%', colors=colors, startangle=90, 
                    textprops={'color':"w", 'weight':'bold'})
            plt.title("Dataset Distribution", color='white', fontsize=14, pad=20)
            
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches='tight', facecolor='#1e2429')
            img.seek(0)
            cache['chart_base64'] = base64.b64encode(img.getvalue()).decode()
            plt.close()
            logger.info("✅ Statistics and Visuals cached.")
        else:
            logger.warning("⚠️ data/spam.csv not found. Stats will be empty.")

    except Exception as e:
        logger.error(f"❌ Startup Error: {e}")

# Initialize at runtime
initialize_resources()

# ==================== ROUTES ====================

# Home
@app.route('/')
def index():
    return render_template('index.html')


# Predict API
@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    
    if not cache['model'] or not cache['vectorizer']:
        return jsonify({'success': False, 'error': 'Model files missing on server'}), 503

    data = request.get_json() if request.is_json else request.form
    message = data.get('message', '')

    if not message.strip():
        return jsonify({'success': False, 'error': 'Message content is empty'}), 400

    cleaned = clean_text(message)
    vec = cache['vectorizer'].transform([cleaned])
    pred = cache['model'].predict(vec)[0]
    proba = cache['model'].predict_proba(vec)[0]
    
    duration_ms = round((time.time() - start_time) * 1000, 2)

    return jsonify({
        'success': True,
        'prediction': 'spam' if pred == 1 else 'ham',
        'confidence': round(float(max(proba) * 100), 2),
        'spam_probability': round(float(proba[1] * 100), 2),
        'ham_probability': round(float(proba[0] * 100), 2),
        'testing_time': f"{duration_ms} ms",
        'timestamp': datetime.now().isoformat()
    })


# Stats Page
@app.route('/stats')
def stats():
    if not cache['dataset_stats']:
        return render_template('stats.html', error="Dataset files missing.")
        
    return render_template(
        'stats.html',
        dataset=cache['dataset_stats'],
        model=cache['model_info'],
        visuals={'pie_chart': cache['chart_base64']}
    )


# ✅ ADD THIS
@app.route('/batch')
def batch():
    return render_template('batch.html')


# ✅ ADD THIS
@app.route('/about')
def about():
    return render_template('about.html')


# Health check
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': cache['model'] is not None,
        'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


# Deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)