# config.py
import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_PATH = os.path.join(BASE_DIR, 'data', 'spam.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'spam_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')

# Model settings
MAX_FEATURES = 5000  # Max words for TF-IDF
TEST_SIZE = 0.2      # Train-test split ratio
RANDOM_STATE = 42    # For reproducibility

# App settings
DEBUG = True
HOST = '127.0.0.1'
PORT = 5000