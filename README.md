# 🐄 Dashboard Manajemen Peternakan Sapi

Aplikasi web interaktif berbasis Streamlit untuk mengelola, menganalisis, dan memvisualisasikan data peternakan sapi dari file Excel (`data.xlsx`).
Contoh website : https://manajemenrecording.streamlit.app/

## ✨ Fitur Utama

### 📊 Tab Recording
- Menampilkan data populasi sapi bulanan (Populasi, Kelahiran, Kematian, Jual, Total)
- **Analisis Statistik Lengkap**: Mean, Median, Standar Deviasi, Min, Max, Sum per kolom
- **Visualisasi Data**: 
  - Diagram batang total populasi per bulan
  - Diagram garis tren populasi breeder
- **Insight Otomatis**: 
  - Analisis tren populasi (peningkatan/penurunan)
  - Identifikasi bulan dengan kematian tertinggi
  - Total penjualan sepanjang periode
  - **Insight Pemeliharaan**: Rekomendasi pemeliharaan berdasarkan data (kegiatan audit kesehatan, pembersihan kandang, validasi input, jadwal pemeriksaan) ditampilkan saat Anda mencentang checkbox 'Tampilkan Insight Pemeliharaan (Recording)'.

### 👥 Tab Kepemilikan
- Data kepemilikan sapi per pemilik
- **Statistik Kepemilikan**: Total pemilik, total sapi keseluruhan, rata-rata per pemilik
- **Visualisasi**: Diagram batang distribusi kepemilikan dengan gradient warna
- **Insight Kepemilikan**: 
  - Pemilik dengan jumlah sapi terbanyak
  - Distribusi skala kepemilikan (kecil/menengah/besar)
  - **Insight Pemeliharaan**: Rekomendasi perawatan dan pembinaan bila banyak pemilik skala kecil, atau identifikasi data yang perlu validasi. Aktifkan lewat checkbox 'Tampilkan Insight Pemeliharaan (Kepemilikan)'.

### 🏥 Tab KodePenyakit
- Mapping otomatis kode gejala dengan nama penyakit
- Join data antara sheet `KodePenyakit` dan `GejalaPenyakit`
- Tampilan daftar lengkap kode gejala dan penyakit terkait

### 🗺️ Tab Peta Lokasi (NEW!)
- **Peta Interaktif** menggunakan Folium dengan koordinat GPS
- Marker lokasi untuk setiap kelompok ternak
- **Info Popup** berisi:
  - Nama Kelompok
  - Desa
  - Alamat lengkap
  - Koordinat GPS
  - Link Google Maps
- Zoom dan navigasi interaktif
- Fallback ke gambar peta jika data lokasi tidak tersedia

### 📤 Tab Upload Data
- Upload file Excel (.xlsx) baru
- Preview data sebelum menyimpan
- Download template/contoh file data.xlsx
- Validasi struktur file dan sheet
- Simpan sebagai data.xlsx untuk update data

## 🎨 Desain & UI
- **Layout**: Wide mode dengan sidebar collapsed
- **Theme**: Hijau (#4CAF50) professional
- **Custom CSS**: 
  - Gradient backgrounds
  - Shadow effects dan hover animations
  - Metric cards dengan border accent
  - Tab styling dengan transisi smooth
- **Responsive**: Optimized untuk berbagai ukuran layar
- **Footer**: Credit team dengan gradient background

## 🚀 Cara Menjalankan

### 1. Instalasi Dependensi
Pastikan sudah mengaktifkan virtual environment, lalu install requirements:
```sh
pip install -r requirements.txt
```

**Dependencies yang dibutuhkan:**
- streamlit
- pandas
- matplotlib
- openpyxl
- pillow
- folium
- streamlit-folium

### 2. Jalankan Aplikasi
```sh
streamlit run recording.py
```

### 3. File Data
Pastikan file `data.xlsx` berada di folder yang sama dengan `recording.py`

## 📋 Struktur Data yang Didukung

### Sheet Recording
Kolom yang dibutuhkan:
- `Bulan`: Nama bulan (string)
- `Populasi`: Jumlah populasi breeder (numerik)
- `Kelahiran`: Jumlah kelahiran (numerik)
- `Kematian`: Jumlah kematian (numerik)
- `Jual`: Jumlah penjualan (numerik)
- `Total`: Total populasi (numerik)

### Sheet Kepemilikan
Kolom yang dibutuhkan:
- `No`: Nomor urut (numerik)
- `Nama`: Nama pemilik (string)
- `Total`: Jumlah sapi (numerik)

### Sheet KodePenyakit
Kolom yang dibutuhkan:
- `Kode Gejala`: Kode identifikasi gejala (string)
- `Gejala`: Deskripsi gejala (string)

### Sheet GejalaPenyakit
Kolom yang dibutuhkan:
- `Nama Penyakit`: Nama penyakit (string)
- `Kode Gejala`: Kode gejala yang berkaitan, dipisahkan koma (string)

### Sheet Lokasi (Optional)
Kolom yang dibutuhkan:
- `Nama Kelompok`: Nama kelompok ternak (string)
- `Desa`: Nama desa (string)
- `Alamat`: Alamat lengkap (string)
- `Kordinat`: Koordinat GPS format "latitude, longitude" (string)
- `Gmaps`: Link Google Maps (string, optional)

## 💡 Tips Penggunaan
- Gunakan file `data.xlsx` yang ada sebagai template untuk format yang benar
- Download contoh file di Tab Upload Data jika perlu referensi
- Koordinat harus dalam format: "-3.703004, 115.512293" (latitude, longitude)
- Untuk best practice, backup data.xlsx sebelum upload file baru

## 👥 Tim Pengembang
**Team Pengabdian Pasca Tanah Bambu**  
Fakultas Peternakan Universitas Gadjah Mada

## 📄 Lisensi
Bebas digunakan untuk keperluan edukasi dan non-komersial.
