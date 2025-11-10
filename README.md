# Manajemen Data Rekording XLSX dengan Streamlit

Aplikasi ini digunakan untuk mengelola, menampilkan, dan memvisualisasikan data rekording dari file Excel (`data.xlsx`).

## Fitur
- Menampilkan data dari berbagai sheet dalam file Excel
- Menampilkan statistik deskriptif data
- Menampilkan grafik interaktif dari kolom numerik
- Sheet `KodePenyakit` otomatis menampilkan kolom "Nama Penyakit" hasil join dengan sheet `GejalaPenyakit`

## Cara Menjalankan
1. Pastikan sudah mengaktifkan virtual environment dan menginstal dependensi:
   ```sh
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi Streamlit:
   ```sh
   streamlit run streamlit_xls_manager.py
   ```
3. Pastikan file `data.xlsx` berada di folder yang sama dengan script ini.

## Struktur Sheet yang Didukung
- **KodePenyakit**: Harus memiliki kolom `Kode Gejala`.
- **GejalaPenyakit**: Harus memiliki kolom `Nama Penyakit` dan `Kode Gejala` (berisi kode gejala dipisahkan koma).
- Sheet lain akan ditampilkan dan dapat divisualisasikan sesuai kolom numeriknya.

## Lisensi
Bebas digunakan untuk keperluan edukasi dan non-komersial.
