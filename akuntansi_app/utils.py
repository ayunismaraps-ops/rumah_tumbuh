"""Validasi, hash kata sandi, waktu, dan format tampilan."""
import re
from datetime import datetime, timezone
import bcrypt

def utc_now() -> datetime:
    """Menghasilkan waktu UTC naive untuk disimpan di MySQL."""
    return datetime.now(timezone.utc).replace(tzinfo=None)

def hash_password(password: str) -> str:
    """Menghasilkan hash bcrypt dengan batas 72 byte."""
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Kata sandi tidak boleh lebih dari 72 byte UTF-8.")
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verifikasi_password(password: str, password_hash: str) -> bool:
    """Memeriksa kata sandi terhadap hash bcrypt."""
    if len(password.encode("utf-8")) > 72:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False

def normalisasi_email(email: str) -> str:
    """Menghapus spasi tepi dan mengubah email menjadi huruf kecil."""
    return email.strip().lower()

def validasi_email(email: str) -> bool:
    """Memeriksa format dasar alamat email."""
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", normalisasi_email(email)))

def format_rupiah(nilai: int | float) -> str:
    """Memformat nilai ke Rupiah."""
    return f"Rp {nilai:,.0f}".replace(",", ".")

def format_tanggal(tanggal: datetime) -> str:
    """Memformat tanggal."""
    return tanggal.strftime("%d-%m-%Y")

def mask_email(email: str) -> str:
    """Menyamarkan bagian lokal alamat email."""
    email = normalisasi_email(email)
    if "@" not in email:
        return email
    lokal, domain = email.split("@", 1)
    return f"{lokal[:1]}****@{domain}"
