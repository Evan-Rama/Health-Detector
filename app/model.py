import os
import pandas as pd
import joblib

# --- Load Model ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder 'app' atau tempat model.py
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "xgb_model.pkl")  # adjust sesuai struktur folder

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Failed to load model: {e}")

# --- Mapping Kategori ---
gender_map = {"Male": 1, "Female": 0}
diabetic_map = {
    "No": 0,
    "No, Borderline Diabetes": 1,
    "Yes": 2,
    "Yes (during pregnancy)": 3
}
genhealth_map = {
    "Excellent": 0,
    "Fair": 1,
    "Good": 2,
    "Poor": 3,
    "Very Good": 4
}
race_map = {
    "American Indian/Alaskan Native": 0,
    "Black": 2,
    "Hispanic": 3,
    "Other": 4,
    "White": 5
}

# --- Fungsi Mapping Umur ke Kategori ---
def map_age_to_category(age: int) -> int:
    if age < 25:
        return 0
    elif age < 30:
        return 1
    elif age < 35:
        return 2
    elif age < 40:
        return 3
    elif age < 45:
        return 4
    elif age < 50:
        return 5
    elif age < 55:
        return 6
    elif age < 60:
        return 7
    elif age < 65:
        return 8
    elif age < 70:
        return 9
    elif age < 75:
        return 10
    elif age < 80:
        return 11
    else:
        return 12

# --- Prepare fitur sesuai model ---
def prepare_features_for_model(data: dict, debug=False) -> dict:
    try:
        height = float(data.get("Height (cm)", 0))
        weight = float(data.get("Weight (kg)", 0))
        bmi = 0
        if height > 0:
            bmi = weight / ((height / 100) ** 2)

        features = {
            "BMI": bmi,
            "Smoking": int(data.get("Smoking", False)),
            "AlcoholDrinking": int(data.get("Alcohol Drinking", False)),
            "Stroke": int(data.get("Stroke", False)),
            "PhysicalHealth": int(data.get("Physical Health Days", 0)),
            "MentalHealth": int(data.get("Mental Health Days", 0)),
            "DiffWalking": int(data.get("Difficulty Walking", False)),
            "Sex": gender_map.get(data.get("Gender", "Male"), -1),
            "AgeCategory": map_age_to_category(int(data.get("Age", 0))),
            "Race": race_map.get(data.get("Race", "White"), -1),
            "Diabetic": diabetic_map.get(data.get("Diabetic", "No"), -1),
            "PhysicalActivity": int(data.get("Physical Activity", False)),
            "GenHealth": genhealth_map.get(data.get("General Health", "Good"), -1),
            "SleepTime": float(data.get("Sleep Time (hours)", 7)),
            "Asthma": int(data.get("Asthma", False)),
            "KidneyDisease": int(data.get("Kidney Disease", False)),
            "SkinCancer": int(data.get("Skin Cancer", False))
        }

        if debug:
            print("Prepared features:", features)

        return features

    except Exception as e:
        raise ValueError(f"Error preparing features: {e}")

# --- Validasi Input ---
def validate_patient_data(features: dict):
    required_keys = [
        "BMI", "Smoking", "AlcoholDrinking", "Stroke", "PhysicalHealth", "MentalHealth",
        "DiffWalking", "Sex", "AgeCategory", "Race", "Diabetic", "PhysicalActivity",
        "GenHealth", "SleepTime", "Asthma", "KidneyDisease", "SkinCancer"
    ]

    missing_keys = [k for k in required_keys if k not in features]
    if missing_keys:
        raise ValueError(f"Missing keys in input data: {missing_keys}")

    # Contoh validasi tipe data sederhana
    for key in required_keys:
        if not isinstance(features[key], (int, float)):
            raise TypeError(f"Invalid type for {key}: expected int or float, got {type(features[key])}")

# --- Fungsi Prediksi ---
def predict_patient_risk(patient_data: dict, debug=False):
    if model is None:
        raise RuntimeError("Model not loaded.")

    features = prepare_features_for_model(patient_data, debug=debug)
    validate_patient_data(features)

    df = pd.DataFrame([features])

    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    if debug:
        print(f"Prediction: {prediction}, Probability: {prob}")

    return prediction, prob
