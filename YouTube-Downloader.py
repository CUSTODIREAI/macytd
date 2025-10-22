#!/usr/bin/env python3
"""
YouTube ULTIMATE Downloader 2025 - macOS Version
Professional-grade YouTube downloader with all latest fixes
- Auto-updates yt-dlp to latest version
- Bypasses YouTube's October 2025 403 restrictions
- Uses player_js_version=actual fix
- High-quality downloads with multiple format options
- Download archive tracking
- Real-time progress display
"""

import sys
import os
import subprocess
import threading
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QPushButton,
                           QTextEdit, QComboBox, QProgressBar, QGroupBox,
                           QCheckBox, QSpinBox, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor

class YtdlpUpdateThread(QThread):
    """Thread to check and update yt-dlp"""
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def run(self):
        try:
            self.update_signal.emit("🔍 Checking yt-dlp version...")

            # Check current version
            result = subprocess.run(['yt-dlp', '--version'],
                                  capture_output=True, text=True, timeout=10)
            current_version = result.stdout.strip() if result.returncode == 0 else "Unknown"

            self.update_signal.emit(f"📌 Current version: {current_version}")
            self.update_signal.emit("⬆️  Updating yt-dlp to latest version...")

            # Update yt-dlp (macOS uses pip3)
            update_result = subprocess.run(
                ['pip3', 'install', '-U', 'yt-dlp'],
                capture_output=True, text=True, timeout=120
            )

            if update_result.returncode == 0:
                # Check new version
                new_result = subprocess.run(['yt-dlp', '--version'],
                                          capture_output=True, text=True, timeout=10)
                new_version = new_result.stdout.strip() if new_result.returncode == 0 else "Unknown"

                if new_version != current_version:
                    self.update_signal.emit(f"✅ Updated to version: {new_version}")
                    self.finished_signal.emit(True, f"yt-dlp updated: {current_version} → {new_version}")
                else:
                    self.update_signal.emit(f"✅ Already up to date: {new_version}")
                    self.finished_signal.emit(True, f"yt-dlp already latest: {new_version}")
            else:
                self.update_signal.emit(f"⚠️  Update failed: {update_result.stderr}")
                self.finished_signal.emit(False, update_result.stderr)

        except Exception as e:
            self.update_signal.emit(f"❌ Error: {str(e)}")
            self.finished_signal.emit(False, str(e))

class DownloadThread(QThread):
    """Thread to handle video downloads"""
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)  # current, total
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, url, output_dir, quality, use_archive, max_downloads):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.quality = quality
        self.use_archive = use_archive
        self.max_downloads = max_downloads
        self.process = None
        self.stopped = False

    def run(self):
        try:
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)

            # Build command with all latest fixes
            cmd = [
                'yt-dlp',
                '--cookies-from-browser', 'firefox',
                '-4',  # Force IPv4
                '--extractor-args', 'youtube:player_client=web_safari;player_js_version=actual',  # THE FIX!
            ]

            # Quality settings
            if self.quality == "Best (≤1080p)":
                cmd.extend(['-f', 'best[height<=1080]'])
            elif self.quality == "Best (≤720p)":
                cmd.extend(['-f', 'best[height<=720]'])
            elif self.quality == "Best (≤480p)":
                cmd.extend(['-f', 'best[height<=480]'])
            elif self.quality == "Best Available":
                cmd.extend(['-f', 'best'])

            # Download archive
            if self.use_archive:
                archive_file = os.path.join(self.output_dir, 'download_archive.txt')
                cmd.extend(['--download-archive', archive_file])

            # Max downloads
            if self.max_downloads > 0:
                cmd.extend(['--max-downloads', str(self.max_downloads)])

            # Additional settings
            cmd.extend([
                '--sleep-interval', '3',
                '--max-sleep-interval', '10',
                '--ignore-errors',
                '--no-abort-on-error',
                '--write-info-json',
                '--concurrent-fragments', '8',
                '-o', os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                self.url
            ])

            self.log_signal.emit(f"🚀 Starting download with command:")
            self.log_signal.emit(f"   {' '.join(cmd)}")
            self.log_signal.emit("")

            # Run download process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            current_item = 0
            total_items = 0

            # Read output line by line
            for line in self.process.stdout:
                if self.stopped:
                    break

                line = line.strip()
                if line:
                    self.log_signal.emit(line)

                    # Parse progress
                    if "Downloading item" in line:
                        try:
                            parts = line.split()
                            if "of" in parts:
                                idx = parts.index("of")
                                current_item = int(parts[idx - 1])
                                total_items = int(parts[idx + 1])
                                self.progress_signal.emit(current_item, total_items)
                        except:
                            pass

            self.process.wait()

            if self.stopped:
                self.finished_signal.emit(False, "Download stopped by user")
            elif self.process.returncode == 0:
                self.finished_signal.emit(True, f"Download completed! ({current_item}/{total_items} videos)")
            else:
                self.finished_signal.emit(False, f"Download failed with code {self.process.returncode}")

        except Exception as e:
            self.log_signal.emit(f"❌ Error: {str(e)}")
            self.finished_signal.emit(False, str(e))

    def stop(self):
        """Stop the download process"""
        self.stopped = True
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except:
                self.process.kill()

class YouTubeDownloaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.update_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube ULTIMATE Downloader 2025 - macOS Edition")
        self.setGeometry(100, 100, 900, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("YouTube ULTIMATE Downloader 2025")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("✅ Bypasses YouTube Oct 2025 403 Restrictions | ✅ Auto-Updates yt-dlp")
        subtitle.setFont(QFont("Arial", 9))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #2E7D32;")
        layout.addWidget(subtitle)

        # Update section
        update_group = QGroupBox("yt-dlp Updates")
        update_layout = QHBoxLayout()

        self.update_btn = QPushButton("🔄 Check & Update yt-dlp")
        self.update_btn.clicked.connect(self.check_update)
        update_layout.addWidget(self.update_btn)

        self.update_status = QLabel("Ready")
        update_layout.addWidget(self.update_status)
        update_layout.addStretch()

        update_group.setLayout(update_layout)
        layout.addWidget(update_group)

        # URL input
        url_group = QGroupBox("YouTube URL")
        url_layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube channel, playlist, or video URL...")
        url_layout.addWidget(self.url_input)

        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        # Settings
        settings_group = QGroupBox("Download Settings")
        settings_layout = QVBoxLayout()

        # Output directory
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Output Directory:"))
        self.dir_input = QLineEdit(os.path.expanduser("~/Downloads/youtube"))
        dir_layout.addWidget(self.dir_input)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        settings_layout.addLayout(dir_layout)

        # Quality and options
        options_layout = QHBoxLayout()

        options_layout.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Best (≤1080p)",
            "Best (≤720p)",
            "Best (≤480p)",
            "Best Available"
        ])
        options_layout.addWidget(self.quality_combo)

        self.archive_check = QCheckBox("Use Download Archive (skip duplicates)")
        self.archive_check.setChecked(True)
        options_layout.addWidget(self.archive_check)
        options_layout.addStretch()

        settings_layout.addLayout(options_layout)

        # Max downloads
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("Max Downloads:"))
        self.max_spin = QSpinBox()
        self.max_spin.setMinimum(0)
        self.max_spin.setMaximum(10000)
        self.max_spin.setValue(0)  # Default: Unlimited
        self.max_spin.setSpecialValueText("Unlimited")
        max_layout.addWidget(self.max_spin)
        max_layout.addStretch()
        settings_layout.addLayout(max_layout)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Progress
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("Ready to download")
        progress_layout.addWidget(self.progress_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Control buttons
        control_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶️  Start Download")
        self.start_btn.clicked.connect(self.start_download)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        control_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹️  Stop")
        self.stop_btn.clicked.connect(self.stop_download)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-weight: bold;")
        control_layout.addWidget(self.stop_btn)

        self.clear_btn = QPushButton("🗑️  Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        control_layout.addWidget(self.clear_btn)

        layout.addLayout(control_layout)

        # Log output
        log_group = QGroupBox("Download Log")
        log_layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Menlo", 9))  # macOS monospace font
        log_layout.addWidget(self.log_output)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Status bar
        self.statusBar().showMessage("Ready | Latest yt-dlp with October 2025 bypass fix included")

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.dir_input.setText(directory)

    def check_update(self):
        if self.update_thread and self.update_thread.isRunning():
            return

        self.update_btn.setEnabled(False)
        self.update_status.setText("Updating...")

        self.update_thread = YtdlpUpdateThread()
        self.update_thread.update_signal.connect(self.log_message)
        self.update_thread.finished_signal.connect(self.update_finished)
        self.update_thread.start()

    def update_finished(self, success, message):
        self.update_btn.setEnabled(True)
        if success:
            self.update_status.setText("✅ Up to date")
            self.update_status.setStyleSheet("color: green;")
        else:
            self.update_status.setText("⚠️  Update failed")
            self.update_status.setStyleSheet("color: red;")

    def start_download(self):
        url = self.url_input.text().strip()
        output_dir = self.dir_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a YouTube URL")
            return

        if not output_dir:
            QMessageBox.warning(self, "Input Error", "Please select output directory")
            return

        # Start download
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)

        self.download_thread = DownloadThread(
            url=url,
            output_dir=output_dir,
            quality=self.quality_combo.currentText(),
            use_archive=self.archive_check.isChecked(),
            max_downloads=self.max_spin.value()
        )

        self.download_thread.log_signal.connect(self.log_message)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()

        self.log_message(f"\n{'='*60}")
        self.log_message(f"Download started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_message(f"{'='*60}\n")

    def stop_download(self):
        if self.download_thread:
            self.log_message("\n⏹️  Stopping download...")
            self.download_thread.stop()

    def download_finished(self, success, message):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        self.log_message(f"\n{'='*60}")
        if success:
            self.log_message(f"✅ {message}")
            self.statusBar().showMessage(f"Download completed: {message}")
            QMessageBox.information(self, "Success", message)
        else:
            self.log_message(f"❌ {message}")
            self.statusBar().showMessage(f"Download failed: {message}")
        self.log_message(f"{'='*60}\n")

    def update_progress(self, current, total):
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.progress_label.setText(f"Downloading: {current} / {total} videos ({percentage}%)")

    def log_message(self, message):
        self.log_output.append(message)
        self.log_output.moveCursor(QTextCursor.End)

    def clear_log(self):
        self.log_output.clear()

def main():
    app = QApplication(sys.argv)

    # macOS-specific styling
    app.setStyle('Fusion')

    window = YouTubeDownloaderGUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
