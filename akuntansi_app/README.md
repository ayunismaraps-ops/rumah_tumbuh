# Rumah Tumbuh — Fondasi Fase 1

Direktori ini menampung implementasi baru agar aplikasi lama di root repository tidak berubah. Fase 1 mencakup konfigurasi, koneksi MySQL, model pengguna, utilitas, dan tes database. UI autentikasi belum dibuat.

## Windows + Laragon

1. Periksa Python: `where python`, `python --version`, dan `py -0`.
2. Siapkan proyek pada `C:\laragon\www\akuntansi_app` (atau gunakan direktori ini).
3. Jalankan MySQL dari Laragon. Apache/Nginx tidak diperlukan untuk Streamlit.
4. Buka terminal pada direktori `akuntansi_app`, lalu jalankan:

   ```powershell
   py -3.13 -m venv .venv
   .venv\Scripts\activate
   python --version
   pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

5. Pastikan versi Python adalah 3.13.x. Isi `SECRET_KEY` pada `.env` dengan nilai acak panjang. Jangan commit file `.env`.
6. Konfigurasi Laragon bawaan: host `127.0.0.1`, port `3306`, user `root`, password kosong. Sesuaikan jika konfigurasi lokal berbeda.
7. Jalankan tes:

   ```powershell
   python scripts/test_database.py
   ```

   Tes membuat database `akuntansi_app` dan tabel `users`, lalu insert dan membaca kembali satu pengguna uji. Pengguna uji tidak dihapus otomatis.
8. Pada fase berikutnya, entry point dijalankan dengan `streamlit run main.py`.

## Pengguna MySQL khusus

Untuk lingkungan non-lokal, jangan gunakan akun root. Buat akun khusus dan batasi haknya:

```sql
CREATE USER 'rumah_tumbuh'@'localhost' IDENTIFIED BY 'kata_sandi_kuat';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
ON akuntansi_app.* TO 'rumah_tumbuh'@'localhost';
FLUSH PRIVILEGES;
```

## Keamanan

Password pengguna di-hash dengan bcrypt dan tidak disimpan sebagai teks biasa. Jika file `.env` pernah ter-commit, segera revoke/ganti seluruh kredensial di dalamnya dan bersihkan riwayat Git. Rahasia production disimpan pada environment server atau `st.secrets`, bukan repository.

MySQL Laragon hanya untuk lokal. Hosting membutuhkan database online dan SMTP online. Streamlit memerlukan proses Python yang terus berjalan dan WebSocket; gunakan VPS dengan systemd/supervisor, Nginx reverse proxy (WebSocket aktif) dan HTTPS, atau platform PaaS. Shared hosting cPanel biasa tidak otomatis mendukung Streamlit. Samakan versi Python server dengan lokal (3.13).

Untuk OTP production, siapkan SPF, DKIM, dan DMARC agar email tidak mudah masuk spam.
