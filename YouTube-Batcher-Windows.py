#!/usr/bin/env python3
"""
YouTube Batch Downloader - The Batcher (Windows Version)
Sequential batch downloading with individual output folders
- Add unlimited URL + output folder pairs
- Sequential processing with progress tracking
- Save/load batch lists
- Pause/resume capability
- Windows 10/11 compatible
"""

import sys
import os
import subprocess
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QPushButton,
                           QTextEdit, QComboBox, QProgressBar, QGroupBox,
                           QCheckBox, QMessageBox, QFileDialog, QTableWidget,
                           QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor

class BatchDownloadThread(QThread):
    """Thread to handle batch video downloads"""
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)  # current item, total items
    item_progress_signal = pyqtSignal(str)  # current download status
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, batch_items, quality, use_archive):
        super().__init__()
        self.batch_items = batch_items  # List of (url, output_dir) tuples
        self.quality = quality
        self.use_archive = use_archive
        self.process = None
        self.stopped = False
        self.paused = False
        self.current_item = 0

    def run(self):
        try:
            total_items = len(self.batch_items)
            successful = 0
            failed = 0

            for idx, (url, output_dir) in enumerate(self.batch_items):
                if self.stopped:
                    break

                # Wait if paused
                while self.paused and not self.stopped:
                    self.msleep(100)

                if self.stopped:
                    break

                self.current_item = idx
                self.progress_signal.emit(idx + 1, total_items)

                self.log_signal.emit(f"\n{'='*70}")
                self.log_signal.emit(f"📥 Batch Item {idx + 1}/{total_items}")
                self.log_signal.emit(f"URL: {url}")
                self.log_signal.emit(f"Output: {output_dir}")
                self.log_signal.emit(f"{'='*70}\n")

                # Create output directory
                os.makedirs(output_dir, exist_ok=True)

                # Build command
                cmd = [
                    'yt-dlp',
                    '--cookies-from-browser', 'firefox',
                    '-4',  # Force IPv4
                    '--extractor-args', 'youtube:player_client=web_safari;player_js_version=actual',
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
                    archive_file = os.path.join(output_dir, 'download_archive.txt')
                    cmd.extend(['--download-archive', archive_file])

                # Additional settings
                cmd.extend([
                    '--sleep-interval', '3',
                    '--max-sleep-interval', '10',
                    '--ignore-errors',
                    '--no-abort-on-error',
                    '--write-info-json',
                    '--concurrent-fragments', '8',
                    '-o', os.path.join(output_dir, '%(title)s.%(ext)s'),
                    url
                ])

                self.item_progress_signal.emit(f"Downloading item {idx + 1}/{total_items}...")

                # Run download process (Windows-compatible)
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )

                # Read output line by line
                for line in self.process.stdout:
                    if self.stopped:
                        break

                    line = line.strip()
                    if line:
                        self.log_signal.emit(line)

                self.process.wait()

                if self.stopped:
                    self.log_signal.emit(f"\n⏹️  Batch stopped at item {idx + 1}/{total_items}")
                    break
                elif self.process.returncode == 0:
                    successful += 1
                    self.log_signal.emit(f"\n✅ Item {idx + 1}/{total_items} completed successfully!")
                else:
                    failed += 1
                    self.log_signal.emit(f"\n❌ Item {idx + 1}/{total_items} failed (exit code: {self.process.returncode})")

            # Final summary
            if self.stopped:
                self.finished_signal.emit(False, f"Batch stopped: {successful} successful, {failed} failed, {total_items - successful - failed} not processed")
            else:
                self.finished_signal.emit(True, f"Batch complete: {successful} successful, {failed} failed out of {total_items} items")

        except Exception as e:
            self.log_signal.emit(f"❌ Error: {str(e)}")
            self.finished_signal.emit(False, str(e))

    def stop(self):
        """Stop the batch process"""
        self.stopped = True
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except:
                self.process.kill()

    def pause(self):
        """Pause the batch process"""
        self.paused = True

    def resume(self):
        """Resume the batch process"""
        self.paused = False

class YouTubeBatcherGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.batch_items = []  # List of (url, output_dir) tuples
        self.download_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube Batch Downloader - The Batcher (Windows)")
        self.setGeometry(100, 100, 1100, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("YouTube Batch Downloader - The Batcher")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Add multiple downloads • Sequential processing • Individual output folders")
        subtitle.setFont(QFont("Arial", 9))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #1976D2;")
        layout.addWidget(subtitle)

        # Add Item Section
        add_group = QGroupBox("Add Batch Item")
        add_layout = QVBoxLayout()

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube channel, playlist, or video URL...")
        url_layout.addWidget(self.url_input)
        add_layout.addLayout(url_layout)

        # Output directory
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Output Folder:"))
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Select output directory for this item...")
        dir_layout.addWidget(self.dir_input)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        add_layout.addLayout(dir_layout)

        # Add button
        add_btn_layout = QHBoxLayout()
        add_btn_layout.addStretch()
        self.add_btn = QPushButton("➕ Add to Batch")
        self.add_btn.clicked.connect(self.add_batch_item)
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px; font-weight: bold;")
        add_btn_layout.addWidget(self.add_btn)
        add_btn_layout.addStretch()
        add_layout.addLayout(add_btn_layout)

        add_group.setLayout(add_layout)
        layout.addWidget(add_group)

        # Batch List Table
        batch_group = QGroupBox("Batch Queue")
        batch_layout = QVBoxLayout()

        self.batch_table = QTableWidget()
        self.batch_table.setColumnCount(3)
        self.batch_table.setHorizontalHeaderLabels(["#", "URL", "Output Folder"])
        self.batch_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.batch_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.batch_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.batch_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        batch_layout.addWidget(self.batch_table)

        # Batch controls
        batch_controls = QHBoxLayout()

        self.remove_btn = QPushButton("🗑️ Remove Selected")
        self.remove_btn.clicked.connect(self.remove_batch_item)
        batch_controls.addWidget(self.remove_btn)

        self.clear_batch_btn = QPushButton("Clear All")
        self.clear_batch_btn.clicked.connect(self.clear_batch)
        batch_controls.addWidget(self.clear_batch_btn)

        batch_controls.addStretch()

        self.save_batch_btn = QPushButton("💾 Save Batch")
        self.save_batch_btn.clicked.connect(self.save_batch)
        batch_controls.addWidget(self.save_batch_btn)

        self.load_batch_btn = QPushButton("📂 Load Batch")
        self.load_batch_btn.clicked.connect(self.load_batch)
        batch_controls.addWidget(self.load_batch_btn)

        batch_layout.addLayout(batch_controls)

        batch_group.setLayout(batch_layout)
        layout.addWidget(batch_group)

        # Settings
        settings_group = QGroupBox("Download Settings")
        settings_layout = QHBoxLayout()

        settings_layout.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Best (≤1080p)",
            "Best (≤720p)",
            "Best (≤480p)",
            "Best Available"
        ])
        settings_layout.addWidget(self.quality_combo)

        self.archive_check = QCheckBox("Use Download Archive (skip duplicates)")
        self.archive_check.setChecked(True)
        settings_layout.addWidget(self.archive_check)
        settings_layout.addStretch()

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Progress
        progress_group = QGroupBox("Batch Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("Ready to start batch download")
        progress_layout.addWidget(self.progress_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Control buttons
        control_layout = QHBoxLayout()

        self.start_btn = QPushButton("▶️  Start Batch")
        self.start_btn.clicked.connect(self.start_batch)
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        control_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹️  Stop")
        self.stop_btn.clicked.connect(self.stop_batch)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-weight: bold;")
        control_layout.addWidget(self.stop_btn)

        self.clear_log_btn = QPushButton("🗑️  Clear Log")
        self.clear_log_btn.clicked.connect(self.clear_log)
        control_layout.addWidget(self.clear_log_btn)

        layout.addLayout(control_layout)

        # Log output
        log_group = QGroupBox("Download Log")
        log_layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        # Use Consolas for Windows (monospace)
        self.log_output.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_output)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Status bar
        self.statusBar().showMessage("Ready | Add items to batch queue")

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.dir_input.setText(directory)

    def add_batch_item(self):
        url = self.url_input.text().strip()
        output_dir = self.dir_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a YouTube URL")
            return

        if not output_dir:
            QMessageBox.warning(self, "Input Error", "Please select an output directory")
            return

        # Add to batch
        self.batch_items.append((url, output_dir))

        # Add to table
        row = self.batch_table.rowCount()
        self.batch_table.insertRow(row)
        self.batch_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.batch_table.setItem(row, 1, QTableWidgetItem(url))
        self.batch_table.setItem(row, 2, QTableWidgetItem(output_dir))

        # Clear inputs
        self.url_input.clear()
        self.dir_input.clear()

        self.statusBar().showMessage(f"Added to batch | Total items: {len(self.batch_items)}")
        self.log_message(f"✅ Added to batch: {url} → {output_dir}")

    def remove_batch_item(self):
        selected_rows = set(item.row() for item in self.batch_table.selectedItems())

        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select an item to remove")
            return

        # Remove in reverse order to maintain indices
        for row in sorted(selected_rows, reverse=True):
            self.batch_table.removeRow(row)
            del self.batch_items[row]

        # Renumber remaining items
        for row in range(self.batch_table.rowCount()):
            self.batch_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

        self.statusBar().showMessage(f"Removed from batch | Total items: {len(self.batch_items)}")

    def clear_batch(self):
        if not self.batch_items:
            return

        reply = QMessageBox.question(self, "Clear Batch",
                                     f"Clear all {len(self.batch_items)} items from batch?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.batch_items.clear()
            self.batch_table.setRowCount(0)
            self.statusBar().showMessage("Batch cleared")
            self.log_message("🗑️  Batch queue cleared")

    def save_batch(self):
        if not self.batch_items:
            QMessageBox.warning(self, "Save Error", "No items in batch to save")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Batch List", "", "JSON Files (*.json);;All Files (*)"
        )

        if filename:
            try:
                batch_data = {
                    'items': self.batch_items,
                    'quality': self.quality_combo.currentText(),
                    'use_archive': self.archive_check.isChecked(),
                    'created': datetime.now().isoformat()
                }

                with open(filename, 'w') as f:
                    json.dump(batch_data, f, indent=2)

                QMessageBox.information(self, "Success", f"Batch saved to {filename}")
                self.log_message(f"💾 Batch saved: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save batch: {str(e)}")

    def load_batch(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Batch List", "", "JSON Files (*.json);;All Files (*)"
        )

        if filename:
            try:
                with open(filename, 'r') as f:
                    batch_data = json.load(f)

                # Clear existing batch
                self.batch_items.clear()
                self.batch_table.setRowCount(0)

                # Load items
                for url, output_dir in batch_data['items']:
                    self.batch_items.append((url, output_dir))
                    row = self.batch_table.rowCount()
                    self.batch_table.insertRow(row)
                    self.batch_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                    self.batch_table.setItem(row, 1, QTableWidgetItem(url))
                    self.batch_table.setItem(row, 2, QTableWidgetItem(output_dir))

                # Load settings
                if 'quality' in batch_data:
                    index = self.quality_combo.findText(batch_data['quality'])
                    if index >= 0:
                        self.quality_combo.setCurrentIndex(index)

                if 'use_archive' in batch_data:
                    self.archive_check.setChecked(batch_data['use_archive'])

                QMessageBox.information(self, "Success", f"Loaded {len(self.batch_items)} items from {filename}")
                self.log_message(f"📂 Batch loaded: {filename} ({len(self.batch_items)} items)")

            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load batch: {str(e)}")

    def start_batch(self):
        if not self.batch_items:
            QMessageBox.warning(self, "Batch Error", "No items in batch queue")
            return

        # Start batch download
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.add_btn.setEnabled(False)
        self.progress_bar.setValue(0)

        self.download_thread = BatchDownloadThread(
            batch_items=self.batch_items.copy(),
            quality=self.quality_combo.currentText(),
            use_archive=self.archive_check.isChecked()
        )

        self.download_thread.log_signal.connect(self.log_message)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.item_progress_signal.connect(self.update_item_progress)
        self.download_thread.finished_signal.connect(self.batch_finished)
        self.download_thread.start()

        self.log_message(f"\n{'='*70}")
        self.log_message(f"🚀 Batch started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_message(f"Total items: {len(self.batch_items)}")
        self.log_message(f"Quality: {self.quality_combo.currentText()}")
        self.log_message(f"Archive: {'Enabled' if self.archive_check.isChecked() else 'Disabled'}")
        self.log_message(f"{'='*70}\n")

    def stop_batch(self):
        if self.download_thread:
            self.log_message("\n⏹️  Stopping batch...")
            self.download_thread.stop()

    def batch_finished(self, success, message):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.add_btn.setEnabled(True)

        self.log_message(f"\n{'='*70}")
        if success:
            self.log_message(f"✅ {message}")
            self.statusBar().showMessage(f"Batch completed: {message}")
            QMessageBox.information(self, "Batch Complete", message)
        else:
            self.log_message(f"⚠️  {message}")
            self.statusBar().showMessage(f"Batch stopped: {message}")
        self.log_message(f"{'='*70}\n")

    def update_progress(self, current, total):
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.progress_label.setText(f"Processing: {current} / {total} items ({percentage}%)")

    def update_item_progress(self, status):
        self.progress_label.setText(status)

    def log_message(self, message):
        self.log_output.append(message)
        self.log_output.moveCursor(QTextCursor.End)

    def clear_log(self):
        self.log_output.clear()

def main():
    app = QApplication(sys.argv)

    # Windows styling
    app.setStyle('Fusion')

    window = YouTubeBatcherGUI()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
