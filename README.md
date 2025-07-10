# Tugas-PI

## Cara Menambahkan Gambar dan Penomoran Indeks

### 1. Menyimpan Gambar
- Simpan semua gambar di folder `static/img/`
- Format yang didukung: PNG, JPG, JPEG, SVG, GIF
- Gunakan nama file yang deskriptif (contoh: `tinggi_badan.png`, `inseam_measurement.jpg`)

### 2. Menambahkan Gambar di HTML
Gunakan struktur berikut untuk menambahkan gambar dengan penomoran:

```html
<div class="image-container">
    <img src="{{ url_for('static', filename='img/nama_gambar.png') }}" 
         class="img-fluid rounded shadow-sm" 
         style="max-width: 400px;" 
         alt="Deskripsi gambar">
    <div class="image-caption">
        <span class="image-number">Gambar X:</span> Deskripsi gambar
    </div>
</div>
```

### 3. Atribut Gambar
- `src`: Path ke file gambar menggunakan Flask `url_for()`
- `class`: Bootstrap classes untuk styling
- `style`: CSS inline untuk ukuran maksimal
- `alt`: Teks alternatif untuk accessibility
- `image-caption`: Caption dengan penomoran otomatis

### 4. Style CSS yang Tersedia
- `.image-container`: Container untuk gambar dan caption
- `.image-caption`: Style untuk caption gambar
- `.image-number`: Style untuk nomor gambar (warna biru, bold)

### 5. Contoh Penggunaan
```html
<!-- Gambar dengan penomoran otomatis -->
<div class="image-container">
    <img src="{{ url_for('static', filename='img/contoh.png') }}" 
         class="img-fluid rounded shadow-sm" 
         style="max-width: 400px;" 
         alt="Contoh gambar">
    <div class="image-caption">
        <span class="image-number">Gambar 1:</span> Contoh penomoran gambar
    </div>
</div>
```

### 6. Tips
- Gunakan ukuran gambar yang optimal (tidak terlalu besar)
- Pastikan alt text deskriptif untuk accessibility
- Gunakan format PNG untuk gambar dengan transparansi
- Gunakan format JPG untuk foto
- Gunakan format SVG untuk ilustrasi vektor