"""Pintu masuk aplikasi: cek login lalu tampilkan halaman. Jalankan: streamlit run main.py"""
import streamlit as st
from app import db, auth
from pages_ui import login, dashboard, catat_transaksi, daftar_transaksi, jurnal_umum, pengaturan

st.set_page_config(page_title="Rumah Tumbuh", page_icon="🌱", layout="wide")
# Huruf besar & jelas untuk pengguna awam
st.markdown("""<style>html, body, [class*="css"] {font-size: 19px;}
div.stButton > button {font-size: 19px; padding: .5rem 1.2rem;}</style>""", unsafe_allow_html=True)


@st.cache_resource
def koneksi():
    db.init_db()          # buat tabel & data awal bila belum ada
    return db.get_conn()


conn = koneksi()

if not auth.ada_user(conn):
    login.buat_akun_pemilik(conn)
elif "user" not in st.session_state:
    login.tampil_login(conn)
else:
    user = st.session_state["user"]
    halaman = {"Beranda": dashboard, "Catat Transaksi": catat_transaksi,
               "Daftar Transaksi": daftar_transaksi, "Jurnal Umum": jurnal_umum}
    if user["peran"] == "Pemilik":
        halaman["Pengaturan"] = pengaturan
    st.sidebar.title("🌱 Rumah Tumbuh")
    st.sidebar.write(f"Halo, **{user['nama']}** ({user['peran']})")
    pilih = st.sidebar.radio("Menu", list(halaman), key="halaman")
    if st.sidebar.button("Keluar"):
        del st.session_state["user"]
        st.rerun()
    halaman[pilih].tampil(conn, user)
