"""Validasi input transaksi. Mengembalikan daftar pesan error (kosong = valid)."""
from datetime import date, datetime
from app.config import BARANG_PENGEPULAN


def validasi(data: dict, aturan: dict) -> list:
    err = []
    a = aturan.get(data.get("jenis_transaksi"))
    if a is None:
        return ["Jenis transaksi tidak dikenal"]

    # Tanggal
    try:
        t = data["tanggal"]
        if not isinstance(t, date):
            datetime.strptime(str(t), "%Y-%m-%d")
    except Exception:
        err.append("Tanggal tidak valid")

    # Nominal
    if int(data.get("nominal") or 0) <= 0:
        err.append("Nominal harus lebih dari 0")

    if not str(data.get("keterangan") or "").strip():
        err.append("Keterangan harus diisi")

    # Kecocokan jenis transaksi & metode pembayaran
    valid = a["pembayaran_valid"].split("|")
    if data.get("metode") not in valid:
        err.append(f"Metode pembayaran '{data.get('metode')}' tidak berlaku untuk {a['jenis_transaksi']}")

    if a["butuh_tujuan"] and not data.get("tujuan"):
        err.append("Tujuan biaya harus dipilih")
    if a["butuh_aset"] and not data.get("aset"):
        err.append("Aset yang disusutkan harus dipilih")
    if a["butuh_barang"] and not data.get("barang"):
        err.append("Barang harus dipilih")

    # Barang pengepulan harus ada jumlahnya (untuk hitung stok & HPP)
    perlu_qty = a["jenis_transaksi"] in ("Jual Hasil Pengepulan", "Beli Hasil Pengepulan") or (
        a["jenis_transaksi"] == "Kerugian Persediaan" and data.get("barang") == BARANG_PENGEPULAN)
    if perlu_qty and float(data.get("jumlah") or 0) <= 0:
        err.append("Jumlah barang harus diisi (lebih dari 0)")
    return err
