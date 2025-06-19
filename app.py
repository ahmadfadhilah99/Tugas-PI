from flask import Flask, request, render_template, jsonify
from flask_cors import CORS 
import joblib
import numpy as np
import pandas as pd


app = Flask(__name__)
CORS(app)

model = joblib.load('models/bike_fitting_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

@app.route('/fitting')
def fitting():
    return render_template('fitting.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        input_data = pd.DataFrame([{
            'Tinggi_Badan': data['tinggi'],
            'Inseam': data['inseam'],
            'Torso': data['torso'],
            'Lengan': data['lengan'],
            'Bahu': data['bahu']
        }])
        # Prediksi, misal hasilnya array: [Frame, Saddle, Crank, Stem, Handlebar]
        hasil = model.predict(input_data)[0]
        # Misal urutannya: Frame, Saddle, Crank, Stem, Handlebar
        crank_mm = hasil[2] * 10
        handlebar_mm = hasil[3] * 10
        stem_mm = hasil[4] * 10

        output = {
            'Frame': hasil[0],
            'Saddle': round(hasil[1], 2),
            'Crank': round(crank_mm, 0),
            'Stem': round(stem_mm, 0),
            'Handlebar': round(handlebar_mm, 0)
        }
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
