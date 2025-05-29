import streamlit as st
import pandas as pd
from database import upsert_patient_data
from model import predict_patient_risk, map_age_to_category
import os

# --- Inisialisasi session state ---
if "form_data" not in st.session_state:
    st.session_state.form_data = None
if "df" not in st.session_state:
    st.session_state.df = None
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# --- Page Configuration ---
st.set_page_config(
    page_title="Patient Data Form",
    page_icon="🏥",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .section-description {
        font-size: 1rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<div class='main-header'>Patient Data Form</div>", unsafe_allow_html=True)

with st.form("patient_data_form"):
    # --- Section 1: Identity ---
    st.markdown("<div class='section-header'>1. Patient Identity</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Basic information about the patient</div>", unsafe_allow_html=True)

    name = st.text_input("Name")
    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email")

    # --- Section 2: Physical Data ---
    st.markdown("<div class='section-header'>2. Physical Data</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Physical attributes of the patient</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (cm)", min_value=50, max_value=250)
    with col2:
        weight = st.number_input("Weight (kg)", min_value=3, max_value=300)

    gender = st.selectbox("Gender", ["", "Male", "Female"], format_func=lambda x: "Select gender" if x == "" else x)
    age = st.number_input("Age", min_value=0, max_value=120)
    race = st.selectbox("Race", ["", "American Indian/Alaskan Native", "Black", "Hispanic", "White", "Other"], format_func=lambda x: "Select race" if x == "" else x)

    # --- Section 3: Health History ---
    st.markdown("<div class='section-header'>3. Health History</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        smoking = st.checkbox("Smoking")
        stroke = st.checkbox("Stroke")
        asthma = st.checkbox("Asthma")
        skin_cancer = st.checkbox("Skin Cancer")
    with col2:
        alcohol_drinking = st.checkbox("Alcohol Drinking")
        diff_walking = st.checkbox("Difficulty Walking")
        physical_activity = st.checkbox("Physical Activity")
        kidney_disease = st.checkbox("Kidney Disease")

    diabetic = st.selectbox("Diabetic", ["", "No", "No, Borderline Diabetes", "Yes", "Yes (during pregnancy)"], format_func=lambda x: "Select status" if x == "" else x)
    genhealth = st.selectbox("General Health", ["", "Excellent", "Very Good", "Good", "Fair", "Poor"], format_func=lambda x: "Select status" if x == "" else x)
    sleep_time = st.number_input("Sleep Time (hours per day)", 0, 16, step=1)

    # --- Section 4: Health Days ---
    st.markdown("<div class='section-header'>4. Health Status</div>", unsafe_allow_html=True)
    physical_health_days = st.slider("Physical Health (days per month)", 0, 31, 0)
    mental_health_days = st.slider("Mental Health (days per month)", 0, 31, 0)

    submitted = st.form_submit_button("Submit")

    if submitted:
        required_fields = {
            "Name": name,
            "Phone Number": phone_number,
            "Email": email,
            "Gender": gender,
            "Race": race,
            "General Health": genhealth
        }
        missing = [k for k, v in required_fields.items() if not v]

        if missing:
            st.error(f"Please complete the following fields: {', '.join(missing)}")
        else:
            form_data = {
                "Name": name,
                "Phone Number": phone_number,
                "Email": email,
                "Height (cm)": height,
                "Weight (kg)": weight,
                "Gender": gender,
                "Age": age,
                "Race": race,
                "Smoking": smoking,
                "Alcohol Drinking": alcohol_drinking,
                "Stroke": stroke,
                "Difficulty Walking": diff_walking,
                "Diabetic": diabetic,
                "Physical Activity": physical_activity,
                "Asthma": asthma,
                "Kidney Disease": kidney_disease,
                "Skin Cancer": skin_cancer,
                "General Health": genhealth,
                "Sleep Time (hours)": sleep_time,
                "Physical Health Days": physical_health_days,
                "Mental Health Days": mental_health_days,
            }

            df = pd.DataFrame([form_data])
            st.session_state.form_data = form_data
            st.session_state.df = df
            st.session_state.form_submitted = True

            st.success("Form submitted successfully!")

# --- After Submit: show results and prediction ---
if st.session_state.form_submitted and st.session_state.df is not None:
    st.markdown("<div class='section-header'>Results & Prediction</div>", unsafe_allow_html=True)
    df = st.session_state.df

    if 'Height (cm)' in df.columns and 'Weight (kg)' in df.columns:
        height = df["Height (cm)"][0]
        weight = df["Weight (kg)"][0]
        bmi = weight / ((height / 100) ** 2)
        st.markdown(f"**BMI:** {bmi:.2f}")

    try:
        prediction, prob = predict_patient_risk(st.session_state.form_data)
        pred_label = "AT RISK" if prediction == 1 else "NOT AT RISK"
        st.markdown(f"**Prediction Result:** {pred_label}")
        st.markdown(f"**Risk Probability:** {prob:.2%}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")

    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="patient_data.csv", mime="text/csv")

    # --- Save to database section, hanya tampil jika form sudah submit ---
    if st.checkbox("Save to database"):
        if st.button("Confirm and Save"):
            try:
                form_data = st.session_state.form_data

                # Tambahkan prediksi ke data
                prediction, prob = predict_patient_risk(form_data)
                form_data["risk_prediction"] = int(prediction)
                form_data["risk_probability"] = float(prob)

                # Tambahkan age_category numerik sesuai model
                form_data["Age Category"] = map_age_to_category(int(form_data["Age"]))
                print(form_data)
                upsert_patient_data(form_data)
                st.success("Data successfully saved to the database.")
                st.session_state.reset_form = True
            except Exception as e:
                st.error(f"Failed to save data to the database: {e}")

# --- Reset form and session state ---
if st.session_state.get("reset_form", False):
    keys_to_clear = ["form_data", "df", "form_submitted", "reset_form"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Patient Data Collection System")
