@echo off
setlocal
cd /d "%~dp0"
title Rumah Tumbuh - Aplikasi Desktop
if not exist "requirements.txt" (
  echo File requirements.txt tidak ditemukan. Ekstrak seluruh ZIP terlebih dahulu.
  pause
  exit /b 1
)
where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)
if not exist ".venv\Scripts\python.exe" (
  echo Menyiapkan lingkungan Python...
  %PY% -m venv .venv
  if errorlevel 1 goto gagal
)
echo Memasang komponen aplikasi desktop dan web lokal...
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto gagal
echo Membuka jendela Rumah Tumbuh...
".venv\Scripts\python.exe" main.pyw
if errorlevel 1 goto gagal
exit /b 0
:gagal
echo.
echo Aplikasi belum dapat dijalankan. Periksa Python dan koneksi internet, lalu coba lagi.
pause
exit /b 1
