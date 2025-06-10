import streamlit as st
import numpy as np
import pickle

# Load model and scaler
ridge = pickle.load(open('models/best_model_ridge.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

st.title("Fire Area Prediction App")

# Input fields
temp = st.number_input('Temperature')
rh = st.number_input('Relative Humidity (RH)')
ws = st.number_input('Wind Speed (Ws)')
rain = st.number_input('Rain')
ffmc = st.number_input('FFMC')
dmc = st.number_input('DMC')
isi = st.number_input('ISI')
classes = st.number_input('Classes', step=1)
region = st.number_input('Region', step=1)

if st.button('Predict'):
    try:
        input_data = np.array([[temp, rh, ws, rain, ffmc, dmc, isi, classes, region]])
        input_scaled = scaler.transform(input_data)
        result = ridge.predict(input_scaled)[0]
        st.success(f"Predicted Fire Area: {round(result, 3)}")
    except Exception as e:
        st.error(f"Error: {e}")
