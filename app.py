import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Patient Data Form",
    page_icon="🏥",
    layout="centered"
)

# Custom CSS for better styling
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

# Title
st.markdown("<div class='main-header'>Patient Data Form</div>", unsafe_allow_html=True)

# Initialize session state for form data
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Create a form
with st.form("patient_data_form"):
    # Section 1: Patient Identity
    st.markdown("<div class='section-header'>1. Identitas Pasien</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Informasi dasar tentang pasien</div>", unsafe_allow_html=True)
    
    name = st.text_input("Nama", help="Masukkan nama lengkap")
    phone_number = st.text_input("Nomor Telepon", help="Masukkan nomor telepon")
    email = st.text_input("Email", help="Masukkan alamat email")
    
    # Section 2: Physical Data
    st.markdown("<div class='section-header'>2. Data Fisik</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Informasi fisik pasien</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Tinggi Badan (cm)", min_value=50, max_value=250, help="Masukkan tinggi badan dalam cm")
    with col2:
        weight = st.number_input("Berat Badan (kg)", min_value=3, max_value=300, help="Masukkan berat badan dalam kg")
    
    gender = st.selectbox(
        "Gender",
        options=["", "Laki-laki", "Perempuan"],
        format_func=lambda x: "Pilih gender" if x == "" else x,
        help="Pilih gender"
    )
    
    age = st.number_input("Age", min_value=0, max_value=120, help="Enter age")
    
    race = st.selectbox(
        "Race",
        options=["", "American Indian/Alaskan Native", "Black", "Hispanic", "White", "Other"],
        format_func=lambda x: "Select race" if x == "" else x,
        help="Select race"
    )
    
    # Section 3: Health History
    st.markdown("<div class='section-header'>3. Riwayat Kesehatan dan Gaya Hidup</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Informasi tentang riwayat kesehatan pasien</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        smoking = st.checkbox("Smoking")
        stroke = st.checkbox("Stroke")
        diabetic = st.checkbox("Diabetic")
        asthma = st.checkbox("Asthma")
        skin_cancer = st.checkbox("Skin Cancer")
    
    with col2:
        alcohol_drinking = st.checkbox("Alcohol Drinking")
        diff_walking = st.checkbox("Diff Walking (Kesulitan berjalan)")
        physical_activity = st.checkbox("Physical Activity")
        kidney_disease = st.checkbox("Kidney Disease")
    
    genhealth = st.selectbox(
        "General Health",
        options=["", "Excellent", "Very Good", "Good", "Fair", "Poor"],
        format_func=lambda x: "Select general health status" if x == "" else x,
        help="Select your general health status"
    )
    
    sleep_time = st.number_input("Sleep Time (hours per day)", min_value=0, max_value=24, step=1, help="Enter sleep time in hours")
    
    # Section 4: Physical Health
    st.markdown("<div class='section-header'>4. Kesehatan Fisik</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-description'>Informasi tentang kesehatan fisik dan mental pasien</div>", unsafe_allow_html=True)
    
    physical_health_days = st.slider(
        "Physical Health (days per month with health problems)",
        min_value=0,
        max_value=31,
        step=1,
        help="Select the number of days you experienced physical health problems in the past month"
    )
    
    mental_health_days = st.slider(
        "Mental Health (days per month with mental health problems)",
        min_value=0,
        max_value=31,
        step=1,
        help="Select the number of days you experienced mental health problems in the past month"
    )
    
    # Submit button
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # Validate required fields
        required_fields = {
            "Nama": name,
            "Nomor Telepon": phone_number,
            "Email": email,
            "Gender": gender,
            "Race": race,
            "General Health": genhealth
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
        else:
            # Create a dictionary with all form data
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
                "Diff Walking": diff_walking,
                "Diabetic": diabetic,
                "Physical Activity": physical_activity,
                "Asthma": asthma,
                "Kidney Disease": kidney_disease,
                "Skin Cancer": skin_cancer,
                "General Health": genhealth,
                "Sleep Time (hours)": sleep_time,
                "Physical Health Days": physical_health_days,
                "Mental Health Days": mental_health_days
            }
            
            # Convert to DataFrame for display
            df = pd.DataFrame([form_data])
            
            # Set session state to indicate form was submitted
            st.session_state.form_submitted = True
            st.session_state.form_data = form_data
            
            st.success("Form submitted successfully!")
            
            # Calculate BMI if height and weight are provided
            if height > 0 and weight > 0:
                bmi = weight / ((height/100) ** 2)
                st.session_state.bmi = bmi
            
            # Store data in session state
            st.session_state.df = df

# Display submitted data if form was submitted
if st.session_state.form_submitted:
    st.markdown("<div class='section-header'>Submitted Data</div>", unsafe_allow_html=True)
    
    # Display BMI if calculated
    if 'bmi' in st.session_state:
        bmi = st.session_state.bmi
        st.markdown(f"**BMI:** {bmi:.2f}")
        
        # BMI categories
        if bmi < 18.5:
            st.markdown("**Category:** Underweight")
        elif bmi < 25:
            st.markdown("**Category:** Normal weight")
        elif bmi < 30:
            st.markdown("**Category:** Overweight")
        else:
            st.markdown("**Category:** Obesity")
    
    # Display the DataFrame
    st.dataframe(st.session_state.df)
    
    # Option to download data as CSV
    csv = st.session_state.df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="patient_data.csv",
        mime="text/csv"
    )

# Add a footer
st.markdown("---")
st.markdown("© 2025 Patient Data Collection System")