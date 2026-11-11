"""Penyimpanan transaksi yang atomik: validasi -> jurnal -> database -> audit."""
from app import audit, inventory
from app.config import BARANG_PENGEPULAN
from app.journal_engine import bangun_jurnal
from app.money import ke_tanggal_iso
from app.validators import validasi


class ValidasiError(Exception):
    def __init__(self, errors):
        super().__init__("; ".join(errors))
        self.errors = errors


class StokKurang(Exception):
    """Stok hasil pengepulan tidak cukup; perlu konfirmasi pengguna."""
    def __init__(self, tersedia, diminta):
        super().__init__(f"Stok tersedia {tersedia:g}, diminta {diminta:g}")
        self.tersedia, self.diminta = tersedia, diminta


def _no_jurnal_berikut(conn) -> str:
    n = conn.execute("SELECT COALESCE(MAX(CAST(substr(no_jurnal,4) AS INTEGER)),0) FROM journals").fetchone()[0]
    return f"JU-{n + 1:04d}"


def _sisipkan(conn, data, aturan, user_id, konfirmasi_stok) -> int:
    jenis = data["jenis_transaksi"]
    tgl = ke_tanggal_iso(data["tanggal"])
    nominal = int(data["nominal"])
    jumlah = float(data.get("jumlah") or 0)

    # Hitung HPP (khusus jual hasil pengepulan) sebelum menyimpan
    hpp = 0
    if jenis == "Jual Hasil Pengepulan":
        stok, _ = inventory.stok_dan_nilai(conn, BARANG_PENGEPULAN)
        if jumlah > stok and not konfirmasi_stok:
            raise StokKurang(stok, jumlah)
        hpp = inventory.hitung_hpp(conn, BARANG_PENGEPULAN, jumlah)

    jurnal = bangun_jurnal(aturan[jenis], data, nominal, hpp)

    cur = conn.execute("""INSERT INTO transactions(tanggal,jenis_transaksi,metode_bayar,keterangan,jumlah,
        satuan,harga_satuan,nominal,pihak,no_invoice,blok_lahan,catatan,tujuan,aset,barang,dibuat_oleh)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (tgl, jenis, data["metode"], data["keterangan"].strip(), jumlah or None, data.get("satuan"),
         data.get("harga_satuan"), nominal, data.get("pihak"), data.get("no_invoice"),
         data.get("blok_lahan"), data.get("catatan"), data.get("tujuan"), data.get("aset"),
         data.get("barang"), user_id))
    tid = cur.lastrowid

    for j in jurnal:
        no = _no_jurnal_berikut(conn)
        jid = conn.execute("INSERT INTO journals(no_jurnal,transaction_id,tanggal,keterangan,jenis) "
                           "VALUES(?,?,?,?,?)", (no, tid, tgl, data["keterangan"].strip(), j["jenis"])).lastrowid
        for b in j["baris"]:
            conn.execute("INSERT INTO journal_lines(journal_id,kode_akun,debit,kredit) VALUES(?,?,?,?)",
                         (jid, b["kode"], b["debit"], b["kredit"]))

    # Catat pergerakan stok hasil pengepulan
    if jenis == "Beli Hasil Pengepulan":
        conn.execute("INSERT INTO stock_movements(transaction_id,barang,tanggal,qty,nilai) VALUES(?,?,?,?,?)",
                     (tid, BARANG_PENGEPULAN, tgl, jumlah, nominal))
    elif jenis == "Jual Hasil Pengepulan":
        conn.execute("INSERT INTO stock_movements(transaction_id,barang,tanggal,qty,nilai) VALUES(?,?,?,?,?)",
                     (tid, BARANG_PENGEPULAN, tgl, -jumlah, -hpp))
    elif jenis == "Kerugian Persediaan" and data.get("barang") == BARANG_PENGEPULAN:
        conn.execute("INSERT INTO stock_movements(transaction_id,barang,tanggal,qty,nilai) VALUES(?,?,?,?,?)",
                     (tid, BARANG_PENGEPULAN, tgl, -jumlah, -nominal))
    return tid


def simpan_transaksi(conn, data: dict, user_id=None, konfirmasi_stok=False, ganti_id=None) -> int:
    """Simpan satu transaksi + jurnalnya dalam satu blok database.
    ganti_id: jika diisi (mode Edit), transaksi lama ditandai dibatalkan di blok yang sama."""
    aturan = _aturan(conn)
    errors = validasi(data, aturan)
    if errors:
        raise ValidasiError(errors)
    conn.execute("BEGIN")
    try:
        if ganti_id:
            conn.execute("UPDATE transactions SET status='dibatalkan' WHERE id=?", (ganti_id,))
        tid = _sisipkan(conn, data, aturan, user_id, konfirmasi_stok)
        aksi = "edit_transaksi" if ganti_id else "tambah_transaksi"
        audit.catat(conn, user_id, aksi, f"id={tid} jenis={data['jenis_transaksi']} "
                    f"nominal={data['nominal']}" + (f" menggantikan id={ganti_id}" if ganti_id else ""))
        conn.execute("COMMIT")
        return tid
    except Exception:
        conn.execute("ROLLBACK")
        raise


def batalkan_transaksi(conn, tid: int, user_id=None) -> None:
    conn.execute("BEGIN")
    try:
        conn.execute("UPDATE transactions SET status='dibatalkan' WHERE id=?", (tid,))
        audit.catat(conn, user_id, "hapus_transaksi", f"id={tid}")
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _aturan(conn):
    from app.db import ambil_aturan
    return ambil_aturan(conn)
