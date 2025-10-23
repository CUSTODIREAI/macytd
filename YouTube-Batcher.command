#!/bin/bash
# YouTube Batcher - Double-clickable launcher
# Works on macOS 10.14 (Mojave) and later

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 Required" message "Please install Python 3 to run The Batcher.\n\nInstall via:\nbrew install python3" as critical'
    exit 1
fi

# Check if PyQt5 is installed
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo "Installing dependencies (first time only)..."
    echo "This may take a few minutes..."
    pip3 install --user PyQt5 yt-dlp

    if [ $? -ne 0 ]; then
        osascript -e 'display alert "Installation Failed" message "Failed to install dependencies. Please run:\npip3 install PyQt5 yt-dlp" as critical'
        exit 1
    fi
fi

# Check if yt-dlp is installed
if ! python3 -c "import yt_dlp" 2>/dev/null; then
    pip3 install --user yt-dlp
fi

# Clear the terminal
clear

echo "================================================"
echo "  YouTube Batch Downloader - The Batcher"
echo "================================================"
echo ""
echo "Starting application..."
echo ""

# Launch the application
cd "$SCRIPT_DIR"
python3 "$SCRIPT_DIR/YouTube-Batcher.py"

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "================================================"
    echo "Application exited with an error"
    echo "================================================"
    echo ""
    read -p "Press Enter to close..."
fi
