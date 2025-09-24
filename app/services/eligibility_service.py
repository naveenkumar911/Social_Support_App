import joblib
from pathlib import Path
MODEL_PATH = Path('models/eligibility_model.pkl')

def predict_eligibility(features: dict):
    if not MODEL_PATH.exists():
        return {'error': 'model not found'}
    model = joblib.load(MODEL_PATH)
    X = [[features['income'], features['family_size'], features['employment_years'], features['assets_value']]]
    pred = model.predict(X)[0]
    proba = model.predict_proba(X).tolist()[0]
    label = 'approve' if pred==1 else 'soft_decline'
    return {'prediction': label, 'probability': proba}