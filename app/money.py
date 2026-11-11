"""Format uang (Rp 1.250.000) dan tanggal (07 Nov 2026)."""
from datetime import date, datetime

BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def format_rupiah(n) -> str:
    n = int(n or 0)
    teks = f"{abs(n):,}".replace(",", ".")
    return f"-Rp {teks}" if n < 0 else f"Rp {teks}"


def format_tanggal(t) -> str:
    """Terima 'YYYY-MM-DD' atau objek date -> '07 Nov 2026'."""
    if isinstance(t, str):
        t = datetime.strptime(t, "%Y-%m-%d").date()
    return f"{t.day:02d} {BULAN[t.month - 1]} {t.year}"


def format_qty(q) -> str:
    """12.5 -> '12,5' ; 10.0 -> '10'."""
    q = float(q or 0)
    return (f"{q:.3f}".rstrip("0").rstrip(".")).replace(".", ",")


def ke_tanggal_iso(t) -> str:
    return t.isoformat() if isinstance(t, date) else str(t)
