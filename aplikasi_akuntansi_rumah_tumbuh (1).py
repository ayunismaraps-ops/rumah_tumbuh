# ==============================================================================
# APLIKASI SISTEM AKUNTANSI KEBUN DURIAN "RUMAH TUMBUH"
# Dibangun menggunakan Python + Streamlit + Database MySQL (Laragon)
# ==============================================================================
# Cara Menjalankan:
# 1. Jalankan Laragon dan klik "Start All" (pastikan MySQL aktif di port 3306).
# 2. Install library: pip install streamlit mysql-connector-python
# 3. Jalankan aplikasi: streamlit run rumah_tumbuh_app.py
# ==============================================================================

import streamlit as st
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Rumah Tumbuh - Akuntansi Kebun Durian (MySQL Laragon)",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk mempercantik tampilan (Tema Hijau Kebun Durian)
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
# KONFIGURASI KONEKSI DATABASE MYSQL (LARAGON)
# ==============================================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Default password MySQL di Laragon adalah kosong
    "port": 3306
}
DB_NAME = "db_rumahtumbuh"

def get_db_connection(use_db=True):
    """Membuka koneksi ke MySQL Laragon."""
    config = DB_CONFIG.copy()
    if use_db:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)

def init_laragon_database():
    """Membuat database, tabel, dan data awal secara otomatis di Laragon jika belum ada."""
    try:
        # 1. Buat Database jika belum ada
        conn = get_db_connection(use_db=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()

        # 2. Buat Tabel-Tabel di dalam db_rumahtumbuh
        conn = get_db_connection(use_db=True)
        cursor = conn.cursor()

        # Tabel COA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coa (
                kode VARCHAR(10) PRIMARY KEY,
                nama_akun VARCHAR(100) NOT NULL,
                klasifikasi VARCHAR(50),
                pos VARCHAR(5),
                laporan VARCHAR(10)
            )
        """)

        # Tabel Jurnal Umum
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jurnal_umum (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tanggal DATE NOT NULL,
                ref VARCHAR(30),
                keterangan VARCHAR(255),
                kode VARCHAR(10),
                nama_akun VARCHAR(100),
                debit BIGINT DEFAULT 0,
                kredit BIGINT DEFAULT 0
            )
        """)

        # Tabel Kartu Persediaan (3 Jenis Durian)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kartu_persediaan (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tanggal DATE NOT NULL,
                jenis_durian VARCHAR(50) NOT NULL,
                keterangan VARCHAR(255),
                masuk_kg DOUBLE DEFAULT 0,
                keluar_kg DOUBLE DEFAULT 0,
                saldo_kg DOUBLE DEFAULT 0,
                harga_pokok BIGINT DEFAULT 0
            )
        """)

        # 3. Isi Data Awal COA jika tabel masih kosong
        cursor.execute("SELECT COUNT(*) FROM coa")
        if cursor.fetchone()[0] == 0:
            data_coa = [
                ("1110", "Kas", "Aset Lancar", "Db", "NRC"),
                ("1120", "Bank", "Aset Lancar", "Db", "NRC"),
                ("1130", "Piutang Usaha", "Aset Lancar", "Db", "NRC"),
                ("1140", "Persediaan Hasil Kebun", "Aset Lancar", "Db", "NRC"),
                ("1141", "Persediaan Hasil Pengepulan", "Aset Lancar", "Db", "NRC"),
                ("1142", "Perlengkapan Kebun (Pupuk/Pestisida)", "Aset Lancar", "Db", "NRC"),
                ("1143", "Persediaan Bibit Tanaman", "Aset Lancar", "Db", "NRC"),
                ("1150", "Uang Muka Pembelian / Persekot", "Aset Lancar", "Db", "NRC"),
                ("1210", "Tanah Kebun", "Aset Tetap", "Db", "NRC"),
                ("1220", "Gudang", "Aset Tetap", "Db", "NRC"),
                ("1221", "Akm. Penyusutan Gudang", "Kontra Aset", "Kr", "NRC"),
                ("1230", "Gubuk Kebun", "Aset Tetap", "Db", "NRC"),
                ("1231", "Akm. Penyusutan Gubuk Kebun", "Kontra Aset", "Kr", "NRC"),
                ("1240", "Tanaman Belum Menghasilkan (TBM)", "Aset Agrikultur", "Db", "NRC"),
                ("1250", "Tanaman Menghasilkan (TM)", "Aset Agrikultur", "Db", "NRC"),
                ("1251", "Akm. Penyusutan Tanaman Menghasilkan", "Kontra Aset", "Kr", "NRC"),
                ("1260", "Peralatan Kebun", "Aset Tetap", "Db", "NRC"),
                ("1261", "Akm. Penyusutan Peralatan", "Kontra Aset", "Kr", "NRC"),
                ("1270", "Kendaraan Operasional", "Aset Tetap", "Db", "NRC"),
                ("1271", "Akm. Penyusutan Kendaraan Operasional", "Kontra Aset", "Kr", "NRC"),
                ("2110", "Utang Usaha", "Liabilitas", "Kr", "NRC"),
                ("2120", "Utang Gaji", "Liabilitas", "Kr", "NRC"),
                ("2130", "Utang Bank", "Liabilitas", "Kr", "NRC"),
                ("2140", "Utang Pajak", "Liabilitas", "Kr", "NRC"),
                ("3110", "Modal", "Ekuitas", "Kr", "NRC"),
                ("3120", "Prive", "Ekuitas", "Db", "NRC"),
                ("4110", "Penjualan Hasil Kebun", "Pendapatan", "Kr", "LR"),
                ("4120", "Penjualan Hasil Pengepulan", "Pendapatan", "Kr", "LR"),
                ("4130", "Pendapatan Lain-Lain", "Pendapatan", "Kr", "LR"),
                ("5110", "HPP Hasil Kebun", "HPP", "Db", "LR"),
                ("5120", "HPP Hasil Pengepulan", "HPP", "Db", "LR"),
                ("5130", "Kerugian Persediaan", "Beban", "Db", "LR"),
                ("6110", "Beban Gaji Karyawan", "Beban Operasional", "Db", "LR"),
                ("6120", "Beban Perawatan dan Kebersihan", "Beban Operasional", "Db", "LR"),
                ("6130", "Beban Listrik dan Air", "Beban Operasional", "Db", "LR"),
                ("6140", "Beban Penyusutan", "Beban Operasional", "Db", "LR"),
                ("6150", "Beban Transportasi", "Beban Operasional", "Db", "LR"),
                ("6160", "Beban Lain-Lain", "Beban Operasional", "Db", "LR"),
                ("6170", "Beban Pupuk dan Pestisida", "Beban Operasional", "Db", "LR"),
                ("6180", "Beban Panen dan Pasca Panen", "Beban Operasional", "Db", "LR"),
                ("6190", "Beban Pemasaran dan Pengiriman", "Beban Operasional", "Db", "LR")
            ]
            cursor.executemany("INSERT INTO coa VALUES (%s, %s, %s, %s, %s)", data_coa)

        # 4. Isi Data Awal Jurnal Umum jika masih kosong
        cursor.execute("SELECT COUNT(*) FROM jurnal_umum")
        if cursor.fetchone()[0] == 0:
            data_jurnal = [
                ("2026-11-02", "TRX-001", "Setoran Modal Awal Pemilik", "1120", "Bank", 150000000, 0),
                ("2026-11-02", "TRX-001", "Setoran Modal Awal Pemilik", "3110", "Modal", 0, 150000000),
                ("2026-11-05", "TRX-002", "Beli Pupuk NPK & Pestisida (Stok)", "1142", "Perlengkapan Kebun (Pupuk/Pestisida)", 5000000, 0),
                ("2026-11-05", "TRX-002", "Beli Pupuk NPK & Pestisida (Stok)", "1110", "Kas", 0, 5000000),
                ("2026-11-10", "TRX-003", "Penjualan Durian Musang King (40 Kg)", "1120", "Bank", 12000000, 0),
                ("2026-11-10", "TRX-003", "Penjualan Durian Musang King (40 Kg)", "4110", "Penjualan Hasil Kebun", 0, 12000000),
                ("2026-11-12", "TRX-004", "Pemakaian Pupuk Pohon Berbuah (TM)", "6170", "Beban Pupuk dan Pestisida", 1500000, 0),
                ("2026-11-12", "TRX-004", "Pemakaian Pupuk Pohon Berbuah (TM)", "1142", "Perlengkapan Kebun (Pupuk/Pestisida)", 0, 1500000),
                ("2026-11-15", "TRX-005", "Pembayaran Upah Buruh Panen", "6180", "Beban Panen dan Pasca Panen", 2500000, 0),
                ("2026-11-15", "TRX-005", "Pembayaran Upah Buruh Panen", "1110", "Kas", 0, 2500000),
            ]
            cursor.executemany(
                "INSERT INTO jurnal_umum (tanggal, ref, keterangan, kode, nama_akun, debit, kredit) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                data_jurnal
            )

        # 5. Isi Data Awal Kartu Persediaan jika masih kosong
        cursor.execute("SELECT COUNT(*) FROM kartu_persediaan")
        if cursor.fetchone()[0] == 0:
            data_stok = [
                ("2026-11-01", "Musang King", "Panen Kebun Blok A", 100.0, 0.0, 100.0, 75000),
                ("2026-11-10", "Musang King", "Penjualan ke Pengepul", 0.0, 40.0, 60.0, 75000),
                ("2026-11-03", "Bawor", "Panen Kebun Blok B", 85.0, 0.0, 85.0, 60000),
                ("2026-11-04", "Montong", "Panen Kebun Blok C", 50.0, 0.0, 50.0, 50000),
            ]
            cursor.executemany(
                "INSERT INTO kartu_persediaan (tanggal, jenis_durian, keterangan, masuk_kg, keluar_kg, saldo_kg, harga_pokok) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                data_stok
            )

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Terhubung ke MySQL Laragon"
    except Error as e:
        return False, str(e)

# Jalankan Inisialisasi Database Laragon
db_connected, db_status_msg = init_laragon_database()

if not db_connected:
    st.error("⚠️ Gagal terhubung ke MySQL Laragon! Pastikan aplikasi **Laragon** sudah dibuka dan tombol **Start All** sudah aktif.")
    st.code(f"Detail Error: {db_status_msg}")
    st.stop()

# ==============================================================================
# FUNGSI QUERY DATABASE (PENGGANTI PANDAS)
# ==============================================================================
def fetch_all_dict(query, params=()):
    """Mengambil hasil query MySQL sebagai list of dictionaries (siap ditampilkan di st.dataframe)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def execute_query(query, params=()):
    """Menjalankan perintah INSERT / UPDATE / DELETE ke MySQL Laragon."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

def format_rp(val):
    return f"Rp {int(val):,}".replace(",", ".")

# Inisialisasi Session State untuk Login & Periode
if 'periode' not in st.session_state:
    st.session_state.periode = "November 2026"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True

# ==============================================================================
# HALAMAN LOGIN
# ==============================================================================
if not st.session_state.logged_in:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        <div class="header-box" style="height: 450px; display: flex; flex-direction: column; justify-content: center;">
            <span style="background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 20px; font-size: 12px; width: fit-content;">DARI KEBUN, UNTUK MASA DEPAN</span>
            <h1 style="color: white; font-size: 38px; margin-top: 15px;">Usaha bertumbuh.<br>Catatan tetap tertata.</h1>
            <p style="color: #d1fae5; font-size: 15px; margin-top: 10px;">Terintegrasi langsung dengan Database MySQL Laragon untuk keamanan data pembukuan kebun durian.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.subheader("Masuk ke Akun Rumah Tumbuh")
        username = st.text_input("Username", value="Rumah_Tumbuh")
        password = st.text_input("Sandi", type="password", value="12345678")
        if st.button("Masuk Dashboard →", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
    st.stop()

# ==============================================================================
# SIDEBAR NAVIGASI UTAMA
# ==============================================================================
with st.sidebar:
    st.markdown("## 🌱 Rumah Tumbuh")
    st.caption(f"Periode Aktif: **{st.session_state.periode}**")
    st.success("🟢 MySQL Laragon Aktif")
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
            <p style="color: #a7f3d0; margin: 0; font-size: 13px;">Database: MySQL Laragon ({DB_NAME}) | Periode: {st.session_state.periode}</p>
        </div>
        <div style="background: rgba(255,255,255,0.15); padding: 8px 16px; border-radius: 10px; font-weight: bold; font-size: 13px;">
            Admin Kebun Durian
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Ambil Data Terbaru dari MySQL Laragon
rows_jurnal = fetch_all_dict("SELECT tanggal, ref, keterangan, kode, nama_akun, debit, kredit FROM jurnal_umum ORDER BY id ASC")
rows_coa = fetch_all_dict("SELECT kode, nama_akun, klasifikasi, pos, laporan FROM coa ORDER BY kode ASC")

# ==============================================================================
# 1. DASHBOARD UTAMA
# ==============================================================================
if menu == "📊 Dashboard":
    st.subheader("Ringkasan Keuangan Periode Berjalan")

    kas_bank = sum(r["debit"] - r["kredit"] for r in rows_jurnal if r["kode"] in ("1110", "1120"))
    pendapatan = sum(r["kredit"] - r["debit"] for r in rows_jurnal if r["kode"].startswith("4"))
    beban = sum(r["debit"] - r["kredit"] for r in rows_jurnal if r["kode"].startswith(("5", "6")))
    laba_berjalan = pendapatan - beban

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kas + Bank Tersedia", format_rp(kas_bank), "Saldo Likuid")
    c2.metric("Total Pendapatan", format_rp(pendapatan), "Hasil Kebun & Pengepulan")
    c3.metric("Total Beban", format_rp(beban), "Pupuk, Panen & Operasional")
    c4.metric("Laba Berjalan", format_rp(laba_berjalan), "Pendapatan - Beban")

    st.divider()
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("#### 🕒 Transaksi Terakhir (Dari Database Laragon)")
        st.dataframe(rows_jurnal[-6:], use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("#### 🔄 Status Siklus Akuntansi")
        st.info("""
        1. **Catat Transaksi** ✅ (Tersimpan ke MySQL)
        2. **Update Kartu Persediaan** ✅ (Otomatis)
        3. **Jurnal Umum & Buku Besar** ✅ (Otomatis)
        4. **Neraca Saldo** ✅ (Seimbang)
        5. **Penyesuaian & Laporan** ⏳ (Siap dicetak)
        6. **Tutup Periode** ⏳ (Menunggu akhir bulan)
        """)

# ==============================================================================
# 2. CATAT TRANSAKSI (SIMPAN KE MYSQL LARAGON)
# ==============================================================================
elif menu == "➕ Catat Transaksi":
    st.subheader("Form Pencatatan Transaksi Kebun Durian")
    st.caption("Data transaksi akan langsung tersimpan permanen ke tabel `jurnal_umum` dan `kartu_persediaan` di Laragon.")

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

        st.markdown("##### 🍈 Detail Persediaan Durian *(Isi jika transaksi penjualan atau panen stok)*")
        c_durian1, c_durian2 = st.columns(2)
        jenis_durian = c_durian1.selectbox("Jenis Durian", ["Tidak Ada (Non-Stok)", "Musang King", "Bawor", "Montong"])
        kuantitas_kg = c_durian2.number_input("Kuantitas (Kg)", min_value=0.0, step=1.0)

        keterangan = st.text_input("Keterangan Transaksi", placeholder="Contoh: Penjualan durian Musang King grade A ke pengepul")
        nominal = st.number_input("Total Nominal (Rp)", min_value=0, step=50000)

        submitted = st.form_submit_button("Simpan ke Database MySQL Laragon", type="primary")

        if submitted:
            if not keterangan or nominal <= 0:
                st.error("Mohon lengkapi keterangan dan nominal lebih dari 0!")
            else:
                ref_baru = f"TRX-00{len(rows_jurnal)//2 + 1}"
                tgl_str = str(tgl)

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

                # Insert Debit & Kredit ke MySQL Laragon
                sql_jurnal = "INSERT INTO jurnal_umum (tanggal, ref, keterangan, kode, nama_akun, debit, kredit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                execute_query(sql_jurnal, (tgl_str, ref_baru, keterangan, debit_acc[0], debit_acc[1], int(nominal), 0))
                execute_query(sql_jurnal, (tgl_str, ref_baru, keterangan, kredit_acc[0], kredit_acc[1], 0, int(nominal)))

                # Update Kartu Persediaan di MySQL jika memilih jenis durian
                if jenis_durian != "Tidak Ada (Non-Stok)" and kuantitas_kg > 0:
                    riwayat_stok = fetch_all_dict("SELECT saldo_kg, harga_pokok FROM kartu_persediaan WHERE jenis_durian = %s ORDER BY id DESC LIMIT 1", (jenis_durian,))
                    saldo_sebelum = riwayat_stok[0]["saldo_kg"] if riwayat_stok else 0.0
                    hpp_sebelum = riwayat_stok[0]["harga_pokok"] if riwayat_stok else 60000

                    if "Penjualan" in kategori:
                        saldo_baru = max(0.0, saldo_sebelum - kuantitas_kg)
                        execute_query(
                            "INSERT INTO kartu_persediaan (tanggal, jenis_durian, keterangan, masuk_kg, keluar_kg, saldo_kg, harga_pokok) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (tgl_str, jenis_durian, keterangan, 0.0, kuantitas_kg, saldo_baru, hpp_sebelum)
                        )
                    elif "Panen" in kategori:
                        saldo_baru = saldo_sebelum + kuantitas_kg
                        execute_query(
                            "INSERT INTO kartu_persediaan (tanggal, jenis_durian, keterangan, masuk_kg, keluar_kg, saldo_kg, harga_pokok) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (tgl_str, jenis_durian, keterangan, kuantitas_kg, 0.0, saldo_baru, hpp_sebelum)
                        )

                st.success(f"Tersimpan di MySQL Laragon! Transaksi **{ref_baru}** berhasil dicatat.")

# ==============================================================================
# 3. JURNAL UMUM
# ==============================================================================
elif menu == "📒 Jurnal Umum":
    st.subheader("Jurnal Umum (General Journal)")
    st.dataframe(rows_jurnal, use_container_width=True, hide_index=True)

    tot_db = sum(r["debit"] for r in rows_jurnal)
    tot_kr = sum(r["kredit"] for r in rows_jurnal)
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
        [f"{a['kode']} - {a['nama_akun']}" for a in rows_coa]
    )
    kode_terpilih = pilihan_akun.split(" - ")[0]

    mutasi_akun = [r for r in rows_jurnal if r["kode"] == kode_terpilih]
    if not mutasi_akun:
        st.warning("Belum ada transaksi pada akun ini di periode berjalan.")
    else:
        saldo_berjalan = 0
        tabel_bb = []
        for m in mutasi_akun:
            saldo_berjalan += (m["debit"] - m["kredit"])
            tabel_bb.append({
                "Tanggal": m["tanggal"],
                "Ref": m["ref"],
                "Keterangan": m["keterangan"],
                "Debit": m["debit"],
                "Kredit": m["kredit"],
                "Saldo Berjalan": saldo_berjalan
            })
        st.dataframe(tabel_bb, use_container_width=True, hide_index=True)

# ==============================================================================
# 5. NERACA SALDO (TRIAL BALANCE)
# ==============================================================================
elif menu == "⚖️ Neraca Saldo":
    st.subheader("Neraca Saldo (Trial Balance)")
    ns_list = []
    for acc in rows_coa:
        kd = acc["kode"]
        nm = acc["nama_akun"]
        db = sum(r["debit"] for r in rows_jurnal if r["kode"] == kd)
        kr = sum(r["kredit"] for r in rows_jurnal if r["kode"] == kd)
        selisih = db - kr
        if selisih > 0:
            ns_list.append({"Kode": kd, "Nama Akun": nm, "Debit": selisih, "Kredit": 0})
        elif selisih < 0:
            ns_list.append({"Kode": kd, "Nama Akun": nm, "Debit": 0, "Kredit": abs(selisih)})

    st.dataframe(ns_list, use_container_width=True, hide_index=True)
    if ns_list:
        c1, c2 = st.columns(2)
        c1.info(f"**Total Saldo Debit:** {format_rp(sum(x['Debit'] for x in ns_list))}")
        c2.info(f"**Total Saldo Kredit:** {format_rp(sum(x['Kredit'] for x in ns_list))}")

# ==============================================================================
# 6. INPUT PENYESUAIAN
# ==============================================================================
elif menu == "🛠️ Input Penyesuaian":
    st.subheader("Input Jurnal Penyesuaian Akhir Periode")
    with st.form("form_penyesuaian"):
        tgl_adj = st.date_input("Tanggal Penyesuaian", datetime(2026, 11, 30))
        ket_adj = st.text_input("Keterangan Penyesuaian", value="Penyusutan Gudang & Peralatan Kebun Bulan November")
        c1, c2 = st.columns(2)
        akun_db = c1.selectbox("Akun Debit (Beban)", ["6140 - Beban Penyusutan", "5130 - Kerugian Persediaan", "6170 - Beban Pupuk dan Pestisida"])
        akun_kr = c2.selectbox("Akun Kredit (Akumulasi / Aset)", ["1221 - Akm. Penyusutan Gudang", "1261 - Akm. Penyusutan Peralatan", "1251 - Akm. Penyusutan Tanaman Menghasilkan", "1142 - Perlengkapan Kebun (Pupuk/Pestisida)"])
        nom_adj = st.number_input("Nominal Penyesuaian (Rp)", min_value=0, value=750000, step=50000)

        if st.form_submit_button("Posting Penyesuaian ke MySQL Laragon", type="primary"):
            kd_db, nm_db = akun_db.split(" - ")
            kd_kr, nm_kr = akun_kr.split(" - ")
            sql_jurnal = "INSERT INTO jurnal_umum (tanggal, ref, keterangan, kode, nama_akun, debit, kredit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            execute_query(sql_jurnal, (str(tgl_adj), "ADJ-001", ket_adj, kd_db, nm_db, int(nom_adj), 0))
            execute_query(sql_jurnal, (str(tgl_adj), "ADJ-001", ket_adj, kd_kr, nm_kr, 0, int(nom_adj)))
            st.success("Jurnal Penyesuaian berhasil tersimpan ke database MySQL Laragon!")

# ==============================================================================
# 7. LAPORAN KEUANGAN (LABA RUGI, NERACA, ARUS KAS)
# ==============================================================================
elif menu == "📈 Laporan Keuangan":
    st.subheader("Laporan Keuangan Kebun Durian")
    tab1, tab2, tab3 = st.tabs(["📄 Laporan Laba Rugi", "🏛️ Laporan Posisi Keuangan (Neraca)", "💵 Laporan Arus Kas"])

    pendapatan = sum(r["kredit"] - r["debit"] for r in rows_jurnal if r["kode"].startswith("4"))
    beban = sum(r["debit"] - r["kredit"] for r in rows_jurnal if r["kode"].startswith(("5", "6")))
    laba_bersih = pendapatan - beban

    with tab1:
        st.markdown(f"### Laporan Laba Rugi — {st.session_state.periode}")
        st.write(f"**Total Pendapatan Usaha:** {format_rp(pendapatan)}")
        st.write(f"**Total Beban Operasional & HPP:** {format_rp(beban)}")
        st.divider()
        st.success(f"### LABA BERSIH PERIODE BERJALAN: {format_rp(laba_bersih)}")

    with tab2:
        st.markdown(f"### Laporan Posisi Keuangan (Neraca) — Per Akhir {st.session_state.periode}")
        total_aset = sum(r["debit"] - r["kredit"] for r in rows_jurnal if r["kode"].startswith("1"))
        total_liabilitas = sum(r["kredit"] - r["debit"] for r in rows_jurnal if r["kode"].startswith("2"))
        total_modal = sum(r["kredit"] - r["debit"] for r in rows_jurnal if r["kode"].startswith("3")) + laba_bersih

        col_a, col_b = st.columns(2)
        col_a.info(f"**TOTAL ASET:** {format_rp(total_aset)}")
        col_b.info(f"**TOTAL LIABILITAS + EKUITAS:** {format_rp(total_liabilitas + total_modal)}")

    with tab3:
        st.markdown(f"### Laporan Arus Kas — {st.session_state.periode}")
        kas_masuk = sum(r["debit"] for r in rows_jurnal if r["kode"] in ("1110", "1120"))
        kas_keluar = sum(r["kredit"] for r in rows_jurnal if r["kode"] in ("1110", "1120"))
        st.write(f"• **Total Arus Kas Masuk:** {format_rp(kas_masuk)}")
        st.write(f"• **Total Arus Kas Keluar:** {format_rp(kas_keluar)}")
        st.success(f"**Saldo Kas & Bank Akhir Periode:** {format_rp(kas_masuk - kas_keluar)}")

# ==============================================================================
# 8. JURNAL PENUTUP
# ==============================================================================
elif menu == "🔒 Jurnal Penutup":
    st.subheader("Jurnal Penutup (Closing Entries)")
    pendapatan = sum(r["kredit"] for r in rows_jurnal if r["kode"].startswith("4"))
    beban = sum(r["debit"] for r in rows_jurnal if r["kode"].startswith(("5", "6")))

    closing_rows = [
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Pendapatan", "Kode": "4110", "Nama Akun": "Penjualan Hasil Kebun", "Debit": pendapatan, "Kredit": 0},
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Pendapatan", "Kode": "3110", "Nama Akun": "Ikhtisar Laba Rugi / Modal", "Debit": 0, "Kredit": pendapatan},
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Beban", "Kode": "3110", "Nama Akun": "Ikhtisar Laba Rugi / Modal", "Debit": beban, "Kredit": 0},
        {"Tanggal": "2026-11-30", "Keterangan": "Menutup Akun Beban", "Kode": "6100", "Nama Akun": "Seluruh Beban Operasional", "Debit": 0, "Kredit": beban},
    ]
    st.dataframe(closing_rows, use_container_width=True, hide_index=True)

# ==============================================================================
# 9. NERACA SALDO SETELAH PENUTUPAN
# ==============================================================================
elif menu == "🛡️ Neraca Saldo Stlh Penutupan":
    st.subheader("Neraca Saldo Setelah Penutupan")
    akun_riil = [a for a in rows_coa if a["laporan"] == "NRC"]
    st.dataframe(akun_riil, use_container_width=True, hide_index=True)

# ==============================================================================
# 10. KARTU PERSEDIAAN (3 JENIS DURIAN DARI MYSQL LARAGON)
# ==============================================================================
elif menu == "📦 Kartu Persediaan (3 Durian)":
    st.subheader("Kartu Persediaan Durian (Musang King, Bawor, Montong)")
    c1, c2, c3 = st.columns(3)

    for idx, jenis in enumerate(["Musang King", "Bawor", "Montong"]):
        data_d = fetch_all_dict("SELECT saldo_kg, harga_pokok FROM kartu_persediaan WHERE jenis_durian = %s ORDER BY id DESC LIMIT 1", (jenis,))
        stok_akhir = data_d[0]["saldo_kg"] if data_d else 0.0
        hpp = data_d[0]["harga_pokok"] if data_d else 0
        col_target = [c1, c2, c3][idx]
        col_target.metric(f"🍈 Durian {jenis}", f"{stok_akhir} Kg", format_rp(stok_akhir * hpp))

    st.divider()
    pilih_durian = st.selectbox("Lihat Rincian Mutasi Kartu Stok:", ["Musang King", "Bawor", "Montong"])
    riwayat_durian = fetch_all_dict("SELECT tanggal, keterangan, masuk_kg, keluar_kg, saldo_kg, harga_pokok FROM kartu_persediaan WHERE jenis_durian = %s ORDER BY id ASC", (pilih_durian,))
    st.dataframe(riwayat_durian, use_container_width=True, hide_index=True)

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
    st.subheader("Daftar Akun (Chart of Accounts) Kebun Durian — MySQL Laragon")
    st.dataframe(rows_coa, use_container_width=True, hide_index=True)