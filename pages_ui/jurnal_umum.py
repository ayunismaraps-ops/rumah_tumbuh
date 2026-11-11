"""Buku Jurnal Umum per bulan."""
from datetime import date
import streamlit as st
from app import ledger
from app.money import format_rupiah, format_tanggal


def tampil(conn, user):
    st.title("📒 Jurnal Umum")
    hari = date.today()
    c1, c2 = st.columns(2)
    tahun = c1.number_input("Tahun", 2000, 2100, hari.year)
    bulan = c2.number_input("Bulan", 1, 12, hari.month)
    rows = ledger.jurnal_umum(conn, f"{int(tahun)}-{int(bulan):02d}")
    if not rows:
        st.info("Belum ada jurnal di bulan ini.")
        return
    tampil_rows, terakhir = [], None
    for r in rows:
        awal = r["no_jurnal"] != terakhir
        terakhir = r["no_jurnal"]
        nama = f"{r['kode_akun']} {r['nama']}"
        tampil_rows.append({"Tanggal": format_tanggal(r["tanggal"]) if awal else "",
                            "No": r["no_jurnal"] if awal else "",
                            "Akun": ("\u00a0" * 8 + nama) if r["kredit"] else nama,
                            "Debit": format_rupiah(r["debit"]) if r["debit"] else "",
                            "Kredit": format_rupiah(r["kredit"]) if r["kredit"] else ""})
    st.table(tampil_rows)
