import pandas as pd
import numpy as np

# Baca data asli
data = pd.read_csv('bike_fitting_dataset.csv')

# List untuk menyimpan data sintetis
data_sintetis = []

for idx, row in data.iterrows():
    # Data asli tetap dimasukkan
    data_sintetis.append(row)
    for _ in range(2):  # Buat 2 data sintetis per baris
        new_row = row.copy()
        # Variasi fitur ±2%
        for col in ['Tinggi_Badan', 'Inseam', 'Torso', 'Lengan', 'Bahu']:
            variation = np.random.uniform(-0.02, 0.02)
            new_row[col] = round(row[col] * (1 + variation), 1)
        # Variasi target ±2%
        for col in ['Frame', 'Stem', 'Handlebar', 'Crank', 'Saddle']:
            variation = np.random.uniform(-0.02, 0.02)
            if col == 'Frame':
                new_row[col] = int(round(row[col] * (1 + variation)))
            else:
                new_row[col] = round(row[col] * (1 + variation), 2)
        data_sintetis.append(new_row)

# Buat DataFrame baru
df_sintetis = pd.DataFrame(data_sintetis)

# Simpan ke file baru
df_sintetis.to_csv('bike_fitting_dataset_sintetis.csv', index=False)
print('Data sintetis berhasil dibuat dan disimpan sebagai bike_fitting_dataset_sintetis.csv') 