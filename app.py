from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import csv
import os


app = Flask(__name__)
model = joblib.load('models/bike_fitting_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')


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
        data_input = {
            "tinggi": data['tinggi'],
            "inseam": data['inseam'],
            "lengan": data['lengan'],
            "torso": data['torso'],
            "bahu": data['bahu']
        }
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **data_input,
            **output
        }
        file_path = 'dataset/riwayat_rekomendasi.csv'
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
