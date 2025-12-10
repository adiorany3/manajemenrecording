import pandas as pd


def generate_maintenance_insights(df: pd.DataFrame, domain: str = None):
    """Buat daftar insight pemeliharaan berdasar heuristik sederhana.
    Mengembalikan list tuple (tag, message) di mana tag adalah salah satu 'info', 'warning', 'success'.
    """
    insights = []
    if df is None or df.empty:
        insights.append(('info', 'Data kosong: tidak ada insight yang bisa diberikan.'))
        return insights

    # Duplikasi
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        insights.append(('warning', f'Ada {dup_count} baris duplikat. Periksa proses input data.'))

    # Per kolom
    for col in df.columns:
        s = df[col]
        miss_pct = s.isna().mean()
        if miss_pct > 0.2:
            insights.append(('warning', f'Kolom "{col}" memiliki {miss_pct:.0%} nilai kosong. Isi atau validasi input.'))
        elif miss_pct > 0:
            insights.append(('info', f'Kolom "{col}" memiliki beberapa nilai kosong ({miss_pct:.0%}).'))
        if s.nunique(dropna=True) <= 1:
            insights.append(('warning', f'Kolom "{col}" tampak konstan (1 nilai). Pertimbangkan evaluasi/penyingkiran kolom.'))
        # Numeric checks
        if pd.api.types.is_numeric_dtype(s):
            num = pd.to_numeric(s, errors='coerce').dropna()
            if len(num) >= 3:
                q1, q3 = num.quantile([0.25, 0.75])
                iqr = q3 - q1
                outliers = num[(num < (q1 - 1.5 * iqr)) | (num > (q3 + 1.5 * iqr))]
                if len(outliers) / len(num) > 0.05:
                    insights.append(('warning', f'Kolom "{col}" punya {len(outliers)/len(num):.0%} pencilan — periksa sensor/input atau lakukan normalisasi.'))
                if 'durasi' in col.lower() or 'lama' in col.lower() or 'waktu' in col.lower():
                    if (num < 0).any():
                        insights.append(('warning', f'Kolom "{col}" mengandung nilai negatif padahal seharusnya >= 0.'))

    # Domain-specific heuristics
    if domain == 'recording':
        # Kematian: jika tinggi dibandingkan dengan Total
        if 'Kematian' in df.columns and 'Total' in df.columns:
            merged = df[['Kematian', 'Total']].dropna()
            if not merged.empty:
                rata_kematian = merged['Kematian'].mean()
                rata_total = merged['Total'].mean()
                if rata_total > 0 and (rata_kematian / rata_total) > 0.05:
                    insights.append(('warning', f'Rata-rata kematian ({rata_kematian:.2f}) relatif tinggi dibandingkan rata-rata total populasi ({rata_total:.2f}). Sarankan audit kesehatan ternak dan kebersihan kandang.'))
                else:
                    insights.append(('success', 'Rasio kematian relatif terkendali.'))
        if 'Sakit' in df.columns and pd.api.types.is_numeric_dtype(df['Sakit']):
            sakit_pct = df['Sakit'].dropna().mean()
            if sakit_pct and sakit_pct > 0.05:
                insights.append(('warning', 'Tingkat penyakit ("Sakit") cukup tinggi. Pertimbangkan vaccination dan biosecurity.'))

    if domain == 'kepemilikan':
        if 'Total' in df.columns and pd.api.types.is_numeric_dtype(df['Total']):
            low_owners = df[df['Total'] <= 2]
            if len(low_owners) / max(1, len(df)) > 0.3:
                insights.append(('info', 'Banyak pemilik dengan skala kecil. Pertimbangkan program pembinaan dan pendidikan pemeliharaan.'))

    # Rekomendasi umum
    if any(tag == 'warning' for tag, _ in insights):
        insights.append(('info', 'Saran umum: lakukan validasi input, jadwalkan pemeriksaan berkala, dan perkuat prosedur sanitasi.'))
    else:
        insights.append(('success', 'Data terindikasi baik. Tidak ditemukan masalah signifikan.'))
    return insights
