from flask import Flask, request, render_template, jsonify
from flask_cors import CORS 
import joblib
import numpy as np
import pandas as pd


app = Flask(__name__)
CORS(app)

# Load semua model
models = {
    'Frame': joblib.load('models/model_Frame.pkl'),
    'Stem': joblib.load('models/model_Stem.pkl'),
    'Handlebar': joblib.load('models/model_Handlebar.pkl'),
    'Crank': joblib.load('models/model_Crank.pkl'),
    'Saddle': joblib.load('models/model_Saddle.pkl'),
}

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

        print("Data diterima:", data)  # Debugging

        input_data = pd.DataFrame([{
            'Tinggi_Badan': data['tinggi'],
            'Inseam': data['inseam'],
            'Torso': data['torso'],
            'Lengan': data['lengan'],
            'Bahu': data['bahu']
        }])
        
        output = {key: models[key].predict(input_data)[0] for key in models}
        print("Output prediksi:", output)  # Debugging
        return jsonify(output)
    
    except Exception as e:
        print("Terjadi error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
