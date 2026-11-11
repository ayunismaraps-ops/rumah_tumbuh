"""Pengaturan umum aplikasi Rumah Tumbuh."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "rumah_tumbuh.db"

MAKS_GAGAL = 5          # percobaan login gagal sebelum dikunci
DURASI_KUNCI = 60       # detik
BARIS_PER_HALAMAN = 20

# Pembayaran -> kode akun (placeholder {PEMBAYARAN})
AKUN_METODE = {"Tunai": "1110", "Transfer Bank": "1120", "Piutang": "1130", "Utang": "2110"}
# Aset yang disusutkan -> akun akumulasi penyusutan (placeholder {ASET})
AKUN_ASET = {"Gudang": "1221", "Gubuk Kebun": "1231",
             "Tanaman Menghasilkan": "1251", "Peralatan": "1261"}
# Barang persediaan -> akun persediaan (placeholder {BARANG})
AKUN_BARANG = {"Hasil Pengepulan": "1141", "Pupuk": "1142",
               "Pestisida": "1143", "Bibit": "1144"}
PILIHAN_TUJUAN = ["Operasional", "Tanaman Belum Menghasilkan"]
AKUN_TBM = "1240"       # Tanaman Belum Menghasilkan (dikapitalisasi)
BARANG_PENGEPULAN = "Hasil Pengepulan"
