
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def extract_data(file_path):
    """1. EXTRACT: Membaca dataset"""
    print("=== [1/5] EXTRACTING DATA ===")
    try:
        df = pd.read_csv(file_path)
        print(f"Berhasil memuat dataset dari {file_path}\n")
        return df
    except Exception as e:
        print(f"Gagal memuat dataset: {e}")
        return None

def inspect_data(df):
    """2. INSPECT: Pemeriksaan awal dataset"""
    print("=== [2/5] INSPECTING DATA ===")
    if df is None:
        return
    
    print("--- Lima Baris Pertama Dataset ---")
    print(df.head())
    print("\n--- Ukuran Dataset ---")
    print(f"Jumlah baris: {df.shape[0]}, Jumlah kolom: {df.shape[1]}")
    
    print("\n--- Informasi Kolom dan Tipe Data ---")
    print(df.info())
    
    print("\n--- Jumlah Missing Values Per Kolom ---")
    print(df.isnull().sum())
    
    print("\n--- Jumlah Duplicate Records ---")
    print(df.duplicated().sum())
    
    print("\n--- Nilai Unik Kolom Kategorikal (Relevan) ---")
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        print(f"{col}: {df[col].unique()[:10]} ... (Total Unik: {df[col].nunique()})")
    print("\n")

def clean_data(df):
    """3. TRANSFORM - CLEANING: Pembersihan data"""
    print("=== [3/5] CLEANING DATA ===")
    df_clean = df.copy()
    
    init_rows = df_clean.shape[0]
    init_missing = df_clean.isnull().sum().sum()
    
    dup_count = df_clean.duplicated().sum()
    df_clean = df_clean.drop_duplicates()
    
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
    
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            
    for col in categorical_cols:
        if df_clean[col].isnull().sum() > 0:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
            
    for col in ['stroke', 'horsepower', 'peak-rpm', 'price']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].replace(['?', 'nan', 'none', ''], np.nan)
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())

    final_rows = df_clean.shape[0]
    final_missing = df_clean.isnull().sum().sum()
    
    print(f"Jumlah data SEBELUM cleaning: {init_rows} baris")
    print(f"Jumlah data SESUDAH cleaning: {final_rows} baris")
    print(f"Jumlah missing values SEBELUM cleaning: {init_missing}")
    print(f"Jumlah missing values SESUDAH cleaning: {final_missing}")
    print(f"Jumlah baris terduplikasi yang dihapus: {dup_count}\n")
    
    return df_clean

def transform_data(df):
    """4. TRANSFORM - TRANSFORMATION: Scaling dan Encoding"""
    print("=== [4/5] TRANSFORMING DATA ===")
    df_trans = df.copy()
    
    if 'normalized-losses' in df_trans.columns:
        scaler = MinMaxScaler()
        df_trans['normalized-losses-before'] = df_trans['normalized-losses']
        df_trans['normalized-losses'] = scaler.fit_transform(df_trans[['normalized-losses']])
        print("--- Perbandingan Min-Max Scaling ('normalized-losses') ---")
        print(df_trans[['normalized-losses-before', 'normalized-losses']].head())
        df_trans = df_trans.drop(columns=['normalized-losses-before'])
        
    if 'aspiration' in df_trans.columns:
        print("\n--- One-Hot Encoding pada kolom 'aspiration' ---")
        print(f"Kategori unik sebelum encoding: {df['aspiration'].unique()}")
        df_trans = pd.get_dummies(df_trans, columns=['aspiration'], prefix='aspiration', dtype=int)
        encoded_cols = [col for col in df_trans.columns if col.startswith('aspiration_')]
        print(f"Kolom hasil encoding baru: {encoded_cols}")
        print(df_trans[encoded_cols].head())
        
    print("\n")
    return df_trans

def load_data(df, output_path):
    """5. LOAD: Menyimpan hasil ke file CSV"""
    print("=== [5/5] LOADING DATA ===")
    try:
        df.to_csv(output_path, index=False)
        print(f"Sukses! Dataset hasil proses disimpan ke: {output_path}\n")
    except Exception as e:
        print(f"Gagal menyimpan dataset: {e}")

def run_pipeline(input_file, output_file):
    """Fungsi utama orchestrator ETL"""
    print("=========================================")
    print("      MULAI EKSEKUSI PIPELINE ETL        ")
    print("=========================================\n")
    
    df_raw = extract_data(input_file)
    if df_raw is None: return
    
    inspect_data(df_raw)
    df_cleaned = clean_data(df_raw)
    df_transformed = transform_data(df_cleaned)
    load_data(df_transformed, output_file)
    
    print("=========================================")
    print("    EKSEKUSI PIPELINE SELESAI SUKSES     ")
    print("=========================================")

if __name__ == '__main__':
    run_pipeline('/content/automobileEDA_dirty_training.csv', '/content/automobileEDA_processed.csv')
