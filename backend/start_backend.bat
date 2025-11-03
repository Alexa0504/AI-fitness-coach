@echo off
title Starting Flask Backend
cd /d %~dp0

echo =====================================================
echo    AI Fitness Coach - Flask Backend Starter
echo =====================================================
echo.

REM Create venv if it doesn’t exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Force upgrade of pip, setuptools, and wheel first
echo Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found. Installing basic dependencies...
    pip install flask flask_sqlalchemy python-dotenv
)

echo.
echo Starting Flask server...
echo =====================================================
python run.py

pause
