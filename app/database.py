import logging
import streamlit as st
from st_supabase_connection import SupabaseConnection

def get_connection():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to Supabase: {e}")
        raise

def upsert_patient_data(data):
    try:
        conn = get_connection()

        field_mapping = {
            "Name": "name",
            "Phone Number": "phone",
            "Email": "email",
            "Height (cm)": "height",
            "Weight (kg)": "weight",
            "Gender": "gender",
            "Age": "age",
            "Age Category": "age_category",
            "Race": "race",
            "Smoking": "smoking",
            "Alcohol Drinking": "alcohol",
            "Stroke": "stroke",
            "Difficulty Walking": "diff_walking",
            "Diabetic": "diabetic",
            "Physical Activity": "physical_activity",
            "Asthma": "asthma",
            "Kidney Disease": "kidney_disease",
            "Skin Cancer": "skin_cancer",
            "General Health": "general_health",
            "Sleep Time (hours)": "sleep_time",
            "Physical Health Days": "physical_health_days",
            "Mental Health Days": "mental_health_days",
            "risk_prediction": "risk_prediction",
            "risk_probability": "risk_probability"
        }
        print(data.items())
        mapped_data = {field_mapping[k]: v for k, v in data.items() if k in field_mapping}

        print(mapped_data)

        # Upsert (insert or update) based on phone and email
        response = conn.table("patients").upsert(mapped_data, on_conflict=["phone", "email"]).execute()
        if hasattr(response, "status_code") and response.status_code >= 400:
            raise Exception(f"Supabase upsert error: {response}")
        logging.info("Upsert (insert/update) data pasien berhasil.")
    except Exception as e:
        logging.error(f"Upsert gagal: {e}")
        raise

def fetch_all_patient_data():
    try:
        conn = get_connection()
        response = conn.table("patients").select("*").execute()
        if hasattr(response, "status_code") and response.status_code >= 400:
            raise Exception(f"Supabase fetch error: {response}")
        data = response.data
        return data
    except Exception as e:
        logging.error(f"Gagal mengambil data: {e}")
        raise