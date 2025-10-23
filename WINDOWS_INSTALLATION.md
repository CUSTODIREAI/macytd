# YouTube Batcher - Windows Installation Guide

Complete guide for running YouTube Batcher on Windows 10/11

---

## Option 1: Run from Source (Easiest)

**Requires:** Python 3.7 or later

### Step 1: Install Python

1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Install Python

### Step 2: Download YouTube Batcher

Clone or download this repository:
```cmd
git clone https://github.com/CUSTODIREAI/macytd.git
cd macytd
```

Or download ZIP and extract it.

### Step 3: Run the Launcher

**Double-click:** `launch-batcher.bat`

The launcher will:
- Check if Python is installed
- Install dependencies (PyQt5, yt-dlp)
- Launch YouTube Batcher

**Or run from Command Prompt:**
```cmd
launch-batcher.bat
```

**Or run directly with Python:**
```cmd
python YouTube-Batcher-Windows.py
```

---

## Option 2: Build Standalone .exe

**Build it yourself (requires Python on build machine):**

### Step 1: Install Build Tools

```cmd
pip install pyinstaller
```

### Step 2: Build the .exe

```cmd
python build-exe.py
```

This creates: `dist\YouTube-Batcher.exe`

### Step 3: Distribute

The `.exe` file can run on any Windows 10/11 PC without Python installed!

**Note:** Users still need `yt-dlp` installed. Include `install-yt-dlp.bat` (below).

---

## Option 3: Manual Installation

### Install Dependencies

```cmd
pip install PyQt5 yt-dlp
```

### Run Application

```cmd
python YouTube-Batcher-Windows.py
```

---

## Creating install-yt-dlp.bat for Users

If distributing the .exe, include this batch file:

```batch
@echo off
echo Installing yt-dlp...
pip install yt-dlp
echo.
echo Installation complete!
pause
```

---

## System Requirements

- **OS:** Windows 10 or Windows 11
- **Python:** 3.7 or later (for source version)
- **Disk:** 100MB free space
- **Memory:** 2GB RAM recommended

---

## Dependencies

```
PyQt5>=5.12
yt-dlp>=2023.1.1
```

---

## Usage

### Running YouTube Batcher

1. **Launch** the application (double-click .bat or .exe)

2. **Add batch items:**
   - URL: Enter YouTube channel/playlist/video URL
   - Output Folder: Click "Browse" and select destination
   - Click "➕ Add to Batch"
   - Repeat for all items you want

3. **Configure settings:**
   - Quality: Choose video quality
   - Archive: Check to skip already-downloaded videos

4. **Start batch:**
   - Click "▶️ Start Batch"
   - Watch progress in log window
   - Each item downloads sequentially to its own folder

5. **Save batch (optional):**
   - Click "💾 Save Batch" to save your list
   - Load it later with "📂 Load Batch"

---

## Building EXE with Icon

### Step 1: Create/Download Icon

Save an icon as `batcher-icon.ico` in the project folder.

### Step 2: Modify build-exe.py

Change this line:
```python
'--icon=NONE',
```

To:
```python
'--icon=batcher-icon.ico',
```

### Step 3: Build

```cmd
python build-exe.py
```

---

## Troubleshooting

### Python not found

**Error:** `'python' is not recognized as an internal or external command`

**Fix:**
1. Reinstall Python from https://www.python.org/downloads/
2. **Check** "Add Python to PATH" during installation
3. Restart Command Prompt

### PyQt5 installation fails

**Error:** `Could not build wheels for PyQt5`

**Fix:**
```cmd
pip install --upgrade pip
pip install PyQt5 --only-binary=:all:
```

### yt-dlp not found

**Error:** `ModuleNotFoundError: No module named 'yt_dlp'`

**Fix:**
```cmd
pip install yt-dlp
```

### Downloads fail with 403 errors

**Fix:**
- Update yt-dlp: `pip install -U yt-dlp`
- Or use the "Check & Update" button in the app (if you add that feature)

### Application won't start

**Fix:**
Run from Command Prompt to see errors:
```cmd
cd path\to\macytd
python YouTube-Batcher-Windows.py
```

### Permission denied error

**Fix:**
Run Command Prompt as Administrator:
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Run the command again

---

## Features

### Batch Processing
- Add unlimited URL + folder pairs
- Sequential processing (one after another)
- Individual output folders per item
- Real-time progress tracking

### Batch Management
- Save batch lists to JSON files
- Load saved batches
- Remove individual items
- Clear entire queue

### Download Features
- Multiple quality options (1080p, 720p, 480p, best)
- Download archive (skip duplicates)
- Firefox cookie support
- October 2025 bypass fix built-in
- Unlimited downloads (no cap)

---

## Example Batch

**Downloading multiple channels to organized folders:**

```
Item 1:
  URL: https://www.youtube.com/@cspan
  Folder: C:\Downloads\YouTube\cspan

Item 2:
  URL: https://www.youtube.com/@mitocw
  Folder: C:\Downloads\YouTube\mit

Item 3:
  URL: https://www.youtube.com/@lexfridman
  Folder: C:\Downloads\YouTube\lex-fridman

Item 4:
  URL: https://www.youtube.com/@TED
  Folder: C:\Downloads\YouTube\ted
```

Click "Start Batch" → Downloads sequentially → Each channel in its own folder!

---

## Advanced: Silent Install Script

Create `install-all.bat`:

```batch
@echo off
echo Installing Python packages...
pip install --quiet PyQt5 yt-dlp
echo Done!
```

---

## Distribution Package

**If you want to distribute to Windows users:**

### Package Contents:
```
YouTube-Batcher/
├── YouTube-Batcher.exe         (built with PyInstaller)
├── install-yt-dlp.bat          (yt-dlp installer)
├── README.txt                  (usage instructions)
└── examples/                   (example batch files)
    └── sample-batch.json
```

### Include README.txt:

```
YouTube Batch Downloader - The Batcher

1. First time setup:
   - Double-click: install-yt-dlp.bat
   - Wait for installation to complete

2. Run the application:
   - Double-click: YouTube-Batcher.exe

3. Add downloads:
   - Enter URL and select output folder
   - Click "Add to Batch"
   - Repeat for all items

4. Start downloading:
   - Click "Start Batch"
   - Wait for completion

For help: https://github.com/CUSTODIREAI/macytd
```

---

## Building from Source

### Full Build Process:

```cmd
# 1. Install build tools
pip install pyinstaller

# 2. Clone repository
git clone https://github.com/CUSTODIREAI/macytd.git
cd macytd

# 3. Build executable
python build-exe.py

# 4. Test the executable
dist\YouTube-Batcher.exe

# 5. Distribute
# Copy dist\YouTube-Batcher.exe to users
```

---

## PyInstaller Options Explained

**In build-exe.py:**

- `--onefile`: Single .exe (not a folder)
- `--windowed`: No console window (GUI only)
- `--icon`: Application icon
- `--add-data`: Include extra files
- `--hidden-import`: Force include modules
- `--clean`: Clean build cache
- `--noconfirm`: Overwrite without asking

---

## Alternative: Create Installer

**Using Inno Setup (advanced):**

1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Create installer script (`installer.iss`)
3. Include:
   - YouTube-Batcher.exe
   - Python installer
   - yt-dlp installer
   - Desktop shortcut

**This creates:** `YouTube-Batcher-Setup.exe`

---

## Security Note

**Windows SmartScreen warning:**

When running the .exe for the first time, Windows may show:
```
"Windows protected your PC"
```

This is normal for unsigned applications. Click:
1. "More info"
2. "Run anyway"

**To avoid this:** Code-sign the .exe (requires certificate, costs money)

---

## File Locations

**Python Script:**
- `YouTube-Batcher-Windows.py`

**Launcher:**
- `launch-batcher.bat`

**Build Script:**
- `build-exe.py`

**Output:**
- `dist\YouTube-Batcher.exe` (after build)

**Batch Lists:**
- Saved as `.json` files (user-selected location)

**Downloads:**
- User-selected output folders

---

## Support

**Issues?**
- GitHub Issues: https://github.com/CUSTODIREAI/macytd/issues
- Check README.md for updates

**Updates:**
- Pull latest: `git pull`
- Or download new ZIP from GitHub

---

## Version Info

- **Application:** YouTube Batch Downloader (The Batcher)
- **Platform:** Windows 10/11
- **Python:** 3.7+ required (for source version)
- **License:** See repository LICENSE file

---

Last Updated: October 2025
