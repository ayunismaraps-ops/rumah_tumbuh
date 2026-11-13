"""Akses data pengguna pada tabel MySQL."""
from typing import Any
from database import koneksi
from utils import utc_now

def ambil_user_berdasarkan_email(email: str) -> dict[str, Any] | None:
    """Mengambil pengguna berdasarkan email."""
    with koneksi() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email=%s LIMIT 1", (email.strip().lower(),))
            return cur.fetchone()

def ambil_user_berdasarkan_username(username: str) -> dict[str, Any] | None:
    """Mengambil pengguna berdasarkan username."""
    with koneksi() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username=%s LIMIT 1", (username.strip().lower(),))
            return cur.fetchone()

def buat_user(nama: str, email: str, username: str, password_hash: str, *, is_verified: bool = False) -> int:
    """Menyimpan pengguna dan mengembalikan ID-nya."""
    with koneksi() as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO users
                (nama,email,username,password_hash,is_verified,created_at)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (nama.strip(), email.strip().lower(), username.strip().lower(),
                 password_hash, int(is_verified), utc_now()))
            return int(cur.lastrowid)

def hitung_user() -> int:
    """Menghitung jumlah pengguna."""
    with koneksi() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS jumlah FROM users")
            return int(cur.fetchone()["jumlah"])
