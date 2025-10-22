# YouTube ULTIMATE Downloader 2025 - macOS Edition

Professional YouTube downloader with October 2025 bypass fix built-in.

## Features

- Bypasses YouTube October 2025 403 restrictions
- Auto-updates yt-dlp to latest version
- Professional GUI interface
- Real-time progress tracking
- Download archive (skips duplicates)
- Multiple quality options (up to 1080p)
- Firefox cookie integration

## System Requirements

- macOS 10.14 (Mojave) or later
- Python 3.7 or later
- 100MB free disk space

## Installation

### Option 1: Download DMG (Recommended)
1. Download the latest DMG from releases
2. Open the DMG file
3. Drag "YouTube Downloader" to Applications folder
4. Launch from Applications

### Option 2: Run from Source
```bash
# Install dependencies
pip3 install PyQt5 yt-dlp

# Run the application
python3 YouTube-Downloader.py
```

## Usage

1. Launch the application
2. Click "🔄 Check & Update yt-dlp" to ensure latest version
3. Enter a YouTube URL (channel, playlist, or video)
4. Select output directory (default: ~/Downloads/youtube)
5. Choose quality (1080p recommended)
6. Click "▶️ Start Download"

## Technical Details

**Built-in Fix:**
- Uses `player_js_version=actual` with web_safari client
- Forces IPv4 connections
- Sleep intervals to prevent IP blocking

**Default Settings:**
- Quality: Best up to 1080p
- Output: ~/Downloads/youtube
- Archive: Enabled (skip duplicates)
- Max Downloads: 500 (configurable)

## Building from Source

```bash
# Install py2app
pip3 install py2app

# Build the app
python3 setup.py py2app

# The app will be in: dist/YouTube Downloader.app
```

## Creating DMG

```bash
# After building the app
./create-dmg.sh
```

## Troubleshooting

**Issue:** "ModuleNotFoundError: No module named 'PyQt5'"
**Fix:** `pip3 install PyQt5`

**Issue:** "command not found: yt-dlp"
**Fix:** `pip3 install yt-dlp`

**Issue:** Downloads fail with 403 errors
**Fix:** Click "Check & Update yt-dlp" button in the GUI

## License

For personal use only.

## Support

For issues and questions, please open an issue on GitHub.
