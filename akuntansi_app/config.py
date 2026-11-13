"""Konfigurasi aplikasi dan saklar fitur."""
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

def _boolean(nama: str, default: bool) -> bool:
    """Membaca variabel lingkungan boolean."""
    nilai = os.getenv(nama)
    return default if nilai is None else nilai.strip().lower() in {"1", "true", "yes", "ya", "on"}

APP_NAME = os.getenv("APP_NAME", "Rumah Tumbuh").strip() or "Rumah Tumbuh"
APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
if APP_ENV not in {"development", "production"}:
    raise ValueError("APP_ENV harus development atau production.")
OTP_ENABLED = _boolean("OTP_ENABLED", True)
OTP_ON_LOGIN = _boolean("OTP_ON_LOGIN", False)
REMEMBER_ME_ENABLED = _boolean("REMEMBER_ME_ENABLED", True)
OTP_DEV_MODE = _boolean("OTP_DEV_MODE", False)
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY wajib diisi di file .env.")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1").strip()
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "akuntansi_app").strip()
DB_USER = os.getenv("DB_USER", "root").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
if not re.fullmatch(r"[A-Za-z0-9_]+", DB_NAME):
    raise ValueError("DB_NAME hanya boleh berisi huruf, angka, dan garis bawah.")
if not 1 <= DB_PORT <= 65535:
    raise ValueError("DB_PORT harus di antara 1 dan 65535.")
if APP_ENV == "production":
    OTP_DEV_MODE = False
    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD wajib diisi pada lingkungan production.")
