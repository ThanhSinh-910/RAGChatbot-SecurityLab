@echo off
chcp 65001 >nul
echo ============================================================
echo   RAG Security Lab - Nhom A10 VKU - Setup Script
echo   Do an: Data Poisoning tren RAG + Giam sat an toan
echo ============================================================
echo.

:: Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [LOI] Chua cai Python! Tai tai: https://www.python.org/downloads/
    echo       Nho tich "Add Python to PATH" khi cai dat.
    pause
    exit /b 1
)
echo [OK] Python da san sang.

:: Tao virtual environment neu chua co
if not exist ".venv" (
    echo.
    echo [SETUP] Tao virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [LOI] Khong the tao virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment da duoc tao tai .venv\
) else (
    echo [OK] Virtual environment da ton tai.
)

:: Kich hoat venv va cai thu vien
echo.
echo [SETUP] Cai dat cac thu vien can thiet (co the mat 2-5 phut lan dau)...
call .venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [LOI] Cai dat thu vien that bai. Kiem tra ket noi mang.
    pause
    exit /b 1
)
echo [OK] Tat ca thu vien da duoc cai dat.

:: Kiem tra file .env
echo.
if not exist ".env" (
    echo [CANH BAO] Chua co file .env !
    echo.
    echo Huong dan tao file .env:
    echo   1. Mo file .env.example trong thu muc nay
    echo   2. Sao chep thanh file moi ten ".env"
    echo   3. Lay API key tai: https://aistudio.google.com/api-keys
    echo   4. Thay "your_google_api_key_here" bang key that cua ban
    echo.
    echo Ban co muon mo file .env.example de xem huong dan khong? [Y/N]
    set /p choice=
    if /i "%choice%"=="Y" notepad .env.example
    echo.
    echo Sau khi tao file .env, chay lai setup.bat hoac chay lenh:
    echo   .venv\Scripts\streamlit.exe run web.py
    echo.
) else (
    echo [OK] File .env da ton tai.
    echo.
    echo Dang khoi dong ung dung Streamlit...
    echo Truy cap: http://localhost:8501
    echo Nhan Ctrl+C de dung.
    echo.
    .venv\Scripts\streamlit.exe run web.py
)

pause
