@echo off
rem Klik dua kali file ini untuk menjalankan aplikasi Rumah Tumbuh
cd /d "%~dp0"
if exist venv\Scripts\activate.bat goto aktifkan
echo Pertama kali: menyiapkan lingkungan, mohon tunggu...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
goto jalan
:aktifkan
call venv\Scripts\activate.bat
:jalan
start "" http://localhost:8501
streamlit run main.py
pause
