import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import joblib
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

# Membaca dataset
file_path = '../dataset/bike_fitting_dataset.csv'
data = pd.read_csv(file_path)

# Fitur dan target
fitur = ['Tinggi_Badan', 'Inseam', 'Torso', 'Lengan', 'Bahu']
target = ['Frame', 'Saddle', 'Crank', 'Handlebar', 'Stem']

X = data[fitur]
y = data[target]

# Split data untuk training dan testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membuat model Decision Tree
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluasi performa model
prediksi = model.predict(X_test)
prediksi = pd.DataFrame(prediksi, columns=target)
prediksi['Frame'] = prediksi['Frame'].round().astype(int)
mae = mean_absolute_error(y_test, prediksi)
r2 = r2_score(y_test, prediksi)
mse = mean_squared_error(y_test, prediksi)
rmse = np.sqrt(mean_squared_error(y_test, prediksi))

# Performa model
print(f'Performa Model:')
print(f'- Mean Absolute Error (MAE): {mae:.2f}')
print(f'- Mean Squared Error (MSE): {mse:.2f}')
print(f'- Root Mean Squared Error (RMSE): {rmse:.2f}')
print(f'- R^2 Score: {r2:.2f}')

# Simpan model
joblib.dump(model, 'bike_fitting_model.pkl')

print('Model berhasil dilatih dan disimpan sebagai bike_fitting_model.pkl') 