"""Catatan jejak aktivitas (siapa melakukan apa)."""


def catat(conn, user_id, aksi: str, detail: str = "") -> None:
    conn.execute("INSERT INTO audit_log(user_id,aksi,detail) VALUES(?,?,?)", (user_id, aksi, detail))
