"""Beranda: ringkasan singkat."""
from datetime import date
import streamlit as st
from app import ledger
from app.money import format_rupiah, format_tanggal


def _ke_catat():
    st.session_state["halaman"] = "Catat Transaksi"


def tampil(conn, user):
    st.title(f"Selamat datang, {user['nama']} 👋")
    st.button("➕ Catat Transaksi", type="primary", on_click=_ke_catat)
    ym = date.today().strftime("%Y-%m")
    k1, k2 = st.columns(2)
    k1.metric("Uang Tunai (Kas)", format_rupiah(ledger.saldo_akun(conn, "1110")))
    k2.metric("Uang di Bank", format_rupiah(ledger.saldo_akun(conn, "1120")))
    k3, k4 = st.columns(2)
    k3.metric("Penjualan Bulan Ini", format_rupiah(ledger.total_penjualan_bulan(conn, ym)))
    k4.metric("Pengeluaran Bulan Ini", format_rupiah(ledger.total_pengeluaran_bulan(conn, ym)))
    st.subheader("5 Transaksi Terakhir")
    baris = [t for t in ledger.daftar_transaksi(conn, 5) if t["status"] == "aktif"]
    if not baris:
        st.info("Belum ada transaksi.")
    for t in baris:
        st.write(f"**{format_tanggal(t['tanggal'])}** — {t['jenis_transaksi']}: "
                 f"{t['keterangan']} — **{format_rupiah(t['nominal'])}**")
