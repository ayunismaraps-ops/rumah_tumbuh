"""Pengaturan (khusus Pemilik): tambah pengguna, ekspor Excel/PDF."""
import io
import streamlit as st
from app import auth, ledger
from app.money import format_rupiah, format_tanggal


def _excel(rows) -> bytes:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Jurnal Umum"
    ws.append(["Tanggal", "No Jurnal", "Keterangan", "Kode", "Akun", "Debit", "Kredit"])
    for r in rows:
        ws.append([r["tanggal"], r["no_jurnal"], r["keterangan"], r["kode_akun"], r["nama"],
                   r["debit"], r["kredit"]])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def _pdf(rows) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    buf = io.BytesIO()
    data = [["Tanggal", "No", "Akun", "Debit", "Kredit"]]
    for r in rows:
        data.append([format_tanggal(r["tanggal"]), r["no_jurnal"],
                     ("    " if r["kredit"] else "") + f"{r['kode_akun']} {r['nama']}",
                     format_rupiah(r["debit"]) if r["debit"] else "",
                     format_rupiah(r["kredit"]) if r["kredit"] else ""])
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
                           ("GRID", (0, 0), (-1, -1), .25, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 8)]))
    SimpleDocTemplate(buf, pagesize=A4).build([Paragraph("Jurnal Umum - Rumah Tumbuh",
                                                         getSampleStyleSheet()["Title"]), t])
    return buf.getvalue()


def tampil(conn, user):
    st.title("⚙️ Pengaturan")
    st.subheader("Tambah Pengguna")
    nama = st.text_input("Nama")
    username = st.text_input("Username baru")
    pw = st.text_input("Password (min. 8 karakter)", type="password")
    peran = st.selectbox("Peran", ["Pencatat", "Pemilik"],
                         help="Pencatat hanya bisa mencatat & melihat. Pemilik punya akses penuh.")
    if st.button("Tambah Pengguna"):
        e = auth.buat_user(conn, nama, username, pw, peran)
        st.error(e) if e else st.success("Pengguna ditambahkan")

    st.subheader("Ekspor Jurnal Umum")
    rows = ledger.jurnal_umum(conn)
    if rows:
        st.download_button("⬇️ Unduh Excel", _excel(rows), "jurnal_umum.xlsx")
        st.download_button("⬇️ Unduh PDF", _pdf(rows), "jurnal_umum.pdf")
    else:
        st.info("Belum ada data untuk diekspor.")
