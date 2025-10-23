@echo off
REM YouTube Batcher Launcher for Windows
REM Compatible with Windows 10/11

echo ========================================
echo YouTube Batch Downloader - The Batcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed!
    echo.
    echo Please install Python 3.7 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Check if PyQt5 is installed
python -c "import PyQt5" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [SETUP] Installing dependencies (first time only)...
    echo This may take a few minutes...
    echo.
    pip install PyQt5 yt-dlp
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [OK] Dependencies installed

REM Check if yt-dlp is installed
python -c "import yt_dlp" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [SETUP] Installing yt-dlp...
    pip install yt-dlp
)

echo.
echo [LAUNCH] Starting YouTube Batcher...
echo.

REM Launch the application
python "%~dp0YouTube-Batcher-Windows.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed to start
    pause
)
