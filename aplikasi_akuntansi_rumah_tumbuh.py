# ==============================================================================
# APLIKASI SISTEM AKUNTANSI KEBUN DURIAN "RUMAH TUMBUH"
# Dibangun menggunakan Python + Streamlit + Pandas
# ==============================================================================
# Cara Menjalankan:
# 1. Install library yang dibutuhkan: pip install streamlit pandas
# 2. Jalankan aplikasi di terminal: streamlit run rumah_tumbuh_app.py
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Rumah Tumbuh - Akuntansi Kebun Durian",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk mempercantik tampilan (Tema Hijau Kebun Durian / Forest Green)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #14532d;
    }
    .header-box {
        background: linear-gradient(135deg, #0a2918 0%, #166534 100%);
        padding: 20px 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# INISIALISASI DATABASE SEMENTARA (SESSION STATE)
# ==============================================================================

def init_session_state():
    # 1. Daftar Akun (COA) Kebun Durian
    if 'coa' not in st.session_state:
        st.session_state.coa = pd.DataFrame([
            {"Kode": "1110", "Nama Akun": "Kas", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1120", "Nama Akun": "Bank", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1130", "Nama Akun": "Piutang Usaha", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1140", "Nama Akun": "Persediaan Hasil Kebun", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1141", "Nama Akun": "Persediaan Hasil Pengepulan", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1142", "Nama Akun": "Perlengkapan Kebun (Pupuk/Pestisida)", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1143", "Nama Akun": "Persediaan Bibit Tanaman", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1150", "Nama Akun": "Uang Muka Pembelian / Persekot", "Klasifikasi": "Aset Lancar", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1210", "Nama Akun": "Tanah Kebun", "Klasifikasi": "Aset Tetap", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1220", "Nama Akun": "Gudang", "Klasifikasi": "Aset Tetap", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1221", "Nama Akun": "Akm. Penyusutan Gudang", "Klasifikasi": "Kontra Aset", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "1230", "Nama Akun": "Gubuk Kebun", "Klasifikasi": "Aset Tetap", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1231", "Nama Akun": "Akm. Penyusutan Gubuk Kebun", "Klasifikasi": "Kontra Aset", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "1240", "Nama Akun": "Tanaman Belum Menghasilkan (TBM)", "Klasifikasi": "Aset Agrikultur", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1250", "Nama Akun": "Tanaman Menghasilkan (TM)", "Klasifikasi": "Aset Agrikultur", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1251", "Nama Akun": "Akm. Penyusutan Tanaman Menghasilkan", "Klasifikasi": "Kontra Aset", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "1260", "Nama Akun": "Peralatan Kebun", "Klasifikasi": "Aset Tetap", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1261", "Nama Akun": "Akm. Penyusutan Peralatan", "Klasifikasi": "Kontra Aset", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "1270", "Nama Akun": "Kendaraan Operasional", "Klasifikasi": "Aset Tetap", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "1271", "Nama Akun": "Akm. Penyusutan Kendaraan Operasional", "Klasifikasi": "Kontra Aset", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "2110", "Nama Akun": "Utang Usaha", "Klasifikasi": "Liabilitas", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "2120", "Nama Akun": "Utang Gaji", "Klasifikasi": "Liabilitas", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "2130", "Nama Akun": "Utang Bank", "Klasifikasi": "Liabilitas", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "2140", "Nama Akun": "Utang Pajak", "Klasifikasi": "Liabilitas", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "3110", "Nama Akun": "Modal", "Klasifikasi": "Ekuitas", "Pos": "Kr", "Laporan": "NRC"},
            {"Kode": "3120", "Nama Akun": "Prive", "Klasifikasi": "Ekuitas", "Pos": "Db", "Laporan": "NRC"},
            {"Kode": "4110", "Nama Akun": "Penjualan Hasil Kebun", "Klasifikasi": "Pendapatan", "Pos": "Kr", "Laporan": "LR"},
            {"Kode": "4120", "Nama Akun": "Penjualan Hasil Pengepulan", "Klasifikasi": "Pendapatan", "Pos": "Kr", "Laporan": "LR"},
            {"Kode": "4130", "Nama Akun": "Pendapatan Lain-Lain", "Klasifikasi": "Pendapatan", "Pos": "Kr", "Laporan": "LR"},
            {"Kode": "5110", "Nama Akun": "HPP Hasil Kebun", "Klasifikasi": "HPP", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "5120", "Nama Akun": "HPP Hasil Pengepulan", "Klasifikasi": "HPP", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "5130", "Nama Akun": "Kerugian Persediaan", "Klasifikasi": "Beban", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6110", "Nama Akun": "Beban Gaji Karyawan", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6120", "Nama Akun": "Beban Perawatan dan Kebersihan", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6130", "Nama Akun": "Beban Listrik dan Air", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6140", "Nama Akun": "Beban Penyusutan", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6150", "Nama Akun": "Beban Transportasi", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6160", "Nama Akun": "Beban Lain-Lain", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6170", "Nama Akun": "Beban Pupuk dan Pestisida", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6180", "Nama Akun": "Beban Panen dan Pasca Panen", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
            {"Kode": "6190", "Nama Akun": "Beban Pemasaran dan Pengiriman", "Klasifikasi": "Beban Operasional", "Pos": "Db", "Laporan": "LR"},
        ])

    # 2. Jurnal Umum (Transaksi Awal)
    if 'journal' not in st.session_state:
        st.session_state.journal = [
            {"Tanggal": "2026-11-02", "Ref": "TRX-001", "Keterangan": "Setoran Modal Awal Pemilik", "Kode": "1120", "Nama Akun": "Bank", "Debit": 150000000, "Kredit": 0},
            {"Tanggal": "2026-11-02", "Ref": "TRX-001", "Keterangan": "Setoran Modal Awal Pemilik", "Kode": "3110", "Nama Akun": "Modal", "Debit": 0, "Kredit": 150000000},
            {"Tanggal": "2026-11-05", "Ref": "TRX-002", "Keterangan": "Beli Pupuk NPK & Pestisida (Stok)", "Kode": "1142", "Nama Akun": "Perlengkapan Kebun (Pupuk/Pestisida)", "Debit": 5000000, "Kredit": 0},
            {"Tanggal": "2026-11-05", "Ref": "TRX-002", "Keterangan": "Beli Pupuk NPK & Pestisida (Stok)", "Kode": "1110", "Nama Akun": "Kas", "Debit": 0, "Kredit": 5000000},
            {"Tanggal": "2026-11-10", "Ref": "TRX-003", "Keterangan": "Penjualan Durian Musang King (40 Kg)", "Kode": "1120", "Nama Akun": "Bank", "Debit": 12000000, "Kredit": 0},
            {"Tanggal": "2026-11-10", "Ref": "TRX-003", "Keterangan": "Penjualan Durian Musang King (40 Kg)", "Kode": "4110", "Nama Akun": "Penjualan Hasil Kebun", "Debit": 0, "Kredit": 12000000},
            {"Tanggal": "2026-11-12", "Ref": "TRX-004", "Keterangan": "Pemakaian Pupuk Pohon Berbuah (TM)", "Kode": "6170", "Nama Akun": "Beban Pupuk dan Pestisida", "Debit": 1500000, "Kredit": 0},
            {"Tanggal": "2026-11-12", "Ref": "TRX-004", "Keterangan": "Pemakaian Pupuk Pohon Berbuah (TM)", "Kode": "1142", "Nama Akun": "Perlengkapan Kebun (Pupuk/Pestisida)", "Debit": 0, "Kredit": 1500000},
            {"Tanggal": "2026-11-15", "Ref": "TRX-005", "Keterangan": "Pembayaran Upah Buruh Panen", "Kode": "6180", "Nama Akun": "Beban Panen dan Pasca Panen", "Debit": 2500000, "Kredit": 0},
            {"Tanggal": "2026-11-15", "Ref": "TRX-005", "Keterangan": "Pembayaran Upah Buruh Panen", "Kode": "1110", "Nama Akun": "Kas", "Debit": 0, "Kredit": 2500000},
        ]

    # 3. Kartu Persediaan 3 Jenis Durian
    if 'inventory' not in st.session_state:
        st.session_state.inventory = {
            "Musang King": {"stok": 60.0, "harga_pokok": 75000, "riwayat": [
                {"Tanggal": "2026-11-01", "Keterangan": "Panen Kebun Blok A", "Masuk (Kg)": 100.0, "Keluar (Kg)": 0.0, "Saldo (Kg)": 100.0},
                {"Tanggal": "2026-11-10", "Keterangan": "Penjualan ke Pengepul", "Masuk (Kg)": 0.0, "Keluar (Kg)": 40.0, "Saldo (Kg)": 60.0},
            ]},
            "Bawor": {"stok": 85.0, "harga_pokok": 60000, "riwayat": [
                {"Tanggal": "2026-11-03", "Keterangan": "Panen Kebun Blok B", "Masuk (Kg)": 85.0, "Keluar (Kg)": 0.0, "Saldo (Kg)": 85.0},
            ]},
            "Montong": {"stok": 50.0, "harga_pokok": 50000, "riwayat": [
                {"Tanggal": "2026-11-04", "Keterangan": "Panen Kebun Blok C", "Masuk (Kg)": 50.0, "Keluar (Kg)": 0.0, "Saldo (Kg)": 50.0},
            ]}
        }

    # 4. Periode Akuntansi Aktif
    if 'periode' not in st.session_state:
        st.session_state.periode = "November 2026"

    # 5. Status Login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True

init_session_state()

# Fungsi Helper Format Rupiah
def format_rp(val):
    return f"Rp {val:,.0f}".replace(",", ".")

# ==============================================================================
# HALAMAN LOGIN (SESUAI SCREENSHOT AWAL)
# ==============================================================================
if not st.session_state.logged_in:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        <div class="header-box" style="height: 450px; display: flex; flex-direction: column; justify-content: center;">
            <span style="background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 20px; font-size: 12px; width: fit-content;">DARI KEBUN, UNTUK MASA DEPAN</span>
            <h1 style="color: white; font-size: 38px; margin-top: 15px;">Usaha bertumbuh.<br>Catatan tetap tertata.</h1>
            <p style="color: #d1fae5; font-size: 15px; margin-top: 10px;">Satu tempat untuk melihat perjalanan keuangan hasil kebun durian dan pengepulan Anda.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.subheader("Masuk ke Akun Rumah Tumbuh")
        st.caption("Masukkan detail pengguna untuk mengakses pembukuan kebun.")
        username = st.text_input("Username", value="Rumah_Tumbuh")
        password = st.text_input("Sandi", type="password", value="12345678")
        if st.button("Masuk Dashboard →", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ==============================================================================
# SIDEBAR NAVIGASI UTAMA (SESUAI FLOWCHART)
# ==============================================================================
with st.sidebar:
    st.markdown("## 🌱 Rumah Tumbuh")
    st.caption(f"Periode Aktif: **{st.session_state.periode}**")
    st.divider()

    menu = st.radio(
        "MENU PEMBUKUAN & SIKLUS",
        [
            "📊 Dashboard",
            "➕ Catat Transaksi",
            "📒 Jurnal Umum",
            "📖 Buku Besar",
            "⚖️ Neraca Saldo",
            "🛠️ Input Penyesuaian",
            "📈 Laporan Keuangan",
            "🔒 Jurnal Penutup",
            "🛡️ Neraca Saldo Stlh Penutupan",
            "📦 Kartu Persediaan (3 Durian)",
            "🧾 Invoice & Form Pesanan",
            "🗓️ Periode Akuntansi",
            "🗂️ Daftar Akun (COA)"
        ]
    )

    st.divider()
    if st.button("Keluar Akun", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# Header Atas
st.markdown(f"""
<div class="header-box">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="color: white; margin: 0;">Sistem Akuntansi Kebun Durian</h2>
            <p style="color: #a7f3d0; margin: 0; font-size: 13px;">Periode Pembukuan Aktif: {st.session_state.periode}</p>
        </div>
        <div style="background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 10px; font-weight: bold; font-size: 13px;">
            Admin Kebun Durian
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

df_journal = pd.DataFrame(st.session_state.journal)

# ==============================================================================
# 1. DASHBOARD UTAMA
# ==============================================================================
if menu == "📊 Dashboard":
    st.subheader("Ringkasan Keuangan Periode Berjalan")

    # Hitung Metrik Otomatis dari Jurnal
    kas_bank = df_journal[df_journal["Kode"].isin(["1110", "1120"])]["Debit"].sum() - df_journal[df_journal["Kode"].isin(["1110", "1120"])]["Kredit"].sum()
    pendapatan = df_journal[df_journal["Kode"].str.startswith("4")]["Kredit"].sum() - df_journal[df_journal["Kode"].str.startswith("4")]["Debit"].sum()
    beban = df_journal[df_journal["Kode"].str.startswith(("5", "6"))]["Debit"].sum() - df_journal[df_journal["Kode"].str.startswith(("5", "6"))]["Kredit"].sum()
    laba_berjalan = pendapatan - beban

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kas + Bank Tersedia", format_rp(kas_bank), "Saldo Likuid")
    c2.metric("Total Pendapatan", format_rp(pendapatan), "Hasil Kebun & Pengepulan")
    c3.metric("Total Beban", format_rp(beban), "Pupuk, Panen & Operasional")
    c4.metric("Laba Berjalan", format_rp(laba_berjalan), "Pendapatan - Beban")

    st.divider()
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("#### 🕒 Transaksi Terakhir")
        st.dataframe(df_journal.tail(6), use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("#### 🔄 Status Siklus Akuntansi")
        st.info("""
        1. **Catat Transaksi** ✅ (Aktif)
        2. **Update Kartu Persediaan** ✅ (Otomatis)
        3. **Jurnal Umum & Buku Besar** ✅ (Otomatis)
        4. **Neraca Saldo** ✅ (Seimbang)
        5. **Penyesuaian & Laporan** ⏳ (Siap dicetak)
        6. **Tutup Periode** ⏳ (Menunggu akhir bulan)
        """)

# ==============================================================================
# 2. CATAT TRANSAKSI (TERINTEGRASI DENGAN KARTU PERSEDIAAN 3 DURIAN)
# ==============================================================================
elif menu == "➕ Catat Transaksi":
    st.subheader("Form Pencatatan Transaksi Kebun Durian")
    st.caption("Pilih kategori transaksi. Jika menjual/panen stok durian, kartu persediaan akan otomatis terupdate.")

    with st.form("form_transaksi"):
        col1, col2 = st.columns(2)
        tgl = col1.date_input("Tanggal Transaksi", datetime(2026, 11, 16))
        kategori = col2.selectbox("Kategori Transaksi", [
            "Pemasukan - Penjualan Hasil Kebun Durian",
            "Panen Masuk Gudang (Tambah Stok Durian)",
            "Pengeluaran - Pembelian Pupuk/Pestisida (Stok)",
            "Pengeluaran - Pemakaian Pupuk (Pohon Berbuah/TM)",
            "Pengeluaran - Pemakaian Pupuk (Pohon Muda/TBM)",
            "Pengeluaran - Beban Panen & Pasca Panen",
            "Pengeluaran - Beban Gaji Karyawan",
            "Transaksi Lainnya - Setoran Modal"
        ])

        # Input khusus stok durian jika berkaitan dengan penjualan atau panen
        st.markdown("##### 🍈 Detail Persediaan Durian *(Isi jika transaksi penjualan atau panen stok)*")
        c_durian1, c_durian2 = st.columns(2)
        jenis_durian = c_durian1.selectbox("Jenis Durian", ["Tidak Ada (Non-Stok)", "Musang King", "Bawor", "Montong"])
        kuantitas_kg = c_durian2.number_input("Kuantitas (Kg)", min_value=0.0, step=1.0)

        keterangan = st.text_input("Keterangan Transaksi", placeholder="Contoh: Penjualan durian Musang King grade A ke pengepul")
        nominal = st.number_input("Total Nominal (Rp)", min_value=0, step=50000)

        submitted = st.form_submit_button("Simpan Transaksi ke Jurnal & Persediaan", type="primary")

        if submitted:
            if not keterangan or nominal <= 0:
                st.error("Mohon lengkapi keterangan dan nominal lebih dari 0!")
            else:
                ref_baru = f"TRX-00{len(st.session_state.journal)//2 + 1}"
                tgl_str = str(tgl)

                # Mapping Akun Otomatis Sesuai Flowchart
                if kategori == "Pemasukan - Penjualan Hasil Kebun Durian":
                    debit_acc = ("1120", "Bank")
                    kredit_acc = ("4110", "Penjualan Hasil Kebun")
                elif kategori == "Panen Masuk Gudang (Tambah Stok Durian)":
                    debit_acc = ("1140", "Persediaan Hasil Kebun")
                    kredit_acc = ("4110", "Penjualan Hasil Kebun")
                elif kategori == "Pengeluaran - Pembelian Pupuk/Pestisida (Stok)":
                    debit_acc = ("1142", "Perlengkapan Kebun (Pupuk/Pestisida)")
                    kredit_acc = ("1110", "Kas")
                elif kategori == "Pengeluaran - Pemakaian Pupuk (Pohon Berbuah/TM)":
                    debit_acc = ("6170", "Beban Pupuk dan Pestisida")
                    kredit_acc = ("1142", "Perlengkapan Kebun (Pupuk/Pestisida)")
                elif kategori == "Pengeluaran - Pemakaian Pupuk (Pohon Muda/TBM)":
                    debit_acc = ("1240", "Tanaman Belum Menghasilkan (TBM)")
                    kredit_acc = ("1142", "Perlengkapan Kebun (Pupuk/Pestisida)")
                elif kategori == "Pengeluaran - Beban Panen & Pasca Panen":
                    debit_acc = ("6180", "Beban Panen dan Pasca Panen")
                    kredit_acc = ("1110", "Kas")
                elif kategori == "Pengeluaran - Beban Gaji Karyawan":
                    debit_acc = ("6110", "Beban Gaji Karyawan")
                    kredit_acc = ("1110", "Kas")
                else:
                    debit_acc = ("1120", "Bank")
                    kredit_acc = ("3110", "Modal")

                # Tambahkan ke Jurnal Umum
                st.session_state.journal.append({
                    "Tanggal": tgl_str, "Ref": ref_baru, "Keterangan": keterangan,
                    "Kode": debit_acc[0], "Nama Akun": debit_acc[1], "Debit": nominal, "Kredit": 0
                })
                st.session_state.journal.append({
                    "Tanggal": tgl_str, "Ref": ref_baru, "Keterangan": keterangan,
                    "Kode": kredit_acc[0], "Nama Akun": kredit_acc[1], "Debit": 0, "Kredit": nominal
                })

                # Update Kartu Persediaan jika memilih jenis durian
                if jenis_durian != "Tidak Ada (Non-Stok)" and kuantitas_kg > 0:
                    inv = st.session_state.inventory[jenis_durian]
                    if "Penjualan" in kategori:
                        inv["stok"] = max(0.0, inv["stok"] - kuantitas_kg)
                        inv["riwayat"].append({
                            "Tanggal": tgl_str, "Keterangan": keterangan,
                            "Masuk (Kg)": 0.0, "Keluar (Kg)": kuantitas_kg, "Saldo (Kg)": inv["stok"]
                        })
                    elif "Panen" in kategori:
                        inv["stok"] += kuantitas_kg
                        inv["riwayat"].append({
                            "Tanggal": tgl_str, "Keterangan": keterangan,
                            "Masuk (Kg)": kuantitas_kg, "Keluar (Kg)": 0.0, "Saldo (Kg)": inv["stok"]
                        })

                st.success(f"Berhasil! Transaksi **{ref_baru}** telah masuk ke Jurnal Umum dan Kartu Persediaan diperbarui.")

# ==============================================================================
# 3. JURNAL UMUM
# ==============================================================================
elif menu == "📒 Jurnal Umum":
    st.subheader("Jurnal Umum (General Journal)")
    st.dataframe(df_journal, use_container_width=True, hide_index=True)

    tot_db = df_journal["Debit"].sum()
    tot_kr = df_journal["Kredit"].sum()
    col1, col2 = st.columns(2)
    col1.success(f"**Total Debit:** {format_rp(tot_db)}")
    col2.success(f"**Total Kredit:** {format_rp(tot_kr)}")

# ==============================================================================
# 4. BUKU BESAR (GENERAL LEDGER)
# ==============================================================================
elif menu == "📖 Buku Besar":
    st.subheader("Buku Besar (General Ledger)")
    pilihan_akun = st.selectbox(
        "Pilih Akun untuk Melihat Mutasi:",
        st.session_state.coa["Kode"] + " - " + st.session_state.coa["Nama Akun"]
    )
    kode_terpilih = pilihan_akun.split(" - ")[0]

    df_akun = df_journal[df_journal["Kode"] == kode_terpilih].copy()
    if df_akun.empty:
        st.warning("Belum ada transaksi pada akun ini di periode berjalan.")
    else:
        df_akun["Saldo Berjalan"] = (df_akun["Debit"] - df_akun["Kredit"]).cumsum()
        st.dataframe(df_akun[["Tanggal", "Ref", "Keterangan", "Debit", "Kredit", "Saldo Berjalan"]], use_container_width=True, hide_index=True)

# ==============================================================================
# 5. NERACA SALDO (TRIAL BALANCE)
# ==============================================================================
elif menu == "⚖️ Neraca Saldo":
    st.subheader("Neraca Saldo (Trial Balance)")
    ns_list = []
    for _, row in st.session_state.coa.iterrows():
        kd = row["Kode"]
        nm = row["Nama Akun"]
        db = df_journal[df_journal["Kode"] == kd]["Debit"].sum()
        kr = df_journal[df_journal["Kode"] == kd]["Kredit"].sum()
        selisih = db - kr
        if selisih > 0:
            ns_list.append({"Kode": kd, "Nama Akun": nm, "Debit": selisih, "Kredit": 0})
        elif selisih < 0:
            ns_list.append({"Kode": kd, "Nama Akun": nm, "Debit": 0, "Kredit": abs(selisih)})

    df_ns = pd.DataFrame(ns_list)
    st.dataframe(df_ns, use_container_width=True, hide_index=True)
    if not df_ns.empty:
        c1, c2 = st.columns(2)
        c1.info(f"**Total Saldo Debit:** {format_rp(df_ns['Debit'].sum())}")
        c2.info(f"**Total Saldo Kredit:** {format_rp(df_ns['Kredit'].sum())}")

# ==============================================================================
# 6. INPUT PENYESUAIAN
# ==============================================================================
elif menu == "🛠️ Input Penyesuaian":
    st.subheader("Input Jurnal Penyesuaian Akhir Periode")
    st.caption("Digunakan untuk mencatat penyusutan aset tetap (Gudang, Peralatan, Kendaraan, Tanaman Menghasilkan) atau selisih stok.")

    with st.form("form_penyesuaian"):
        tgl_adj = st.date_input("Tanggal Penyesuaian", datetime(2026, 11, 30))
        ket_adj = st.text_input("Keterangan Penyesuaian", value="Penyusutan Gudang & Peralatan Kebun Bulan November")
        c1, c2 = st.columns(2)
        akun_db = c1.selectbox("Akun Debit (Beban)", ["6140 - Beban Penyusutan", "5130 - Kerugian Persediaan", "6170 - Beban Pupuk dan Pestisida"])
        akun_kr = c2.selectbox("Akun Kredit (Akumulasi / Aset)", ["1221 - Akm. Penyusutan Gudang", "1261 - Akm. Penyusutan Peralatan", "1251 - Akm. Penyusutan Tanaman Menghasilkan", "1142 - Perlengkapan Kebun (Pupuk/Pestisida)"])
        nom_adj = st.number_input("Nominal Penyesuaian (Rp)", min_value=0, value=750000, step=50000)

        if st.form_submit_button("Posting Jurnal Penyesuaian", type="primary"):
            kd_db, nm_db = akun_db.split(" - ")
            kd_kr, nm_kr = akun_kr.split(" - ")
            st.session_state.journal.append({"Tanggal": str(tgl_adj), "Ref": "ADJ-001", "Keterangan": ket_adj, "Kode": kd_db, "Nama Akun": nm_db, "Debit": nom_adj, "Kredit": 0})
            st.session_state.journal.append({"Tanggal": str(tgl_adj), "Ref": "ADJ-001", "Keterangan": ket_adj, "Kode": kd_kr, "Nama Akun": nm_kr, "Debit": 0, "Kredit": nom_adj})
            st.success("Jurnal Penyesuaian berhasil ditambahkan ke Jurnal Umum dan Buku Besar!")

# ==============================================================================
# 7. LAPORAN KEUANGAN (LABA RUGI, NERACA, ARUS KAS)
# ==============================================================================
elif menu == "📈 Laporan Keuangan":
    st.subheader("Laporan Keuangan Kebun Durian")
    tab1, tab2, tab3 = st.tabs(["📄 Laporan Laba Rugi", "🏛️ Laporan Posisi Keuangan (Neraca)", "💵 Laporan Arus Kas"])

    pendapatan = df_journal[df_journal["Kode"].str.startswith("4")]["Kredit"].sum() - df_journal[df_journal["Kode"].str.startswith("4")]["Debit"].sum()
    beban = df_journal[df_journal["Kode"].str.startswith(("5", "6"))]["Debit"].sum() - df_journal[df_journal["Kode"].str.startswith(("5", "6"))]["Kredit"].sum()
    laba_bersih = pendapatan - beban

    with tab1:
        st.markdown(f"### Laporan Laba Rugi — {st.session_state.periode}")
        st.write(f"**Total Pendapatan Usaha:** {format_rp(pendapatan)}")
        st.write(f"**Total Beban Operasional & HPP:** {format_rp(beban)}")
        st.divider()
        st.success(f"### LABA BERSIH PERIODE BERJALAN: {format_rp(laba_bersih)}")

    with tab2:
        st.markdown(f"### Laporan Posisi Keuangan (Neraca) — Per Akhir {st.session_state.periode}")
        total_aset = df_journal[df_journal["Kode"].str.startswith("1")]["Debit"].sum() - df_journal[df_journal["Kode"].str.startswith("1")]["Kredit"].sum()
        total_liabilitas = df_journal[df_journal["Kode"].str.startswith("2")]["Kredit"].sum() - df_journal[df_journal["Kode"].str.startswith("2")]["Debit"].sum()
        total_modal = df_journal[df_journal["Kode"].str.startswith("3")]["Kredit"].sum() - df_journal[df_journal["Kode"].str.startswith("3")]["Debit"].sum() + laba_bersih

        col_a, col_b = st.columns(2)
        with col_a:
            st.info(f"**TOTAL ASET:** {format_rp(total_aset)}")
        with col_b:
            st.info(f"**TOTAL LIABILITAS + EKUITAS:** {format_rp(total_liabilitas + total_modal)}")

    with tab3:
        st.markdown(f"### Laporan Arus Kas — {st.session_state.periode}")
        kas_masuk = df_journal[df_journal["Kode"].isin(["1110", "1120"])]["Debit"].sum()
        kas_keluar = df_journal[df_journal["Kode"].isin(["1110", "1120"])]["Kredit"].sum()
        st.write(f"• **Total Arus Kas Masuk (Operasi & Pendanaan):** {format_rp(kas_masuk)}")
        st.write(f"• **Total Arus Kas Keluar (Pembelian & Beban):** {format_rp(kas_keluar)}")
        st.success(f"**Saldo Kas & Bank Akhir Periode:** {format_rp(kas_masuk - kas_keluar)}")

# ==============================================================================
# 8. JURNAL PENUTUP
# ==============================================================================
elif menu == "🔒 Jurnal Penutup":
    st.subheader("Jurnal Penutup (Closing Entries)")
    st.caption("Menutup akun nominal (Pendapatan dan Beban) ke Modal / Ikhtisar Laba Rugi pada akhir periode.")
    pendapatan = df_journal[df_journal["Kode"].str.startswith("4")]["Kredit"].sum()
    beban = df_journal[df_journal["Kode"].str.startswith(("5", "6"))]["Debit"].sum()

    df_closing = pd.DataFrame([
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Pendapatan", "Kode": "4110", "Nama Akun": "Penjualan Hasil Kebun", "Debit": pendapatan, "Kredit": 0},
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Pendapatan", "Kode": "3110", "Nama Akun": "Ikhtisar Laba Rugi / Modal", "Debit": 0, "Kredit": pendapatan},
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Beban", "Kode": "3110", "Nama Akun": "Ikhtisar Laba Rugi / Modal", "Debit": beban, "Kredit": 0},
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Beban", "Kode": "6100", "Nama Akun": "Seluruh Beban Operasional", "Debit": 0, "Kredit": beban},
    ])
    st.dataframe(df_closing, use_container_width=True, hide_index=True)

# ==============================================================================
# 9. NERACA SALDO SETELAH PENUTUPAN
# ==============================================================================
elif menu == "🛡️ Neraca Saldo Stlh Penutupan":
    st.subheader("Neraca Saldo Setelah Penutupan")
    st.caption("Hanya menampilkan akun riil (Aset, Liabilitas, Ekuitas) yang akan dibawa ke periode berikutnya.")
    df_riil = st.session_state.coa[st.session_state.coa["Laporan"] == "NRC"]
    st.dataframe(df_riil, use_container_width=True, hide_index=True)

# ==============================================================================
# 10. KARTU PERSEDIAAN (3 JENIS DURIAN)
# ==============================================================================
elif menu == "📦 Kartu Persediaan (3 Durian)":
    st.subheader("Kartu Persediaan Durian (Musang King, Bawor, Montong)")
    c1, c2, c3 = st.columns(3)
    inv = st.session_state.inventory

    c1.metric("🍈 Durian Musang King", f"{inv['Musang King']['stok']} Kg", format_rp(inv['Musang King']['stok'] * inv['Musang King']['harga_pokok']))
    c2.metric("🍈 Durian Bawor", f"{inv['Bawor']['stok']} Kg", format_rp(inv['Bawor']['stok'] * inv['Bawor']['harga_pokok']))
    c3.metric("🍈 Durian Montong", f"{inv['Montong']['stok']} Kg", format_rp(inv['Montong']['stok'] * inv['Montong']['harga_pokok']))

    st.divider()
    pilih_durian = st.selectbox("Lihat Rincian Mutasi Kartu Stok:", ["Musang King", "Bawor", "Montong"])
    df_riwayat_stok = pd.DataFrame(inv[pilih_durian]["riwayat"])
    st.dataframe(df_riwayat_stok, use_container_width=True, hide_index=True)

# ==============================================================================
# 11. INVOICE & FORM INPUT PEMESANAN
# ==============================================================================
elif menu == "🧾 Invoice & Form Pesanan":
    st.subheader("Form Input Pemesanan & Cetak Invoice")
    with st.form("form_invoice"):
        pembeli = st.text_input("Nama Pembeli / Pengepul", value="Depot Durian Berkah")
        alamat = st.text_input("Alamat Pengiriman", value="Pasar Buah Sentral Bogor")
        c1, c2, c3 = st.columns(3)
        item_durian = c1.selectbox("Jenis Durian", ["Musang King", "Bawor", "Montong"])
        qty_pesan = c2.number_input("Jumlah Pesanan (Kg)", min_value=1, value=40)
        harga_jual = c3.number_input("Harga Jual per Kg (Rp)", min_value=10000, value=150000, step=5000)

        if st.form_submit_button("Buat Nota / Invoice", type="primary"):
            total_inv = qty_pesan * harga_jual
            st.success("Invoice berhasil dibuat!")
            st.markdown(f"""
            ---
            ### 🧾 INVOICE PENJUALAN DURIAN — RUMAH TUMBUH
            * **Kepada:** {pembeli} ({alamat})
            * **Tanggal:** {datetime.now().strftime('%d-%m-%Y')}
            * **Produk:** Durian {item_durian} — **{qty_pesan} Kg** x {format_rp(harga_jual)}
            * **TOTAL TAGIHAN:** **{format_rp(total_inv)}**
            ---
            """)

# ==============================================================================
# 12. PERIODE AKUNTANSI
# ==============================================================================
elif menu == "🗓️ Periode Akuntansi":
    st.subheader("Manajemen Periode Akuntansi")
    st.info(f"Periode Pembukuan Aktif Saat Ini: **{st.session_state.periode}**")
    periode_baru = st.selectbox("Pilih Periode Baru untuk Tutup Buku:", ["Desember 2026", "Januari 2027", "Februari 2027"])
    if st.button("Tutup Periode Sekarang & Buka Periode Baru", type="primary"):
        st.session_state.periode = periode_baru
        st.success(f"Periode berhasil dipindahkan ke **{periode_baru}**!")
        st.rerun()

# ==============================================================================
# 13. DAFTAR AKUN (COA)
# ==============================================================================
elif menu == "🗂️ Daftar Akun (COA)":
    st.subheader("Daftar Akun (Chart of Accounts) Kebun Durian")
    st.dataframe(st.session_state.coa, use_container_width=True, hide_index=True)