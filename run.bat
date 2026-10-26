@echo off
chcp 65001 >nul
echo ============================================================
echo   RAG Security Lab - Khoi dong Ung dung Chatbot & Security Lab
echo   Nhom A10 - VKU - De tai Data Poisoning tren RAG
echo ============================================================
echo.

if not exist ".venv\Scripts\streamlit.exe" (
    echo [THONG BAO] Chua cai dat moi truong virtual environment.
    echo Dang tu dong chay setup.bat de cai dat...
    call setup.bat
    exit /b
)

echo Dang khoi chay Streamlit Web UI...
echo Ung dung se mo tai trinh duyet: http://localhost:8501
echo Nhan Ctrl+C tai cua so nay de tat ung dung.
echo.

.\.venv\Scripts\streamlit.exe run web.py
pause
