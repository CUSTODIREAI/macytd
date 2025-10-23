# YouTube Batcher - Windows PowerShell Installer
# Run this to install dependencies

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "YouTube Batcher - Windows Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[CHECK] Checking Python installation..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.7+ from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""
Write-Host "[INSTALL] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Write-Host ""

# Install PyQt5
Write-Host "Installing PyQt5..." -ForegroundColor Yellow
pip install PyQt5

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install PyQt5" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[OK] PyQt5 installed" -ForegroundColor Green

# Install yt-dlp
Write-Host "Installing yt-dlp..." -ForegroundColor Yellow
pip install yt-dlp

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install yt-dlp" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[OK] yt-dlp installed" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[SUCCESS] Installation complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To launch YouTube Batcher:" -ForegroundColor Yellow
Write-Host "  1. Double-click: launch-batcher.bat" -ForegroundColor White
Write-Host "  2. Or run: python YouTube-Batcher-Windows.py" -ForegroundColor White
Write-Host ""

$launch = Read-Host "Launch YouTube Batcher now? (Y/n)"

if ($launch -ne 'n' -and $launch -ne 'N') {
    Write-Host ""
    Write-Host "[LAUNCH] Starting YouTube Batcher..." -ForegroundColor Green
    python "$PSScriptRoot\YouTube-Batcher-Windows.py"
}
