import pandas as pd
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dan pastikan dataset sudah dalam cm semua
df = pd.read_csv('bike_fitting_dataset.csv')

# Fitur
X = df[['Tinggi_Badan', 'Inseam', 'Torso', 'Lengan', 'Bahu']]

# ========================
# MODEL 1: Ukuran Frame
# ========================
y_frame = df['Frame']
X_train, X_test, y_train, y_test = train_test_split(X, y_frame, random_state=42)
model_frame = DecisionTreeRegressor()
model_frame.fit(X_train, y_train)
joblib.dump(model_frame, 'model_Frame.pkl')

# ========================
# MODEL 2: Ukuran Stem
# ========================
y_stem = df['Stem']
X_train, X_test, y_train, y_test = train_test_split(X, y_stem, random_state=42)
model_stem = DecisionTreeRegressor()
model_stem.fit(X_train, y_train)
joblib.dump(model_stem, 'model_Stem.pkl')

# ========================
# MODEL 3: Ukuran Handlebar
# ========================
y_handlebar = df['Handlebar']
X_train, X_test, y_train, y_test = train_test_split(X, y_handlebar, random_state=42)
model_handlebar = DecisionTreeRegressor()
model_handlebar.fit(X_train, y_train)
joblib.dump(model_handlebar, 'model_Handlebar.pkl')

# ========================
# MODEL 4: Ukuran Crank
# ========================
y_crank = df['Crank']
X_train, X_test, y_train, y_test = train_test_split(X, y_crank, random_state=42)
model_crank = DecisionTreeRegressor()
model_crank.fit(X_train, y_train)
joblib.dump(model_crank, 'model_Crank.pkl')

# ========================
# MODEL 5: Saddle Height (jika ada)
# ========================
y_saddle = df['Saddle']
X_train, X_test, y_train, y_test = train_test_split(X, y_saddle, random_state=42)
model_saddle = DecisionTreeRegressor()
model_saddle.fit(X_train, y_train)
joblib.dump(model_saddle, 'model_Saddle.pkl')


# ========================
# MODEL 6: Merek Sepeda (jika ada)
# ========================
y_merek = df['Merek']
X_train, X_test, y_train, y_test = train_test_split(X, y_merek, random_state=42)
model_merek = DecisionTreeClassifier()
model_merek.fit(X_train, y_train)
joblib.dump(model_merek, 'model_Merek.pkl')


# ========================
# MODEL 7: Type Sepeda (jika ada)
# ========================
y_tipe = df['Tipe']
X_train, X_test, y_train, y_test = train_test_split(X, y_tipe, random_state=42)
model_tipe = DecisionTreeClassifier()
model_tipe.fit(X_train, y_train)
joblib.dump(model_tipe, 'model_Tipe.pkl')