"""Tes pembuatan database dan insert-baca pengguna."""
import secrets
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from database import inisialisasi_database
from models import ambil_user_berdasarkan_username, buat_user
from utils import hash_password

def main() -> int:
    """Membuat tabel, menyimpan pengguna uji, lalu membaca kembali."""
    print("Menginisialisasi database MySQL...")
    inisialisasi_database()
    username = f"uji_{secrets.token_hex(4)}"
    email = f"{username}@example.test"
    user_id = buat_user("Pengguna Uji", email, username, hash_password("UjiAkun123"), is_verified=True)
    hasil = ambil_user_berdasarkan_username(username)
    if not hasil or hasil["id"] != user_id or hasil["email"] != email:
        print("GAGAL: pengguna uji tidak berhasil dibaca kembali.")
        return 1
    print(f"BERHASIL: database siap; pengguna uji tersimpan dengan ID {user_id}.")
    print("Catatan: pengguna uji tetap tersimpan dan dapat dihapus manual dari tabel users.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
