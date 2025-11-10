import streamlit as st
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

st.title('Manajemen Data Rekording (XLSX)')

# Pilih folder tempat file XLSX berada

# Hanya gunakan data.xlsx di folder ini

file_path = os.path.join('.', 'data.xlsx')
if os.path.isfile(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        # Jika sheet KodePenyakit dan GejalaPenyakit ada, lakukan join Nama Penyakit
        if 'KodePenyakit' in sheet_names and 'GejalaPenyakit' in sheet_names:
            df_kode = pd.read_excel(file_path, sheet_name='KodePenyakit')
            df_gejala = pd.read_excel(file_path, sheet_name='GejalaPenyakit')
            # Buat kolom Nama Penyakit berdasarkan Kode Gejala
            def get_nama_penyakit(kode):
                result = []
                for i, row in df_gejala.iterrows():
                    if kode in str(row['Kode Gejala']).replace(' ', '').split(','):
                        result.append(row['Nama Penyakit'])
                return ', '.join(result) if result else '-'
            df_kode['Nama Penyakit'] = df_kode['Kode Gejala'].apply(get_nama_penyakit)
            # Tempatkan kolom Nama Penyakit setelah Kode Gejala
            cols = df_kode.columns.tolist()
            if 'Nama Penyakit' in cols:
                cols.insert(cols.index('Kode Gejala') + 1, cols.pop(cols.index('Nama Penyakit')))
            df_kode = df_kode[cols]
            st.write('Tabel Kode Gejala + Nama Penyakit:')
            st.dataframe(df_kode)
        # Sheet lain tetap bisa dipilih dan divisualisasikan
        sheet = st.selectbox('Pilih sheet:', sheet_names)
        df = pd.read_excel(file_path, sheet_name=sheet)
        st.write('Data Preview:')
        st.dataframe(df)
        st.write('Statistik Data:')
        st.write(df.describe(include='all'))
        # Pilih kolom untuk grafik
        columns = df.select_dtypes(include=['number']).columns.tolist()
        if columns:
            col_x = st.selectbox('Pilih kolom X (sumbu X):', columns)
            col_y = st.selectbox('Pilih kolom Y (sumbu Y):', columns)
            if col_x and col_y:
                fig, ax = plt.subplots()
                ax.plot(df[col_x], df[col_y], marker='o')
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                ax.set_title(f'Grafik {col_y} terhadap {col_x}')
                st.pyplot(fig)
        else:
            st.warning('Tidak ada kolom numerik untuk digrafikkan.')
    except Exception as e:
        st.error(f'Gagal membaca file: {e}')
else:
    st.warning('File data.xlsx tidak ditemukan di folder ini.')


