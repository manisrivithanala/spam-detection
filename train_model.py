import pandas as pd
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = pd.read_csv('data/spam.csv', encoding='latin-1', quotechar='"', doublequote=True, on_bad_lines='skip')
data = data[['v1', 'v2']]  # Keep only label and message columns
data.columns = ['label', 'message']

# Convert label to binary
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Clean text function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # remove punctuation
    return text

data['clean_message'] = data['message'].apply(clean_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    data['clean_message'], data['label'], test_size=0.2, random_state=42
)

# Vectorize using TF‑IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, 'model/spam_model.pkl')
joblib.dump(vectorizer, 'model/vectorizer.pkl')
print("Model saved!")