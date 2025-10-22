#!/bin/bash
# YouTube Downloader Launcher for macOS
# Compatible with macOS 10.14 (Mojave) and later

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 Required" message "Please install Python 3 to run YouTube Downloader.\n\nInstall via:\nbrew install python3" as critical'
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import PyQt5" 2>/dev/null; then
    osascript -e 'display alert "Installing Dependencies" message "First-time setup: Installing required packages...\nThis may take a few minutes." giving up after 3'

    # Open terminal and install dependencies
    osascript <<EOF
tell application "Terminal"
    activate
    do script "echo 'Installing YouTube Downloader dependencies...'; pip3 install PyQt5 yt-dlp && echo '✅ Installation complete! Launching YouTube Downloader...' && sleep 2 && python3 '$SCRIPT_DIR/YouTube-Downloader.py' && exit"
end tell
EOF
    exit 0
fi

if ! python3 -c "import yt_dlp" 2>/dev/null; then
    pip3 install --user yt-dlp
fi

# Launch the application
python3 "$SCRIPT_DIR/YouTube-Downloader.py" &
