# Rumah Tumbuh — Aplikasi Desktop

Rumah Tumbuh dibuka sebagai jendela aplikasi desktop tersendiri. Tampilan memakai HTML dan CSS asli agar konsisten dengan desain versi web; Flask dan seluruh logika akuntansi berjalan dengan Python di komputer lokal. Halaman ditampilkan di dalam Qt WebEngine, jadi pengguna tidak perlu membuka browser secara terpisah.

## Menjalankan di Windows

1. Ekstrak seluruh ZIP ke satu folder.
2. Pastikan Python terpasang dan internet tersedia saat pertama kali dijalankan.
3. Klik dua kali `jalankan_windows.cmd`.
4. Buat akun pada halaman login jika belum punya akun.

Launcher membuat lingkungan Python lokal dan memasang Flask, PySide6 Qt WebEngine, serta ReportLab secara otomatis. Jendela aplikasi berjalan sendiri, tanpa address bar atau tab browser. Data tetap disimpan lokal di `db/rumah_tumbuh.db`.

## Mengedit tampilan

- `rumah_tumbuh/templates/`: halaman HTML.
- `rumah_tumbuh/static/css/`: desain dan tata letak.
- `rumah_tumbuh/static/js/`: interaksi halaman.
- `main.pyw`: jendela desktop tertanam.
- `rumah_tumbuh/app.py` dan `rumah_tumbuh/pages/`: aplikasi web lokal dan rute halaman.
- `rumah_tumbuh/accounting/`: logika transaksi, jurnal, buku besar, persediaan, penyesuaian, laporan, dan penutup periode.
- `db/migrations/`: struktur serta pembaruan database.

Penjualan yang dicatat melalui form transaksi tetap diposting satu kali ke jurnal dan buku besar, dibuatkan invoice, dan memperbarui stok sesuai alur akuntansi.
