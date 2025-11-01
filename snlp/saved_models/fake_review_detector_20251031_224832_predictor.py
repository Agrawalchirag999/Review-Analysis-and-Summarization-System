
import pickle
import joblib
import re
import numpy as np

# Load the saved model components
def load_model(model_path="saved_models\fake_review_detector_20251031_224832_complete_package.pkl"):
    with open(model_path, 'rb') as f:
        components = pickle.load(f)
    return components

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s!?.]', '', text)
    text = re.sub(r'!+', '!', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_fake_review(text, model_components=None):
    if model_components is None:
        model_components = load_model()

    # Preprocess text
    cleaned = clean_text(text)

    # Vectorize
    vectorized = model_components['vectorizer'].transform([cleaned])

    # Predict using best model
    best_model = model_components['models'][model_components['best_model_name']]
    prediction = best_model.predict(vectorized)[0]
    probabilities = best_model.predict_proba(vectorized)[0]

    return {
        'prediction': 'FAKE' if prediction == 1 else 'REAL',
        'confidence': max(probabilities) * 100,
        'fake_probability': probabilities[1] * 100,
        'real_probability': probabilities[0] * 100,
        'model_used': model_components['best_model_name']
    }

# Example usage:
if __name__ == "__main__":
    # Test the loaded model
    test_text = "This product is AMAZING!!! Best purchase ever!!!"
    result = predict_fake_review(test_text)
    print(f"Text: {test_text}")
    print(f"Prediction: {result['prediction']} ({result['confidence']:.1f}% confidence)")
