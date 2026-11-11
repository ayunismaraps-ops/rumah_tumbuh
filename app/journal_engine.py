"""Mesin jurnal: mengubah pilihan pengguna menjadi debit/kredit otomatis.
Murni logika (tanpa database) supaya mudah diuji."""
from app.config import AKUN_METODE, AKUN_ASET, AKUN_BARANG, AKUN_TBM


def _akun(token: str, ctx: dict) -> str:
    """Ubah token aturan jadi kode akun. Contoh: '1142', '{PEMBAYARAN}', '{TUJUAN:6110}'."""
    if not token.startswith("{"):
        return token
    nama, _, param = token.strip("{}").partition(":")
    if nama == "PEMBAYARAN":
        if ctx["metode"] == "Utang" and param:      # mis. utang upah -> 2120
            return param
        return AKUN_METODE[ctx["metode"]]
    if nama == "TUJUAN":                            # Operasional -> beban, selain itu dikapitalisasi
        return param if ctx["tujuan"] == "Operasional" else AKUN_TBM
    if nama == "ASET":
        return AKUN_ASET[ctx["aset"]]
    if nama == "BARANG":
        return AKUN_BARANG[ctx["barang"]]
    raise ValueError(f"Placeholder tidak dikenal: {token}")


def _cek_seimbang(baris: list) -> None:
    for b in baris:
        if b["debit"] and b["kredit"]:
            raise ValueError("Satu baris tidak boleh berisi debit dan kredit sekaligus")
    if sum(b["debit"] for b in baris) != sum(b["kredit"] for b in baris):
        raise ValueError("Jurnal tidak seimbang (debit harus sama dengan kredit)")


def bangun_jurnal(aturan: dict, ctx: dict, nominal: int, hpp: int = 0) -> list:
    """Kembalikan daftar jurnal: [{'jenis': 'utama'|'hpp', 'baris': [{kode, debit, kredit}]}].
    ctx berisi: metode, tujuan, aset, barang."""
    nominal = int(nominal)
    utama = [{"kode": _akun(aturan["akun_debit"], ctx), "debit": nominal, "kredit": 0},
             {"kode": _akun(aturan["akun_kredit"], ctx), "debit": 0, "kredit": nominal}]
    _cek_seimbang(utama)
    hasil = [{"jenis": "utama", "baris": utama}]

    # Khusus jual hasil pengepulan: tambah jurnal HPP otomatis
    if aturan["jenis_transaksi"] == "Jual Hasil Pengepulan" and hpp > 0:
        j = [{"kode": "5120", "debit": int(hpp), "kredit": 0},
             {"kode": "1141", "debit": 0, "kredit": int(hpp)}]
        _cek_seimbang(j)
        hasil.append({"jenis": "hpp", "baris": j})
    return hasil
