"""Akun pengguna: hash password (bcrypt) dan pembatasan percobaan login."""
import time
import bcrypt
from app.config import MAKS_GAGAL, DURASI_KUNCI
from app import audit


def hash_password(p: str) -> str:
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()


def ada_user(conn) -> bool:
    return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0


def buat_user(conn, nama, username, password, peran):
    nama, username = nama.strip(), username.strip().lower()
    if not nama or not username:
        return "Nama dan username harus diisi"
    if len(password) < 8:
        return "Password minimal 8 karakter"
    if conn.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
        return "Username sudah dipakai"
    conn.execute("INSERT INTO users(nama,username,password_hash,peran) VALUES(?,?,?,?)",
                 (nama, username, hash_password(password), peran))
    return None


def cek_login(conn, username, password, state: dict):
    """Kembalikan (user_row, pesan). state = dict penyimpan jumlah gagal (mis. st.session_state)."""
    sekarang = time.time()
    if state.get("kunci_sampai", 0) > sekarang:
        return None, f"Terlalu banyak salah. Coba lagi dalam {int(state['kunci_sampai'] - sekarang)} detik."
    u = conn.execute("SELECT * FROM users WHERE username=? AND aktif=1", (username.strip().lower(),)).fetchone()
    if u and bcrypt.checkpw(password.encode(), u["password_hash"].encode()):
        state["gagal"] = 0
        audit.catat(conn, u["id"], "login")
        return u, None
    state["gagal"] = state.get("gagal", 0) + 1
    if state["gagal"] >= MAKS_GAGAL:
        state["gagal"], state["kunci_sampai"] = 0, sekarang + DURASI_KUNCI
        return None, "Terlalu banyak salah. Login dikunci 1 menit."
    return None, f"Username atau password salah (sisa percobaan: {MAKS_GAGAL - state['gagal']})."
