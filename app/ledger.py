"""Pertanyaan ke database: saldo, ringkasan bulanan, daftar transaksi, jurnal."""


def saldo_akun(conn, kode: str) -> int:
    r = conn.execute("""SELECT COALESCE(SUM(l.debit),0) d, COALESCE(SUM(l.kredit),0) k, a.pos_saldo p
        FROM accounts a LEFT JOIN journal_lines l ON l.kode_akun=a.kode
        AND l.journal_id IN (SELECT j.id FROM journals j JOIN transactions t ON t.id=j.transaction_id
                             WHERE t.status='aktif')
        WHERE a.kode=?""", (kode,)).fetchone()
    return int(r["d"] - r["k"]) if r["p"] == "Db" else int(r["k"] - r["d"])


def total_penjualan_bulan(conn, ym: str) -> int:
    r = conn.execute("""SELECT COALESCE(SUM(l.kredit - l.debit),0) FROM journal_lines l
        JOIN journals j ON j.id=l.journal_id JOIN transactions t ON t.id=j.transaction_id
        WHERE t.status='aktif' AND l.kode_akun IN ('4110','4120') AND substr(j.tanggal,1,7)=?""", (ym,))
    return int(r.fetchone()[0])


def total_pengeluaran_bulan(conn, ym: str) -> int:
    r = conn.execute("""SELECT COALESCE(SUM(t.nominal),0) FROM transactions t
        JOIN rules r ON r.jenis_transaksi=t.jenis_transaksi
        WHERE t.status='aktif' AND r.menu='Pengeluaran' AND substr(t.tanggal,1,7)=?""", (ym,))
    return int(r.fetchone()[0])


def daftar_transaksi(conn, limit: int, offset: int = 0):
    return conn.execute("SELECT * FROM transactions ORDER BY tanggal DESC, id DESC LIMIT ? OFFSET ?",
                        (limit, offset)).fetchall()


def jumlah_transaksi(conn) -> int:
    return conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]


def ambil_transaksi(conn, tid: int):
    return conn.execute("SELECT * FROM transactions WHERE id=?", (tid,)).fetchone()


def baris_jurnal(conn, transaction_id: int):
    """Semua baris jurnal sebuah transaksi (debit dulu, lalu kredit)."""
    return conn.execute("""SELECT j.no_jurnal, j.jenis, l.kode_akun, a.nama, l.debit, l.kredit
        FROM journals j JOIN journal_lines l ON l.journal_id=j.id JOIN accounts a ON a.kode=l.kode_akun
        WHERE j.transaction_id=? ORDER BY j.id, l.id""", (transaction_id,)).fetchall()


def jurnal_umum(conn, ym: str = None):
    sql = """SELECT j.no_jurnal, j.tanggal, j.keterangan, l.kode_akun, a.nama, l.debit, l.kredit, t.status
        FROM journals j JOIN journal_lines l ON l.journal_id=j.id JOIN accounts a ON a.kode=l.kode_akun
        JOIN transactions t ON t.id=j.transaction_id WHERE t.status='aktif'"""
    par = ()
    if ym:
        sql += " AND substr(j.tanggal,1,7)=?"
        par = (ym,)
    return conn.execute(sql + " ORDER BY j.tanggal, j.id, l.id", par).fetchall()
