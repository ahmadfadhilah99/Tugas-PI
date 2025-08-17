import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error

# --- 1. Baca datasets ---
file_path = '../datasets/bike_fitting_datasets.csv'
df = pd.read_csv(file_path)
print("Data siap digunakan:")
print(df.head())

# --- 2. Pisah Fitur dan Target ---
X = df[['Tinggi_Badan', 'Inseam', 'Torso', 'Lengan', 'Bahu']]

y_frame = df['Frame']
y_stem = df['Stem']
y_handlebar = df['Handlebar']
y_saddle = df['Saddle']

# --- 3. Bagi Data: Latih (80%) dan Uji (20%) ---
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

# Split target masing-masing
y_frame_train, y_frame_test = train_test_split(y_frame, test_size=0.2, random_state=42)
y_stem_train, y_stem_test = train_test_split(y_stem, test_size=0.2, random_state=42)
y_handlebar_train, y_handlebar_test = train_test_split(y_handlebar, test_size=0.2, random_state=42)
y_saddle_train, y_saddle_test = train_test_split(y_saddle, test_size=0.2, random_state=42)

# --- 4. Latih Model ---
# Klasifikasi untuk Frame, Stem, Handlebar
clf_frame = DecisionTreeClassifier(random_state=42)
clf_stem = DecisionTreeClassifier(random_state=42)
clf_handlebar = DecisionTreeClassifier(random_state=42)

clf_frame.fit(X_train, y_frame_train)
clf_stem.fit(X_train, y_stem_train)
clf_handlebar.fit(X_train, y_handlebar_train)

# Regresi untuk Saddle (nilai kontinu)
reg_saddle = DecisionTreeRegressor(random_state=42)
reg_saddle.fit(X_train, y_saddle_train)

# --- 5. Evaluasi Model ---
frame_pred = clf_frame.predict(X_test)
stem_pred = clf_stem.predict(X_test)
handlebar_pred = clf_handlebar.predict(X_test)
saddle_pred = reg_saddle.predict(X_test)

scores = {
    'frame_accuracy': accuracy_score(y_frame_test, frame_pred),
    'stem_accuracy': accuracy_score(y_stem_test, stem_pred),
    'handlebar_accuracy': accuracy_score(y_handlebar_test, handlebar_pred),
    'saddle_mae': mean_absolute_error(y_saddle_test, saddle_pred)
}

print("\n📊 Performa Model:")
for k, v in scores.items():
    print(f"  {k}: {v:.3f}")

# --- 6. Simpan Model dan Skor ---
joblib.dump(clf_frame, 'frame_model.pkl')
joblib.dump(clf_stem, 'stem_model.pkl')
joblib.dump(clf_handlebar, 'handlebar_model.pkl')
joblib.dump(reg_saddle, 'saddle_model.pkl')
joblib.dump(scores, 'model_scores.pkl')

print("\n✅ Semua model dan skor berhasil disimpan di folder 'models/'")

# --- 7. Contoh Prediksi ---
print(f'\nContoh Prediksi (5 data pertama):')
print("Frame | Stem | Handlebar | Saddle")
for i in range(min(5, len(frame_pred))):
    print(f"{frame_pred[i]:5.0f} | {stem_pred[i]:4.0f} | {handlebar_pred[i]:9.0f} | {saddle_pred[i]:6.1f}")

print('Model berhasil dilatih dan disimpan!') 