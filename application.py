import streamlit as st
import numpy as np
import pickle

# Load model and scaler
ridge = pickle.load(open('models/best_model_ridge.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

st.markdown(
    "<h2 style='text-align: center; color: #388e3c;'>Forest Fire Weather Index (FWI) Prediction</h2>",
    unsafe_allow_html=True
)

with st.container():
    st.markdown(
        """
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 20px; border: 1px solid #e0e0e0;">
        <h5>About This Project</h5>
        <p>
            This web application predicts the <b>Forest Fire Weather Index (FWI)</b> for Algerian forests using weather and environmental data.
            The FWI is a numeric rating of fire intensity, widely used for fire danger assessment.
        </p>
        <h6>Dataset Information</h6>
        <p>
            The model is trained on the <b>Algerian Forest Fires Dataset</b>, which contains weather observations and fire records from two regions in Algeria (Bejaia and Sidi-Bel Abbes) for the summer of 2012.
            You can enter weather and region details below to estimate the FWI for your scenario.
        </p>
        <ul>
            <li><b>Temperature</b>: Noon temperature in °C</li>
            <li><b>RH</b>: Relative Humidity (%)</li>
            <li><b>Ws</b>: Wind Speed (km/h)</li>
            <li><b>Rain</b>: Rainfall (mm)</li>
            <li><b>FFMC, DMC, ISI</b>: Fire weather indices</li>
            <li><b>Classes</b>: 0 = Not Fire, 1 = Fire (means whether a fire occurred)</li>
            <li><b>Region</b>: 0 = Bejaia, 1 = Sidi-Bel Abbes</li>
        </ul>
        <b>Enter your data below to get a prediction!</b>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        temp = st.number_input('Temperature (°C, e.g. 10-40)', min_value=0.0, max_value=50.0, step=0.1)
        rain = st.number_input('Rain (mm, e.g. 0-20)', min_value=0.0, max_value=50.0, step=0.1)
        isi = st.number_input('ISI (Initial Spread Index, 0-50)', min_value=0.0, max_value=50.0, step=0.1)
    with col2:
        rh = st.number_input('Relative Humidity (RH, %, 0-100)', min_value=0.0, max_value=100.0, step=0.1)
        ffmc = st.number_input('FFMC (Fine Fuel Moisture Code, 0-101)', min_value=0.0, max_value=101.0, step=0.1)
        classes = st.selectbox('Classes (0=Not Fire, 1=Fire)', [0, 1])
    with col3:
        ws = st.number_input('Wind Speed (Ws, km/h, e.g. 0-50)', min_value=0.0, max_value=100.0, step=0.1)
        dmc = st.number_input('DMC (Duff Moisture Code, 0-220)', min_value=0.0, max_value=220.0, step=0.1)
        region = st.selectbox('Region (0=Bejaia, 1=Sidi-Bel Abbes)', [0, 1])

    submitted = st.form_submit_button("Predict")

if submitted:
    try:
        input_data = np.array([[temp, rh, ws, rain, ffmc, dmc, isi, classes, region]])
        input_scaled = scaler.transform(input_data)
        result = ridge.predict(input_scaled)[0]
        st.success(f"Predicted FWI: {round(result, 3)}")
    except Exception as e:
        st.error(f"Error: {e}")