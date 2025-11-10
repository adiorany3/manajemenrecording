
# --- Import Library ---
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# --- Set Title and Favicon (HTML hack) ---
st.set_page_config(page_title="Manajemen Rekording XLSX", page_icon="📊")
st.markdown(
    """
    <style>
    .css-18e3th9 {padding-top: 2rem;}
    </style>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/337/337946.png">
    """,
    unsafe_allow_html=True
)

st.title('Manajemen Data Rekording (XLSX)')
st.caption('Aplikasi sederhana untuk mengelola dan visualisasi data rekording berbasis file Excel.')

# --- Cek file data.xlsx ---
file_path = os.path.join('.', 'data.xlsx')
if not os.path.isfile(file_path):
    st.warning('File data.xlsx tidak ditemukan di folder ini.')
else:
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names

        # --- Join Nama Penyakit jika sheet tersedia ---
        if 'KodePenyakit' in sheet_names and 'GejalaPenyakit' in sheet_names:
            df_kode = pd.read_excel(file_path, sheet_name='KodePenyakit')
            df_gejala = pd.read_excel(file_path, sheet_name='GejalaPenyakit')

            def get_nama_penyakit(kode):
                result = []
                for _, row in df_gejala.iterrows():
                    if kode in str(row['Kode Gejala']).replace(' ', '').split(','):
                        result.append(row['Nama Penyakit'])
                return ', '.join(result) if result else '-'

            df_kode['Nama Penyakit'] = df_kode['Kode Gejala'].apply(get_nama_penyakit)
            # Tempatkan kolom Nama Penyakit setelah Kode Gejala
            cols = df_kode.columns.tolist()
            if 'Nama Penyakit' in cols:
                cols.insert(cols.index('Kode Gejala') + 1, cols.pop(cols.index('Nama Penyakit')))
            df_kode = df_kode[cols]
            st.subheader('Tabel Kode Gejala + Nama Penyakit')
            st.dataframe(df_kode)

        # --- Pilih sheet dan tampilkan data ---
        sheet = st.selectbox('Pilih sheet:', sheet_names)
        df = pd.read_excel(file_path, sheet_name=sheet)
        st.subheader('Data Preview')
        st.dataframe(df)
        st.subheader('Statistik Data')
        st.write(df.describe(include='all'))

        # --- Visualisasi Data Numerik ---
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
            st.info('Tidak ada kolom numerik untuk digrafikkan.')
    except Exception as e:
        st.error(f'Gagal membaca file: {e}')


