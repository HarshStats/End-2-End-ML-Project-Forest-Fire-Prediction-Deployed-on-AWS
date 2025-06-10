from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import os

application = Flask(__name__)
app=application

#import ridge regressor and standard scaler pickle


ridge = pickle.load(open('models/best_model_ridge.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'POST':
        try:
            temp = float(request.form.get('Temperature'))
            rh = float(request.form.get('RH'))
            ws = float(request.form.get('Ws'))
            rain = float(request.form.get('Rain'))
            ffmc = float(request.form.get('FFMC'))
            dmc = float(request.form.get('DMC'))
            isi = float(request.form.get('ISI'))
            classes = int(request.form.get('Classes'))
            region = int(request.form.get('Region'))

            input_data = np.array([[temp, rh, ws, rain, ffmc, dmc, isi, classes, region]])
            input_scaled = scaler.transform(input_data)
            result = ridge.predict(input_scaled)[0]
            result = round(result, 3)

            return render_template('home.html', result=result)
        except Exception as e:
            return render_template('home.html', result=f"Error: {e}")
        
    return render_template('home.html', result=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

