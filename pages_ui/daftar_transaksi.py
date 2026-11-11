"""Daftar transaksi: paginasi 20 baris, menu ⋮ (detail jurnal, edit, hapus)."""
import math
import streamlit as st
from app import ledger, services
from app.config import BARIS_PER_HALAMAN
from app.money import format_rupiah, format_tanggal

# st.dialog baru ada di Streamlit 1.37; sebelumnya bernama experimental_dialog
dialog = getattr(st, "dialog", None) or st.experimental_dialog
SPASI = "\u00a0" * 8   # menjorokkan akun kredit


@dialog("Detail Jurnal", width="large")
def dialog_jurnal(conn, tid):
    baris = ledger.baris_jurnal(conn, tid)
    if not baris:
        st.info("Tidak ada jurnal.")
        return
    tampil, jurnal_sebelumnya = [], None
    for b in baris:
        if b["no_jurnal"] != jurnal_sebelumnya:
            jurnal_sebelumnya = b["no_jurnal"]
            tampil.append({"Akun": f"{b['no_jurnal']} ({'HPP' if b['jenis'] == 'hpp' else 'Utama'})",
                           "Debit": "", "Kredit": ""})
        nama = f"{b['kode_akun']} {b['nama']}"
        tampil.append({"Akun": (SPASI + nama) if b["kredit"] else nama,
                       "Debit": format_rupiah(b["debit"]) if b["debit"] else "",
                       "Kredit": format_rupiah(b["kredit"]) if b["kredit"] else ""})
    st.table(tampil)


@dialog("Hapus Transaksi")
def dialog_hapus(conn, tid, user_id):
    st.warning("Transaksi akan ditandai DIBATALKAN dan tidak dihitung lagi. Lanjutkan?")
    c1, c2 = st.columns(2)
    if c1.button("Ya, hapus", type="primary"):
        services.batalkan_transaksi(conn, tid, user_id)
        st.rerun()
    if c2.button("Tidak"):
        st.rerun()


def _mulai_edit(tid):
    st.session_state["edit_id"] = tid
    st.session_state["halaman"] = "Catat Transaksi"


def tampil(conn, user):
    st.title("📋 Daftar Transaksi")
    total = ledger.jumlah_transaksi(conn)
    halaman_total = max(1, math.ceil(total / BARIS_PER_HALAMAN))
    hal = st.number_input("Halaman", 1, halaman_total, 1) if halaman_total > 1 else 1
    st.caption(f"{total} transaksi • halaman {hal} dari {halaman_total}")

    h = st.columns([2, 3, 4, 3, 2, 1])
    for kol, teks in zip(h, ["Tanggal", "Jenis", "Keterangan", "Nominal", "Status", ""]):
        kol.markdown(f"**{teks}**")
    for t in ledger.daftar_transaksi(conn, BARIS_PER_HALAMAN, (hal - 1) * BARIS_PER_HALAMAN):
        c = st.columns([2, 3, 4, 3, 2, 1])
        c[0].write(format_tanggal(t["tanggal"]))
        c[1].write(t["jenis_transaksi"])
        c[2].write(t["keterangan"])
        c[3].write(format_rupiah(t["nominal"]))
        c[4].write("✅ Aktif" if t["status"] == "aktif" else "❌ Dibatalkan")
        with c[5].popover("⋮"):
            if st.button("Lihat Detail Jurnal", key=f"d{t['id']}"):
                dialog_jurnal(conn, t["id"])
            if user["peran"] == "Pemilik" and t["status"] == "aktif":
                st.button("Edit", key=f"e{t['id']}", on_click=_mulai_edit, args=(t["id"],))
                if st.button("Hapus", key=f"h{t['id']}"):
                    dialog_hapus(conn, t["id"], user["id"])
