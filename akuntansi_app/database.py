"""Koneksi MySQL dan inisialisasi tabel pengguna."""
from contextlib import contextmanager
from typing import Iterator
import pymysql
from pymysql.cursors import DictCursor
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

@contextmanager
def koneksi(*, tanpa_database: bool = False) -> Iterator[pymysql.Connection]:
    """Membuka koneksi dan mengelola commit, rollback, serta penutupan."""
    opsi = dict(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
                charset="utf8mb4", cursorclass=DictCursor, autocommit=False,
                connect_timeout=10, read_timeout=15, write_timeout=15)
    if not tanpa_database:
        opsi["database"] = DB_NAME
    conn = pymysql.connect(**opsi)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def inisialisasi_database() -> None:
    """Membuat database dan tabel users jika belum tersedia."""
    with koneksi(tanpa_database=True) as conn:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    with koneksi() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    nama VARCHAR(120) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    username VARCHAR(20) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    is_verified TINYINT(1) NOT NULL DEFAULT 0,
                    failed_attempts SMALLINT UNSIGNED NOT NULL DEFAULT 0,
                    locked_until DATETIME NULL,
                    created_at DATETIME NOT NULL,
                    PRIMARY KEY (id),
                    UNIQUE KEY uq_users_email (email),
                    UNIQUE KEY uq_users_username (username),
                    KEY idx_users_email (email),
                    KEY idx_users_username (username)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
