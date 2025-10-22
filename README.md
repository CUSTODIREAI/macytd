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

- **macOS 10.14 (Mojave) or later**
- **Python 3.7 or later** (3.7-3.9 recommended for Mojave)
- 100MB free disk space
- Intel or Apple Silicon (M1/M2/M3)

## Installation

### For macOS 10.14 Mojave / 10.15 Catalina (Intel Macs)

**Use the Mojave installer script:**

```bash
# 1. Download or clone this repository
git clone https://github.com/CUSTODIREAI/macytd.git
cd macytd

# 2. Run the Mojave installer
bash install-mojave.sh
```

The installer will:
- Detect your macOS version
- Install compatible PyQt5 version (5.12-5.15)
- Install latest yt-dlp
- Launch the application

**Or install manually:**
```bash
# Install Python 3.7-3.9 via Homebrew
brew install python@3.9

# Install dependencies
pip3 install -r requirements-mojave.txt

# Run the application
python3 YouTube-Downloader.py
```

### For macOS 11+ (Big Sur and later) - Apple Silicon & Intel

**Option 1: Download DMG (Recommended for Apple Silicon)**
1. Download `YouTube-Downloader-macOS.dmg` from releases
2. Open the DMG file
3. Copy contents to your Applications folder
4. Run `launch-youtube-downloader.sh`

**Option 2: Auto-installer**
```bash
bash launch-youtube-downloader.sh
```

**Option 3: Manual installation**
```bash
pip3 install PyQt5 yt-dlp
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
- Max Downloads: Unlimited (configurable 0-10,000)

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

## Compatibility

### Tested Versions

| macOS Version | Architecture | Installation Method | Status |
|--------------|--------------|---------------------|--------|
| 10.14 Mojave | Intel x86_64 | `install-mojave.sh` | ✅ Supported |
| 10.15 Catalina | Intel x86_64 | `install-mojave.sh` | ✅ Supported |
| 11 Big Sur | Intel / Apple Silicon | DMG or auto-installer | ✅ Supported |
| 12 Monterey | Intel / Apple Silicon | DMG or auto-installer | ✅ Supported |
| 13 Ventura | Intel / Apple Silicon | DMG or auto-installer | ✅ Supported |
| 14 Sonoma | Intel / Apple Silicon | DMG or auto-installer | ✅ Supported |
| 15+ Sequoia+ | Intel / Apple Silicon | DMG or auto-installer | ✅ Supported |

**Note:** The DMG file is built for Apple Silicon (ARM64) and macOS 11+. Mojave/Catalina users must install from source using the Mojave installer script.

## Troubleshooting

### Mojave/Catalina Specific Issues

**Issue:** "PyQt5 requires macOS 11.0+"
**Fix:** Use the Mojave installer: `bash install-mojave.sh`

**Issue:** Python version too new (3.10+)
**Fix:** Install Python 3.9: `brew install python@3.9`

### General Issues

**Issue:** "ModuleNotFoundError: No module named 'PyQt5'"
**Fix:** `pip3 install PyQt5` (or use `install-mojave.sh` for Mojave)

**Issue:** "command not found: yt-dlp"
**Fix:** `pip3 install yt-dlp`

**Issue:** Downloads fail with 403 errors
**Fix:** Click "Check & Update yt-dlp" button in the GUI

**Issue:** Application won't launch
**Fix:** Run from Terminal to see errors:
```bash
python3 YouTube-Downloader.py
```

## License

For personal use only.

## Support

For issues and questions, please open an issue on GitHub.
