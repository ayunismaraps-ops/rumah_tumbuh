"""Persediaan hasil pengepulan dengan harga rata-rata bergerak."""


def stok_dan_nilai(conn, barang: str):
    """(total qty, total nilai) dari transaksi yang masih aktif."""
    r = conn.execute("""SELECT COALESCE(SUM(s.qty),0), COALESCE(SUM(s.nilai),0)
        FROM stock_movements s JOIN transactions t ON t.id = s.transaction_id
        WHERE t.status='aktif' AND s.barang=?""", (barang,)).fetchone()
    return float(r[0]), int(r[1])


def hitung_hpp(conn, barang: str, qty_jual: float) -> int:
    """HPP = jumlah terjual x harga rata-rata persediaan saat ini."""
    qty, nilai = stok_dan_nilai(conn, barang)
    if qty <= 0:
        return 0
    return round(qty_jual * nilai / qty)
