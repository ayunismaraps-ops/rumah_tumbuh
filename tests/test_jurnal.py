"""Unit test aturan jurnal sesuai ketentuan. Jalankan: pytest"""
import pytest
from app import db, services
from app.journal_engine import bangun_jurnal
from app.validators import validasi


@pytest.fixture
def conn(tmp_path):
    p = tmp_path / "t.db"
    db.init_db(p)
    c = db.get_conn(p)
    yield c
    c.close()


@pytest.fixture
def aturan(conn):
    return db.ambil_aturan(conn)


def pasang(jurnal):
    """Ringkas: [(debit_kode, kredit_kode, nilai), ...] per jurnal."""
    hasil = []
    for j in jurnal:
        d = next(b for b in j["baris"] if b["debit"])
        k = next(b for b in j["baris"] if b["kredit"])
        hasil.append((d["kode"], k["kode"], d["debit"]))
    return hasil


def ctx(**kw):
    return {"metode": "Tunai", "tujuan": None, "aset": None, "barang": None, **kw}


def test_beli_pupuk_tunai(aturan):
    j = bangun_jurnal(aturan["Beli Pupuk"], ctx(metode="Tunai"), 3_000_000)
    assert pasang(j) == [("1142", "1110", 3_000_000)]


def test_beli_pupuk_utang(aturan):
    j = bangun_jurnal(aturan["Beli Pupuk"], ctx(metode="Utang"), 3_000_000)
    assert pasang(j) == [("1142", "2110", 3_000_000)]


def test_jual_kebun_tunai_tanpa_hpp(aturan):
    j = bangun_jurnal(aturan["Jual Hasil Kebun"], ctx(), 5_000_000)
    assert pasang(j) == [("1110", "4110", 5_000_000)]


def test_jual_pengepulan_transfer_dengan_hpp(aturan):
    j = bangun_jurnal(aturan["Jual Hasil Pengepulan"], ctx(metode="Transfer Bank"), 4_000_000, hpp=3_200_000)
    assert pasang(j) == [("1120", "4120", 4_000_000), ("5120", "1141", 3_200_000)]


def test_upah_utang_kapitalisasi(aturan):
    j = bangun_jurnal(aturan["Bayar Upah/Gaji"], ctx(metode="Utang", tujuan="Tanaman Belum Menghasilkan"), 500_000)
    assert pasang(j) == [("1240", "2120", 500_000)]


def test_pakai_pupuk_operasional(aturan):
    j = bangun_jurnal(aturan["Pakai Pupuk"], ctx(metode="-", tujuan="Operasional"), 200_000)
    assert pasang(j) == [("6120", "1142", 200_000)]


def test_penyusutan_peralatan(aturan):
    j = bangun_jurnal(aturan["Penyusutan"], ctx(metode="-", aset="Peralatan"), 250_000)
    assert pasang(j) == [("6140", "1261", 250_000)]


def base(**kw):
    return {"tanggal": "2026-11-07", "jenis_transaksi": "Jual Hasil Kebun", "metode": "Tunai",
            "keterangan": "tes", "nominal": 1000, **kw}


def test_validasi_jual_kebun_utang_ditolak(aturan):
    assert validasi(base(metode="Utang"), aturan)


def test_validasi_setoran_modal_nol(aturan):
    err = validasi(base(jenis_transaksi="Setoran Modal", nominal=0), aturan)
    assert "Nominal harus lebih dari 0" in err


def test_simpan_dan_hpp_rata_rata(conn):
    """Beli 10 kg @320rb lalu jual 10 kg Rp 4 jt -> HPP Rp 3,2 jt, stok habis."""
    services.simpan_transaksi(conn, base(jenis_transaksi="Beli Hasil Pengepulan", nominal=3_200_000, jumlah=10))
    tid = services.simpan_transaksi(conn, base(jenis_transaksi="Jual Hasil Pengepulan", nominal=4_000_000,
                                               jumlah=10, metode="Transfer Bank"))
    from app import ledger, inventory
    kode = [(r["kode_akun"], r["debit"], r["kredit"]) for r in ledger.baris_jurnal(conn, tid)]
    assert ("5120", 3_200_000, 0) in kode and ("1141", 0, 3_200_000) in kode
    assert inventory.stok_dan_nilai(conn, "Hasil Pengepulan") == (0.0, 0)


def test_stok_kurang_butuh_konfirmasi(conn):
    with pytest.raises(services.StokKurang):
        services.simpan_transaksi(conn, base(jenis_transaksi="Jual Hasil Pengepulan", jumlah=5))
    assert services.simpan_transaksi(conn, base(jenis_transaksi="Jual Hasil Pengepulan", jumlah=5),
                                     konfirmasi_stok=True)


def test_edit_dan_batal(conn):
    from app import ledger
    t1 = services.simpan_transaksi(conn, base(nominal=1000))
    t2 = services.simpan_transaksi(conn, base(nominal=2000), ganti_id=t1)
    assert ledger.ambil_transaksi(conn, t1)["status"] == "dibatalkan"
    assert ledger.saldo_akun(conn, "1110") == 2000
    services.batalkan_transaksi(conn, t2)
    assert ledger.saldo_akun(conn, "1110") == 0
