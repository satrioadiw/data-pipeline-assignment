# README.md

## REWORK INDVIDUAL ASSIGMMENT
Nama: Satrio Adi Wibowo
Program: AI Engineering Bootcamp
Project: Data Preparation & Pipeline Project
Absensi: AI-70
Email: satrio.ugm@gmail.com

## Deskripsi Singkat & Sumber Dataset
Dataset ini berisi karakteristik teknis dan spesifikasi mobil (seperti horsepower, peak-rpm, dimensi fisik) serta harga penjualannya. Dataset mentah diperoleh dari berkas pembelajaran internal `automobileEDA_dirty_training.csv`.

## Struktur Folder Project
├── automobileEDA_dirty_training.csv # Dataset Utama (Raw) ├── pipeline.py # Script Pipeline ETL Utama ├── automobileEDA_processed.csv # Output Dataset Hasil Proses └── README.md # Dokumentasi Proyek


## Alur ETL (Extract, Transform, Load)
1. **Extract**: Membaca dataset kotor `automobileEDA_dirty_training.csv` menggunakan Pandas.
2. **Transform (Inspection & Cleaning)**:
   - Memeriksa tipe data, missing values, dan data duplikat.
   - Menghapus data duplikat.
   - Menyeragamkan penulisan string (strip whitespace, lowercase).
   - Imputasi missing values numerik menggunakan Median dan kategorikal menggunakan Modus.
   - Koersi tipe data pada kolom numerik yang salah terbaca sebagai text.
3. **Transform (Feature Engineering)**:
   - Melakukan Min-Max Scaling pada kolom `normalized-losses`.
   - Melakukan One-Hot Encoding pada kolom kategori `aspiration`.
4. **Load**: Menyimpan dataframe yang sudah bersih dan ditransformasikan ke dalam berkas `automobileEDA_processed.csv`.

## Ringkasan Temuan Awal (Kondisi Awal Dataset)
* **Ukuran awal dataset**: 201 baris dan beberapa kolom spesifikasi otomotif.
* **Missing Values**: Ditemukan pada beberapa kolom penting seperti `normalized-losses` dan `stroke`.
* **Baris Duplikat**: Ditemukan beberapa record duplikat yang tidak perlu.
* **Ketidaksesuaian Tipe Data**: Kolom angka seperti `horsepower` terkadang dideteksi sebagai objek string karena adanya karakter non-numerik.

## Metode & Alasan Cleaning
* **Drop Duplicates**: Menjamin bahwa analisis di masa depan tidak terdistorsi oleh data redundan.
* **Median Imputation**: Mengisi kolom numerik kosong dengan nilai tengah agar aman terhadap outlier.
* **Min-Max Scaling**: Mengubah skala fitur `normalized-losses` menjadi rentang 0 hingga 1 agar seragam dengan analisis statistik/algoritma Machine Learning.
* **One-Hot Encoding**: Mengonversi variabel kategorikal `aspiration` menjadi fitur numerik biner (0 atau 1) sehingga siap digunakan oleh model prediktif.

## Cara Menjalankan Pipeline
```bash
python pipeline.py
