"""Jendela desktop tanpa chrome browser; antarmuka HTML dirender tertanam di Qt WebEngine."""
import os
import secrets
import sys
import threading
import traceback
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from werkzeug.serving import make_server

from rumah_tumbuh import create_app
from rumah_tumbuh.accounting.seed_accounts import seed_accounts
from rumah_tumbuh.config import database_path, load_env
from rumah_tumbuh.db import connect
from rumah_tumbuh.migrations import migrate

ROOT = Path(__file__).resolve().parent


class RumahTumbuhWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle('Rumah Tumbuh — Pembukuan Usaha Kebun')
        self.resize(1360, 900)
        self.setMinimumSize(1050, 700)
        icon_path = ROOT / 'rumah_tumbuh' / 'static' / 'images' / 'rumah-tumbuh-logo.png'
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.view = QWebEngineView(self)
        self.view.setUrl(QUrl(url))
        self.setCentralWidget(self.view)


def main():
    os.chdir(ROOT)
    load_env()
    os.environ.setdefault('DATABASE_URL', 'file:rumah_tumbuh.db')
    db_path = database_path()
    migrate(db_path)
    conn = connect(db_path)
    try:
        seed_accounts(conn)
    finally:
        conn.close()

    web_app = create_app({
        'DATABASE': str(db_path),
        'JWT_SECRET': os.environ.get('JWT_SECRET') or secrets.token_urlsafe(48),
        'PRODUCTION': False,
    })
    server = make_server('127.0.0.1', 0, web_app, threaded=True)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True, name='rumah-tumbuh-web')
    server_thread.start()

    qt = QApplication(sys.argv)
    window = RumahTumbuhWindow(f'http://127.0.0.1:{server.server_port}/login')
    qt.aboutToQuit.connect(server.shutdown)
    window.show()
    try:
        return qt.exec()
    finally:
        server.server_close()


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        log_path = Path(__file__).resolve().parent / 'rumah_tumbuh_startup_error.log'
        log_path.write_text(traceback.format_exc(), encoding='utf-8')
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, 'Rumah Tumbuh tidak dapat dibuka',
                             f'{error}\n\nRincian kesalahan disimpan di:\n{log_path}')
        raise SystemExit(1)
