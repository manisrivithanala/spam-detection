# test_prediction_complete.py
import joblib
import re
import os
import sys
from datetime import datetime

print("=" * 60)
print("🔍 SPAM DETECTOR - COMPLETE DIAGNOSTIC TEST")
print("=" * 60)
print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Step 1: Check current directory
print("📁 Step 1: Checking project structure...")
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")
print()

# Step 2: Check model files
print("📁 Step 2: Checking model files...")
model_path = 'model/spam_model.pkl'
vectorizer_path = 'model/vectorizer.pkl'

if not os.path.exists('model'):
    print("❌ 'model' folder not found!")
    os.makedirs('model', exist_ok=True)
    print("✅ Created model folder")
else:
    print("✅ Model folder exists")

if not os.path.exists(model_path):
    print(f"❌ Model not found at {model_path}")
    print("Please run train_model.py first")
    sys.exit(1)
else:
    model_size = os.path.getsize(model_path)
    print(f"✅ Model found: {model_path} ({model_size/1024:.2f} KB)")

if not os.path.exists(vectorizer_path):
    print(f"❌ Vectorizer not found at {vectorizer_path}")
    sys.exit(1)
else:
    vec_size = os.path.getsize(vectorizer_path)
    print(f"✅ Vectorizer found: {vectorizer_path} ({vec_size/1024:.2f} KB)")
print()

# Step 3: Load model and vectorizer
print("📁 Step 3: Loading model and vectorizer...")
try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("✅ Model and vectorizer loaded successfully")
    print(f"   Model type: {type(model).__name__}")
    print(f"   Vectorizer type: {type(vectorizer).__name__}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)
print()

# Step 4: Test messages
print("📁 Step 4: Testing predictions...")
print("-" * 60)

# Clean text function
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text
    return ""

# Your messages to test
test_messages = [
    "Hey, are we still meeting for coffee at 3pm?",
    "Can you pick up some milk on your way home?",
    "The project deadline has been extended to Friday.",
    "Don't forget mom's birthday party this Sunday.",
    "Thanks for the gift, I love it!",
    "I'll be there in 10 minutes.",
    "The meeting has been moved to room 404.",
    "Did you finish the report for tomorrow?",
    "Let's order pizza tonight.",
    "What time does the movie start?"
]

print(f"Testing {len(test_messages)} messages...\n")

for i, msg in enumerate(test_messages, 1):
    try:
        # Clean and vectorize
        cleaned = clean_text(msg)
        vec = vectorizer.transform([cleaned])
        
        # Predict
        pred = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        confidence = max(proba) * 100
        
        # Determine result
        result = "🚨 SPAM" if pred == 1 else "✅ HAM"
        
        print(f"Test {i}:")
        print(f"   Message: {msg[:50]}..." if len(msg) > 50 else f"   Message: {msg}")
        print(f"   Result: {result}")
        print(f"   Confidence: {confidence:.1f}%")
        print(f"   Spam probability: {proba[1]*100:.1f}%")
        print(f"   Ham probability: {proba[0]*100:.1f}%")
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error testing message {i}: {e}")
        print("-" * 40)

print("\n✅ Test complete!")

# Step 5: Additional diagnostics
print("\n📁 Step 5: Additional diagnostics...")
print(f"Model classes: {model.classes_}")
print(f"Number of features: {len(vectorizer.get_feature_names_out()) if hasattr(vectorizer, 'get_feature_names_out') else 'Unknown'}")
print(f"Vocabulary size: {len(vectorizer.vocabulary_) if hasattr(vectorizer, 'vocabulary_') else 'Unknown'}")