# Aplikasi Fitting Sepeda - SepedaKu

Aplikasi web untuk memberikan rekomendasi fitting sepeda berdasarkan ukuran tubuh pengguna dengan tampilan yang responsif dan user-friendly.

## Fitur Utama

- **Landing Page Responsif**: Tampilan yang menarik dengan splash screen dan navigasi smooth
- **Panduan Lengkap**: Tutorial cara mengukur tubuh dengan accordion yang interaktif
- **Fitting Otomatis**: Rekomendasi ukuran sepeda menggunakan model Machine Learning
- **Tampilan Responsif**: Layout yang optimal untuk desktop dan mobile
- **Visualisasi Hasil**: Tampilan hasil yang jelas dan mudah dipahami

## Layout Section Fitting (Section 4)

### Desktop View (≥992px)
- **Form Input**: Berada di sebelah kiri (5 kolom)
- **Hasil Rekomendasi**: Berada di sebelah kanan (7 kolom)
- **Layout**: Side-by-side untuk efisiensi ruang

### Mobile View (<992px)
- **Form Input**: Berada di atas
- **Hasil Rekomendasi**: Berada di bawah
- **Layout**: Stacked untuk kemudahan penggunaan

## Instalasi

1. Clone repository ini
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Pastikan file model `models/bike_fitting_model.pkl` tersedia

4. Jalankan aplikasi:
   ```bash
   python app.py
   ```

5. Buka browser dan akses `http://localhost:5000`

## Struktur File

```
├── app.py                      # File utama Flask
├── models/                     # Folder untuk model ML
│   ├── bike_fitting_model.pkl
│   └── train_model.py
├── templates/                  # Template HTML
│   ├── landing_page_fixed.html # Landing page utama (IMPROVED)
│   ├── landing_page.html       # Landing page lama
│   ├── fitting.html           # Halaman fitting terpisah
│   ├── tutorial.html
│   └── info.html
├── static/                     # Asset statis
│   └── img/
├── requirements.txt            # Dependensi Python
└── README.md
```

## Penggunaan

1. Buka aplikasi di browser
2. Scroll ke section "Fitting" atau klik menu "Fitting"
3. Masukkan data tubuh Anda:
   - Tinggi Badan (cm)
   - Inseam / Panjang Selangkangan (cm)
   - Panjang Lengan (cm)
   - Panjang Torso (cm)
   - Lebar Bahu (cm)
4. Klik "Dapatkan Rekomendasi"
5. Lihat hasil rekomendasi fitting sepeda

## API Endpoint

- `POST /predict` - Menerima data tubuh dan mengembalikan rekomendasi fitting

### Format Input:
```json
{
  "tinggi": 170,
  "inseam": 80,
  "torso": 50,
  "lengan": 60,
  "bahu": 30
}
```

### Format Output:
```json
{
  "Frame": "M",
  "Saddle": 75.5,
  "Crank": 170,
  "Stem": 90,
  "Handlebar": 420
}
```

## Perbaikan yang Dilakukan

### Section 4 (Fitting)
1. **Layout Responsif**: Form dan hasil rekomendasi side-by-side di desktop
2. **State Management**: Tiga state (initial, loading, result) yang jelas
3. **Visual Feedback**: Loading spinner dan animasi yang smooth
4. **Card-based Results**: Hasil ditampilkan dalam card yang rapi
5. **Error Handling**: Penanganan error yang lebih baik
6. **Mobile Optimization**: Layout stacked untuk mobile

### UI/UX Improvements
1. **Better Typography**: Font dan spacing yang lebih baik
2. **Color Coding**: Warna berbeda untuk setiap jenis rekomendasi
3. **Smooth Transitions**: Animasi yang halus antar state
4. **Clear Visual Hierarchy**: Struktur informasi yang jelas

## Catatan

- Hasil rekomendasi bersifat estimasi dan sebaiknya dikonsultasikan dengan ahli fitting sepeda
- Model ML harus sudah dilatih dan disimpan dalam format `.pkl`
- Aplikasi memerlukan Python 3.7+ dan Flask
- Tampilan optimal di browser modern dengan dukungan CSS Grid dan Flexbox