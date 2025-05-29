import streamlit as st
import pandas as pd
from database import fetch_all_patient_data

# --- Page Configuration ---
st.set_page_config(
    page_title="View Patient Data",
    page_icon="📋",
    layout="wide"
)

# --- Title ---
st.title("📋 View Patient Data")
st.markdown("Below is the list of all patients stored in the database.")

# --- Fetch data ---
try:
    data = fetch_all_patient_data()

    if data and len(data) > 0:
        df = pd.DataFrame(data)

        # Ubah risk_prediction dari 0/1 ke NO RISK/RISK untuk tampilan
        if 'risk_prediction' in df.columns:
            df['risk_prediction'] = df['risk_prediction'].map({'0': "NO RISK", '1': "RISK"})
            print(df['risk_prediction'])

        # Format column names (optional)
        df.columns = [col.replace("_", " ").title() for col in df.columns]

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="all_patient_data.csv", mime="text/csv")

    else:
        st.info("No data found in the database.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
