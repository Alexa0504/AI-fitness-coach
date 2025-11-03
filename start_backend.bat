@echo off
title Starting Flask Backend
cd /d %~dp0

echo =====================================================
echo    AI Fitness Coach - Flask Backend Starter
echo =====================================================

REM Activate venv
call backend\venv\Scripts\activate

REM Upgrade pip, setuptools, and wheel to the latest versions
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies from the backend folder
if exist backend\requirements.txt (
    echo Installing dependencies from backend\requirements.txt...
    pip install -r backend\requirements.txt
) else (
    echo No requirements.txt found. Installing basic dependencies...
    pip install flask flask_sqlalchemy flask_migrate python-dotenv flask-cors bcrypt PyJWT
)

echo.
echo Starting Flask server...
echo =====================================================
python -m backend.run

pause
