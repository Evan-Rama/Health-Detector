from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import os
import logging

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        raise

def upsert_patient_data(data):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()

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
            "Diff Walking": "diff_walking",
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

        columns = [field_mapping[k] for k in data.keys() if k in field_mapping]
        values = [data[k] for k in data.keys() if k in field_mapping]

        unique_keys = ['phone', 'email']
        update_columns = [col for col in columns if col not in unique_keys]

        insert_query = sql.SQL("""
            INSERT INTO patients ({fields})
            VALUES ({placeholders})
            ON CONFLICT (phone, email)
            DO UPDATE SET {updates}
        """).format(
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(columns)),
            updates=sql.SQL(', ').join(
                sql.Composed([
                    sql.Identifier(col), sql.SQL(" = EXCLUDED."), sql.Identifier(col)
                ]) for col in update_columns
            )
        )

        # Debug log
        print("SQL:", insert_query.as_string(conn))  # debug
        print("Values:", values)

        cur.execute(insert_query, values)
        conn.commit()
        logging.info("Upsert (insert/update) data pasien berhasil.")
    except Exception as e:
        logging.error(f"Upsert gagal: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
