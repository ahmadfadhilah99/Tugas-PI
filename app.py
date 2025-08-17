from flask import Flask, request, render_template, jsonify, session, redirect, flash, send_file, make_response
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import csv
import os
from io import StringIO, BytesIO

app = Flask(__name__)
app.secret_key = 'Mi3@y4M_H3113' 


# Memanggil 4 model terpisah
frame_model = joblib.load('models/frame_model.pkl')
stem_model = joblib.load('models/stem_model.pkl')
handlebar_model = joblib.load('models/handlebar_model.pkl')
saddle_model = joblib.load('models/saddle_model.pkl')

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
        
        # Prediksi menggunakan 4 model terpisah
        frame_pred = frame_model.predict(input_data)[0]
        stem_pred = stem_model.predict(input_data)[0]
        handlebar_pred = handlebar_model.predict(input_data)[0]
        saddle_pred = saddle_model.predict(input_data)[0]

        # Load model scores
        try:
            scores = joblib.load('models/model_scores.pkl')
            model_scores = {
                'Frame': f"{scores['frame_accuracy']*100:.1f}%",
                'Stem': f"{scores['stem_accuracy']*100:.1f}%",
                'Handlebar': f"{scores['handlebar_accuracy']*100:.1f}%",
                'Saddle': f"{scores['saddle_mae']:.2f} cm MAE"
            }
        except:
            model_scores = {
                'Frame': 'N/A',
                'Stem': 'N/A', 
                'Handlebar': 'N/A',
                'Saddle': 'N/A'
            }

        output = {
            'Nama': data['nama'],
            'Usia': data['usia'],
            'noTlp': data['noTlp'],
            'Frame': int(frame_pred),
            'Saddle': round(saddle_pred, 1),
            'Crank': 170,  # Nilai tetap dari datasets
            'Stem': int(stem_pred),
            'Handlebar': int(handlebar_pred),
            'model_scores': model_scores
        }
        
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save', methods=['POST'])
def save_recommendation():
    try:
        data = request.json
        
        # Validasi data yang diperlukan
        required_fields = ['nama', 'usia', 'noTlp', 'tinggi', 'inseam', 'lengan', 'torso', 'bahu', 'Frame', 'Saddle', 'Crank', 'Stem', 'Handlebar']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} diperlukan'}), 400
        
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama": data['nama'],
            "usia": data['usia'],
            "noTlp": data['noTlp'],
            "tinggi": data['tinggi'],
            "inseam": data['inseam'],
            "lengan": data['lengan'],
            "torso": data['torso'],
            "bahu": data['bahu'],
            "Frame": data['Frame'],
            "Saddle": data['Saddle'],
            "Crank": data['Crank'],
            "Stem": data['Stem'],
            "Handlebar": data['Handlebar']
        }
        
        file_path = 'datasets/riwayat_rekomendasi.csv'
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        
        return jsonify({'message': 'Data berhasil disimpan'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_recommendations():
    try:
        data = request.json
        phone_number = data.get('noTlp', '').strip()
        
        if not phone_number:
            return jsonify({'error': 'Nomor telepon diperlukan'}), 400
        
        file_path = 'datasets/riwayat_rekomendasi.csv'
        if not os.path.isfile(file_path):
            return jsonify({'recommendations': []})
        
        recommendations = []
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if str(row.get('noTlp', '')).strip() == phone_number:
                    recommendations.append(row)
        
        # Sort by timestamp descending (newest first)
        recommendations.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Login admin

USER_CSV = 'datasets/users.csv'

# --- Helper: Cek login ---
def check_user(username, password):
    if not os.path.exists(USER_CSV):
        return False
    with open(USER_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

# --- Helper: Cek apakah user sudah login ---
def is_logged_in():
    return 'username' in session

# --- Route: Halaman Utama → Arahkan ke login
@app.route('/admin/auth')
def session_check():
    if is_logged_in():
        return redirect('/admin/dashboard')
    return redirect('/admin/auth/login')

# --- Route: Login
@app.route('/admin/auth/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/admin/dashboard')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_user(username, password):
            session['username'] = username
            return redirect('/admin/dashboard')
        else:
            flash("Username atau password salah.")
    
    return render_template('login.html')

# --- Route: Dashboard
def get_recommendations(limit=None):
    """Get recommendations from CSV file"""
    file_path = 'datasets/riwayat_rekomendasi.csv'
    recommendations = []
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            recommendations = list(reader)
    
    # Sort by timestamp descending (newest first)
    recommendations.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Apply limit if specified
    if limit and len(recommendations) > limit:
        return recommendations[:limit]
    return recommendations

@app.route('/admin/dashboard')
def dashboard():
    if not is_logged_in():
        flash("Silakan login terlebih dahulu.")
        return redirect('/admin/auth/login')
    
    # Get recommendations (show last 10 by default)
    recommendations = get_recommendations(limit=10)
    
    # Count total recommendations
    total_recommendations = len(get_recommendations())
    
    return render_template('dashboard.html', 
                         user=session['username'],
                         recommendations=recommendations,
                         total_recommendations=total_recommendations)

@app.route('/admin/export')
def export_data():
    if not is_logged_in():
        return redirect('/admin/auth/login')
    
    # Get all recommendations
    recommendations = get_recommendations()
    
    if not recommendations:
        flash("Tidak ada data yang dapat diekspor", "warning")
        return redirect('/admin/dashboard')
    
    # Create a string buffer
    si = StringIO()
    
    # Create a CSV writer
    keys = recommendations[0].keys()
    writer = csv.DictWriter(si, fieldnames=keys)
    
    # Write header and data
    writer.writeheader()
    writer.writerows(recommendations)
    
    # Create a response with the CSV data
    output = make_response(si.getvalue())
    
    # Set the filename with current date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"rekomendasi_sepeda_{today}.csv"
    
    # Set headers for file download
    output.headers["Content-Disposition"] = f"attachment; filename={filename}"
    output.headers["Content-type"] = "text/csv; charset=utf-8"
    
    return output

# --- Route: Logout
@app.route('/admin/auth/logout')
def logout():
    session.pop('username', None)
    flash("Anda berhasil logout.")
    return redirect('/admin/auth/login')


if __name__ == '__main__':
    app.run(debug=True)
