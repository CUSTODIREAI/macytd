"""
PyInstaller Build Script for YouTube Batcher (Windows .exe)

Run this on Windows to create a standalone .exe:
    python build-exe.py

Output: dist/YouTube-Batcher.exe
"""

import PyInstaller.__main__
import os

# PyInstaller configuration
PyInstaller.__main__.run([
    'YouTube-Batcher-Windows.py',
    '--name=YouTube-Batcher',
    '--onefile',
    '--windowed',
    '--icon=NONE',  # Add icon file if you have one
    '--add-data=README.md;.',
    '--hidden-import=PyQt5',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    '--clean',
    '--noconfirm',
])

print("\n" + "="*70)
print("BUILD COMPLETE!")
print("="*70)
print(f"\nExecutable location: dist\\YouTube-Batcher.exe")
print("\nYou can now distribute dist\\YouTube-Batcher.exe")
print("\nNote: Users still need to install yt-dlp separately:")
print("  pip install yt-dlp")
print("\nOr use the provided installer script.")
print("="*70)
