"""Koneksi SQLite, pembuatan tabel, dan data awal (COA + aturan jurnal)."""
import csv
import sqlite3
from app.config import DB_PATH, DATA_DIR

SKEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT NOT NULL,
  username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL,
  peran TEXT NOT NULL CHECK(peran IN ('Pemilik','Pencatat')),
  aktif INTEGER NOT NULL DEFAULT 1, dibuat_pada TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS accounts(
  kode TEXT PRIMARY KEY, nama TEXT NOT NULL,
  pos_saldo TEXT NOT NULL CHECK(pos_saldo IN ('Db','Kr')),
  pos_laporan TEXT NOT NULL CHECK(pos_laporan IN ('NRC','LR')),
  aktif INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS rules(
  id INTEGER PRIMARY KEY AUTOINCREMENT, jenis_transaksi TEXT NOT NULL UNIQUE, menu TEXT NOT NULL,
  pembayaran_valid TEXT NOT NULL, akun_debit TEXT NOT NULL, akun_kredit TEXT NOT NULL,
  butuh_tujuan INTEGER DEFAULT 0, butuh_aset INTEGER DEFAULT 0, butuh_barang INTEGER DEFAULT 0,
  catatan TEXT);
CREATE TABLE IF NOT EXISTS transactions(
  id INTEGER PRIMARY KEY AUTOINCREMENT, tanggal TEXT NOT NULL, jenis_transaksi TEXT NOT NULL,
  metode_bayar TEXT NOT NULL, keterangan TEXT NOT NULL, jumlah REAL, satuan TEXT,
  harga_satuan INTEGER, nominal INTEGER NOT NULL CHECK(nominal > 0),
  pihak TEXT, no_invoice TEXT, blok_lahan TEXT, catatan TEXT,
  tujuan TEXT, aset TEXT, barang TEXT,           -- pilihan tambahan (dipakai saat Edit)
  dibuat_oleh INTEGER, dibuat_pada TEXT DEFAULT CURRENT_TIMESTAMP,
  status TEXT NOT NULL DEFAULT 'aktif' CHECK(status IN ('aktif','dibatalkan')));
CREATE TABLE IF NOT EXISTS journals(
  id INTEGER PRIMARY KEY AUTOINCREMENT, no_jurnal TEXT NOT NULL UNIQUE,
  transaction_id INTEGER NOT NULL REFERENCES transactions(id),
  tanggal TEXT NOT NULL, keterangan TEXT, jenis TEXT NOT NULL CHECK(jenis IN ('utama','hpp')));
CREATE TABLE IF NOT EXISTS journal_lines(
  id INTEGER PRIMARY KEY AUTOINCREMENT, journal_id INTEGER NOT NULL REFERENCES journals(id),
  kode_akun TEXT NOT NULL REFERENCES accounts(kode),
  debit INTEGER NOT NULL DEFAULT 0, kredit INTEGER NOT NULL DEFAULT 0,
  CHECK(debit >= 0 AND kredit >= 0 AND NOT (debit > 0 AND kredit > 0)));
CREATE TABLE IF NOT EXISTS stock_movements(
  id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id INTEGER NOT NULL REFERENCES transactions(id),
  barang TEXT NOT NULL, tanggal TEXT NOT NULL, qty REAL NOT NULL, nilai INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS audit_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT, waktu TEXT DEFAULT CURRENT_TIMESTAMP,
  user_id INTEGER, aksi TEXT NOT NULL, detail TEXT);
"""


def get_conn(path=DB_PATH) -> sqlite3.Connection:
    # isolation_level=None -> kita atur BEGIN/COMMIT sendiri (atomik)
    conn = sqlite3.connect(str(path), isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _baca_csv(nama):
    with open(DATA_DIR / nama, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def init_db(path=DB_PATH) -> None:
    conn = get_conn(path)
    conn.executescript(SKEMA)
    if conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0] == 0:
        for r in _baca_csv("seed_coa.csv"):
            conn.execute("INSERT INTO accounts(kode,nama,pos_saldo,pos_laporan) VALUES(?,?,?,?)",
                         (r["kode"], r["nama"], r["pos_saldo"], r["pos_laporan"]))
    if conn.execute("SELECT COUNT(*) FROM rules").fetchone()[0] == 0:
        for r in _baca_csv("seed_rules.csv"):
            conn.execute("""INSERT INTO rules(jenis_transaksi,menu,pembayaran_valid,akun_debit,
                akun_kredit,butuh_tujuan,butuh_aset,butuh_barang,catatan) VALUES(?,?,?,?,?,?,?,?,?)""",
                         (r["jenis_transaksi"], r["menu"], r["pembayaran_valid"], r["akun_debit"],
                          r["akun_kredit"], int(r["butuh_tujuan"]), int(r["butuh_aset"]),
                          int(r["butuh_barang"]), r["catatan"]))
    conn.close()


def ambil_aturan(conn) -> dict:
    """Semua aturan jurnal: {jenis_transaksi: dict}."""
    return {r["jenis_transaksi"]: dict(r) for r in conn.execute("SELECT * FROM rules ORDER BY id")}
