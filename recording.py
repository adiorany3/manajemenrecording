import streamlit as st
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Peternakan Sapi",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    /* Background dan layout utama */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef3 100%);
        padding: 20px;
    }
    
    /* Styling Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding: 10px 0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: #ffffff;
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        color: #2c3e50 !important;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f8f0;
        border-color: #4CAF50;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        color: white !important;
        border-color: #4CAF50 !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: inherit !important;
        font-size: 15px;
    }
    
    /* Header Title */
    h1 {
        color: white;
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%);
        border-radius: 15px;
        margin-bottom: 35px;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
        font-size: 2.5rem;
        letter-spacing: 1px;
    }
    
    /* Subheaders */
    h2, h3 {
        color: #2c3e50 !important;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 3px solid #4CAF50;
        background-color: transparent !important;
    }
    
    /* Styling khusus untuk text dalam section */
    .main p, .main li, .main span {
        color: #2c3e50 !important;
    }
    
    /* Expander text */
    .streamlit-expanderHeader p, .streamlit-expanderContent p {
        color: #2c3e50 !important;
    }
    
    /* Metric Cards */
    .stMetric {
        background-color: white !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    .stMetric label, .stMetric [data-testid="stMetricLabel"] {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    .stMetric [data-testid="stMetricValue"], .stMetric div[data-testid="stMetricValue"] {
        color: #4CAF50 !important;
        font-weight: 700 !important;
        font-size: 28px !important;
    }
    .stMetric div {
        color: #2c3e50 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: white;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        font-weight: 600;
    }
    
    /* Info, Success, Warning boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid;
        padding: 15px 20px;
        margin: 15px 0;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

st.title('🐄 Dashboard Manajemen Peternakan Sapi')

# Pilih folder tempat file XLSX berada

# Hanya gunakan data.xlsx di folder ini


file_path = os.path.join('.', 'data.xlsx')
if os.path.isfile(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        tab_list = []
        if 'Recording' in sheet_names:
            tab_list.append('Recording')
        if 'Kepemilikan' in sheet_names:
            tab_list.append('Kepemilikan')
        if 'KodePenyakit' in sheet_names and 'GejalaPenyakit' in sheet_names:
            tab_list.append('KodePenyakit')
        tab_list.append('Peta Lokasi')
        tab_list.append('Upload Data')
        tab = st.tabs(tab_list)

        # Tab Recording
        if 'Recording' in tab_list:
            with tab[tab_list.index('Recording')]:
                df_recording = pd.read_excel(file_path, sheet_name='Recording')
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader('📊 Data Recording')
                st.dataframe(df_recording, use_container_width=True, height=350)
                
                # Analisis Statistik Recording
                st.markdown("<br>", unsafe_allow_html=True)
                st.write('### 📈 Analisis Statistik Recording')
                numeric_cols = df_recording.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric('Total Data', len(df_recording))
                    with col2:
                        if 'Total' in df_recording.columns:
                            mean_val = df_recording['Total'].mean()
                            st.metric('Rata-rata Total Populasi', f'{mean_val:.2f}')
                    with col3:
                        if 'Total' in df_recording.columns:
                            std_val = df_recording['Total'].std()
                            st.metric('Standar Deviasi Total', f'{std_val:.2f}')
                    
                    st.write('**Statistik Deskriptif Lengkap:**')
                    st.write(df_recording.describe(include='all'))
                    
                    # Ringkasan per kolom numerik
                    st.write('**Ringkasan Statistik per Kolom:**')
                    for col in numeric_cols:
                        if df_recording[col].notna().sum() > 0:
                            with st.expander(f'Statistik {col}'):
                                col_data = df_recording[col].dropna()
                                st.write(f'- **Mean (Rata-rata):** {col_data.mean():.2f}')
                                st.write(f'- **Median (Nilai Tengah):** {col_data.median():.2f}')
                                st.write(f'- **Std Dev (Standar Deviasi):** {col_data.std():.2f}')
                                st.write(f'- **Min (Nilai Minimum):** {col_data.min():.2f}')
                                st.write(f'- **Max (Nilai Maksimum):** {col_data.max():.2f}')
                                st.write(f'- **Sum (Total):** {col_data.sum():.2f}')
                else:
                    st.write(df_recording.describe(include='all'))
                # Visualisasi Grafik
                st.markdown("<br>", unsafe_allow_html=True)
                st.write('### 📊 Visualisasi Data')
                st.markdown("<br>", unsafe_allow_html=True)
                col_chart1, col_chart2 = st.columns(2)
                
                # Diagram batang total populasi per bulan
                with col_chart1:
                    if 'Bulan' in df_recording.columns and 'Total' in df_recording.columns:
                        df_rec_plot = df_recording.dropna(subset=['Bulan', 'Total'])
                        fig, ax = plt.subplots(figsize=(8, 5))
                        bars = ax.bar(df_rec_plot['Bulan'].astype(str), df_rec_plot['Total'], 
                                     color='#4CAF50', alpha=0.8, edgecolor='#2E7D32')
                        ax.set_xlabel('Bulan', fontsize=12, fontweight='bold')
                        ax.set_ylabel('Total Populasi', fontsize=12, fontweight='bold')
                        ax.set_title('Total Populasi per Bulan', fontsize=14, fontweight='bold', pad=20)
                        ax.grid(axis='y', alpha=0.3, linestyle='--')
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        st.pyplot(fig)
                
                # Diagram garis populasi breeder
                with col_chart2:
                    if 'Bulan' in df_recording.columns and 'Populasi' in df_recording.columns:
                        df_rec_plot = df_recording.dropna(subset=['Bulan', 'Populasi'])
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.plot(df_rec_plot['Bulan'].astype(str), df_rec_plot['Populasi'], 
                               marker='o', linewidth=2.5, markersize=8, 
                               color='#2196F3', markerfacecolor='#1976D2')
                        ax.set_xlabel('Bulan', fontsize=12, fontweight='bold')
                        ax.set_ylabel('Populasi Breeder', fontsize=12, fontweight='bold')
                        ax.set_title('Tren Populasi Breeder', fontsize=14, fontweight='bold', pad=20)
                        ax.grid(True, alpha=0.3, linestyle='--')
                        plt.xticks(rotation=45, ha='right')
                        plt.tight_layout()
                        st.pyplot(fig)
                
                # Insight Recording
                st.markdown("<br>", unsafe_allow_html=True)
                st.write('### 💡 Insight Data Recording')
                st.markdown("<br>", unsafe_allow_html=True)
                df_rec_clean = df_recording.dropna(subset=['Bulan'])
                if len(df_rec_clean) > 0:
                    # Tren populasi
                    if 'Total' in df_rec_clean.columns:
                        total_vals = df_rec_clean['Total'].dropna()
                        if len(total_vals) > 1:
                            perubahan = total_vals.iloc[-1] - total_vals.iloc[0]
                            persen = (perubahan / total_vals.iloc[0]) * 100
                            st.info(f"📊 **Tren Populasi:** Total populasi {'meningkat' if perubahan > 0 else 'menurun'} sebesar {abs(perubahan):.0f} ekor ({abs(persen):.1f}%) dari {df_rec_clean.iloc[0]['Bulan']} ke {df_rec_clean.iloc[-1]['Bulan']}")
                    
                    # Kematian tertinggi
                    if 'Kematian' in df_rec_clean.columns:
                        kematian_data = df_rec_clean[['Bulan', 'Kematian']].dropna()
                        if len(kematian_data) > 0:
                            max_kematian = kematian_data.loc[kematian_data['Kematian'].idxmax()]
                            st.warning(f"⚠️ **Kematian Tertinggi:** {max_kematian['Kematian']:.0f} ekor pada bulan {max_kematian['Bulan']}. Perlu investigasi lebih lanjut.")
                    
                    # Penjualan
                    if 'Jual' in df_rec_clean.columns:
                        jual_data = df_rec_clean['Jual'].dropna()
                        if jual_data.sum() > 0:
                            st.success(f"💰 **Total Penjualan:** {jual_data.sum():.0f} ekor sepanjang periode recording")
        # Tab Kepemilikan
        if 'Kepemilikan' in tab_list:
            with tab[tab_list.index('Kepemilikan')]:
                df_kepemilikan = pd.read_excel(file_path, sheet_name='Kepemilikan')
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader('👥 Data Kepemilikan')
                st.dataframe(df_kepemilikan, use_container_width=True, height=350)
                
                # Analisis Statistik Kepemilikan
                st.markdown("<br>", unsafe_allow_html=True)
                st.write('### 📈 Analisis Statistik Kepemilikan')
                numeric_cols = df_kepemilikan.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric('Total Pemilik', len(df_kepemilikan.dropna(subset=['Nama'])))
                    with col2:
                        if 'Total' in df_kepemilikan.columns:
                            total_sum = df_kepemilikan['Total'].sum()
                            st.metric('Total Sapi Keseluruhan', f'{total_sum:.0f}')
                    with col3:
                        if 'Total' in df_kepemilikan.columns:
                            mean_val = df_kepemilikan['Total'].mean()
                            st.metric('Rata-rata Sapi per Pemilik', f'{mean_val:.2f}')
                    
                    st.write('**Statistik Deskriptif Lengkap:**')
                    st.write(df_kepemilikan.describe(include='all'))
                    
                    # Ringkasan per kolom numerik
                    st.write('**Ringkasan Statistik per Kolom:**')
                    for col in numeric_cols:
                        if df_kepemilikan[col].notna().sum() > 0:
                            with st.expander(f'Statistik {col}'):
                                col_data = df_kepemilikan[col].dropna()
                                st.write(f'- **Mean (Rata-rata):** {col_data.mean():.2f}')
                                st.write(f'- **Median (Nilai Tengah):** {col_data.median():.2f}')
                                st.write(f'- **Std Dev (Standar Deviasi):** {col_data.std():.2f}')
                                st.write(f'- **Min (Nilai Minimum):** {col_data.min():.2f}')
                                st.write(f'- **Max (Nilai Maksimum):** {col_data.max():.2f}')
                                st.write(f'- **Sum (Total):** {col_data.sum():.2f}')
                else:
                    st.write(df_kepemilikan.describe(include='all'))
                # Visualisasi Kepemilikan
                st.markdown("<br>", unsafe_allow_html=True)
                st.write('### 📊 Visualisasi Kepemilikan')
                st.markdown("<br>", unsafe_allow_html=True)
                if 'Nama' in df_kepemilikan.columns and 'Total' in df_kepemilikan.columns:
                    df_kep_plot = df_kepemilikan.dropna(subset=['Nama', 'Total'])
                    fig, ax = plt.subplots(figsize=(12, 6))
                    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(df_kep_plot)))
                    bars = ax.bar(df_kep_plot['Nama'].astype(str), df_kep_plot['Total'], 
                                 color=colors, edgecolor='black', linewidth=0.7)
                    ax.set_xlabel('Nama Pemilik', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Total Sapi (ekor)', fontsize=12, fontweight='bold')
                    ax.set_title('Distribusi Kepemilikan Sapi per Pemilik', fontsize=14, fontweight='bold', pad=20)
                    ax.grid(axis='y', alpha=0.3, linestyle='--')
                    plt.xticks(rotation=45, ha='right')
                    
                    # Tambahkan nilai di atas bar
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{int(height)}',
                               ha='center', va='bottom', fontsize=9, fontweight='bold')
                    plt.tight_layout()
                    st.pyplot(fig)
                
                # Insight Kepemilikan
                st.markdown("<br>", unsafe_allow_html=True)
                st.write('### 💡 Insight Data Kepemilikan')
                st.markdown("<br>", unsafe_allow_html=True)
                df_kep_clean = df_kepemilikan.dropna(subset=['Nama', 'Total'])
                if len(df_kep_clean) > 0:
                    # Pemilik terbanyak
                    max_owner = df_kep_clean.loc[df_kep_clean['Total'].idxmax()]
                    st.success(f"🏆 **Pemilik Terbanyak:** {max_owner['Nama']} dengan {max_owner['Total']:.0f} ekor sapi")
                    
                    # Total dan rata-rata
                    total_sapi = df_kep_clean['Total'].sum()
                    rata_rata = df_kep_clean['Total'].mean()
                    st.info(f"📊 **Total Keseluruhan:** {total_sapi:.0f} ekor sapi dimiliki oleh {len(df_kep_clean)} pemilik")
                    st.info(f"📈 **Rata-rata Kepemilikan:** {rata_rata:.1f} ekor per pemilik")
                    
                    # Distribusi kepemilikan
                    small_owners = len(df_kep_clean[df_kep_clean['Total'] <= 5])
                    medium_owners = len(df_kep_clean[(df_kep_clean['Total'] > 5) & (df_kep_clean['Total'] <= 10)])
                    large_owners = len(df_kep_clean[df_kep_clean['Total'] > 10])
                    st.write(f"**Distribusi Kepemilikan:**")
                    st.write(f"- Skala Kecil (≤5 ekor): {small_owners} pemilik")
                    st.write(f"- Skala Menengah (6-10 ekor): {medium_owners} pemilik")
                    st.write(f"- Skala Besar (>10 ekor): {large_owners} pemilik")
        # Tab KodePenyakit (jika ada)
        if 'KodePenyakit' in tab_list:
            with tab[tab_list.index('KodePenyakit')]:
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader('🏥 Data Kode Gejala & Penyakit')
                df_kode = pd.read_excel(file_path, sheet_name='KodePenyakit')
                df_gejala = pd.read_excel(file_path, sheet_name='GejalaPenyakit')
                def get_nama_penyakit(kode):
                    result = []
                    for i, row in df_gejala.iterrows():
                        if kode in str(row['Kode Gejala']).replace(' ', '').split(','):
                            result.append(row['Nama Penyakit'])
                    return ', '.join(result) if result else '-'
                df_kode['Nama Penyakit'] = df_kode['Kode Gejala'].apply(get_nama_penyakit)
                cols = df_kode.columns.tolist()
                if 'Nama Penyakit' in cols:
                    cols.insert(cols.index('Kode Gejala') + 1, cols.pop(cols.index('Nama Penyakit')))
                df_kode = df_kode[cols]
                st.info(f'📋 Total: {len(df_kode)} kode gejala tercatat')
                st.dataframe(df_kode, use_container_width=True, height=400)
        # Tab Peta Lokasi - Menampilkan Peta
        with tab[tab_list.index('Peta Lokasi')]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader('🗺️ Peta Lokasi Peternakan')
            st.markdown("<br>", unsafe_allow_html=True)
            peta_path = os.path.join('.', 'peta.jpeg')
            if os.path.isfile(peta_path):
                try:
                    image = Image.open(peta_path)
                    col1, col2, col3 = st.columns([1, 8, 1])
                    with col2:
                        st.image(image, caption='📍 Peta Lokasi Peternakan Sapi', use_container_width=True)
                    st.success('✅ Peta berhasil dimuat')
                except Exception as e:
                    st.error(f'❌ Gagal memuat peta.jpeg: {e}')
            else:
                st.warning('⚠️ File peta.jpeg tidak ditemukan di folder ini.')
            
            # Opsi untuk tetap menampilkan Peta Lokasi jika ada
            other_sheets = [s for s in sheet_names if s not in ['Recording', 'Kepemilikan', 'KodePenyakit', 'GejalaPenyakit']]
            if other_sheets:
                st.write('---')
                st.write('**Data Peta Lokasi:**')
                sheet = st.selectbox('Pilih Peta Lokasi:', other_sheets)
                df = pd.read_excel(file_path, sheet_name=sheet)
                st.write('Data Preview:')
                st.dataframe(df)
                st.write('Statistik Data:')
                st.write(df.describe(include='all'))
        
        # Tab Upload Data
        with tab[tab_list.index('Upload Data')]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader('📤 Upload Data Excel')
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.info('📋 Upload file Excel (.xlsx) untuk mengganti data.xlsx yang ada')
            
            # Download template/contoh
            col_download, col_space = st.columns([2, 3])
            with col_download:
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        file_bytes = f.read()
                    st.download_button(
                        label='📥 Download Contoh File (data.xlsx)',
                        data=file_bytes,
                        file_name='contoh_data.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        type='secondary'
                    )
                    st.caption('Download file ini sebagai template untuk format data yang sesuai')
            
            st.markdown("<br>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Pilih file Excel", type=['xlsx'], key='file_uploader')
            
            if uploaded_file is not None:
                try:
                    # Preview file yang diupload
                    df_preview = pd.read_excel(uploaded_file, sheet_name=0)
                    st.success(f'✅ File "{uploaded_file.name}" berhasil dimuat!')
                    
                    st.write('### Preview Data yang Diupload:')
                    st.dataframe(df_preview, use_container_width=True, height=300)
                    
                    # Tampilkan sheet yang tersedia
                    uploaded_excel = pd.ExcelFile(uploaded_file)
                    st.write(f'**Sheet yang tersedia:** {", ".join(uploaded_excel.sheet_names)}')
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric('Total Baris', len(df_preview))
                    with col2:
                        st.metric('Total Kolom', len(df_preview.columns))
                    
                    st.write('**Nama Kolom:**')
                    st.write(', '.join(df_preview.columns.tolist()))
                    
                    # Tombol untuk menyimpan file
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button('💾 Simpan sebagai data.xlsx', type='primary'):
                        try:
                            # Simpan file yang diupload menggantikan data.xlsx
                            save_path = os.path.join('.', 'data.xlsx')
                            with open(save_path, 'wb') as f:
                                f.write(uploaded_file.getbuffer())
                            st.success('✅ File berhasil disimpan sebagai data.xlsx!')
                            st.info('🔄 Silakan refresh halaman untuk melihat data terbaru')
                        except Exception as e:
                            st.error(f'❌ Gagal menyimpan file: {e}')
                    
                    st.warning('⚠️ Perhatian: Menyimpan file akan mengganti data.xlsx yang sudah ada')
                    
                except Exception as e:
                    st.error(f'❌ Gagal membaca file: {e}')
            else:
                st.markdown("""
                <div style='text-align: center; padding: 40px; background-color: #f8f9fa; border-radius: 10px; border: 2px dashed #4CAF50;'>
                    <p style='font-size: 18px; color: #666; margin: 0;'>
                        👆 Pilih file Excel untuk diupload
                    </p>
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f'Gagal membaca file: {e}')
else:
    st.warning('File data.xlsx tidak ditemukan di folder ini.')

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%); 
            border-radius: 10px; margin-top: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
    <p style='color: white; font-size: 18px; font-weight: 600; margin: 0 0 10px 0;'>
        ✨ Created by Team Pengabdian Pasca Tanah Bambu ✨
    </p>
    <p style='color: white; font-size: 14px; font-weight: 400; margin: 0; opacity: 0.9;'>
        Fakultas Peternakan Universitas Gadjah Mada
    </p>
</div>
""", unsafe_allow_html=True)


