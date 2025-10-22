#!/bin/bash
# YouTube Downloader - Mojave (10.14) Compatible Installer
# For macOS 10.14 (Mojave) through macOS 10.15 (Catalina) on Intel Macs

echo "=========================================="
echo "YouTube Downloader - Mojave Installer"
echo "macOS 10.14+ Intel Compatible"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check macOS version
MACOS_VERSION=$(sw_vers -productVersion)
echo "Detected macOS: $MACOS_VERSION"

# Check if running on Mojave/Catalina
if [[ "$MACOS_VERSION" == 10.14.* ]] || [[ "$MACOS_VERSION" == 10.15.* ]]; then
    echo "✓ Mojave/Catalina detected - using compatible setup"
    MOJAVE_MODE=true
else
    echo "ℹ️  Newer macOS detected - this installer works but you may use the standard installer"
    MOJAVE_MODE=false
fi

echo ""

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python 3 found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python 3.7-3.9 for Mojave compatibility:"
    echo ""
    echo "Option 1 - Using Homebrew (recommended):"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "  brew install python@3.9"
    echo ""
    echo "Option 2 - From python.org:"
    echo "  Download Python 3.9.x from https://www.python.org/downloads/mac-osx/"
    exit 1
fi

# Check Python version compatibility
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 7 ] && [ "$PYTHON_MINOR" -le 11 ]; then
    echo "✓ Python version compatible"
else
    echo "⚠️  Warning: Python $PYTHON_MAJOR.$PYTHON_MINOR detected"
    echo "   For best Mojave compatibility, use Python 3.7-3.9"
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Installing dependencies..."
echo ""

# For Mojave, we need specific package versions
if [ "$MOJAVE_MODE" = true ]; then
    echo "Installing Mojave-compatible packages..."

    # Install PyQt5 (will auto-select compatible version for system)
    pip3 install --user "PyQt5>=5.12,<5.16" || {
        echo "❌ Failed to install PyQt5"
        exit 1
    }

    # Install yt-dlp (latest version still supports older Python)
    pip3 install --user yt-dlp || {
        echo "❌ Failed to install yt-dlp"
        exit 1
    }
else
    # Modern macOS
    pip3 install --user PyQt5 yt-dlp || {
        echo "❌ Failed to install dependencies"
        exit 1
    }
fi

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "To launch YouTube Downloader:"
echo "  python3 \"$SCRIPT_DIR/YouTube-Downloader.py\""
echo ""
echo "Or create a desktop shortcut:"
echo "  ln -s \"$SCRIPT_DIR/YouTube-Downloader.py\" ~/Desktop/YouTube-Downloader.command"
echo "  chmod +x ~/Desktop/YouTube-Downloader.command"
echo ""

read -p "Launch YouTube Downloader now? (Y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    python3 "$SCRIPT_DIR/YouTube-Downloader.py" &
    echo "✓ YouTube Downloader launched!"
fi
