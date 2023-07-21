import sys
import os
import csv
import concurrent.futures
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QHeaderView, QProgressBar, QFileDialog, QTableWidgetItem)

from PyQt6.QtCore import Qt

class FilesDownloader(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Files Downloader')
        self.setFixedWidth(600)

        # Labels
        self.file_list_path = QLabel('List file:')
        self.target_dir_path = QLabel('Target directory:')

        # Browse Buttons
        self.file_list_browse = QPushButton('Browse file list')
        self.file_list_browse.setFixedHeight(50)
        self.file_list_browse.clicked.connect(self.open_file_list)
        self.directory_browse = QPushButton('Browse directory target')
        self.directory_browse.setFixedHeight(50)
        self.directory_browse.clicked.connect(self.open_target_dir)

        # Hold file path and folder path
        self.file_list = ''
        self.target_dir = ''

        # Flag
        self.download_start = False

        # Data
        self.data = []
        self.total = 0
        self.success = 0
        self.fail = 0

        # Table
        self.download_table = QTableWidget(1, 3)
        self.download_table_header = self.download_table.horizontalHeader()
        self.download_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.download_table.setHorizontalHeaderLabels(["URL", "CHECKSUM", "STATUS"])

        # Progress bar
        self.download_progress = QProgressBar()
        self.download_progress.setValue(0)

        # Actions button
        self.check_link_btn = QPushButton('Check File Links')
        self.check_link_btn.setDisabled(True)
        self.check_link_btn.clicked.connect(self.check_file)
        self.start_download_btn = QPushButton('Start/Stop Download')
        self.start_download_btn.setDisabled(True)
        self.start_download_btn.clicked.connect(self.start_download)
        self.save_log_btn = QPushButton('Save Log')
        self.save_log_btn.setDisabled(True)
        self.clean_download_btn = QPushButton('Clean Download')
        self.clean_download_btn.setDisabled(True)
        self.clean_download_btn.clicked.connect(self.clean_download)

        # Report Label
        self.download_total = QLabel('Total:')
        self.download_total.setText(f'Total: {self.total}')
        self.download_success = QLabel('Success:')
        self.download_success.setText(f'Success: {self.success}')
        self.download_fail = QLabel('Fail:')
        self.download_fail.setText(f'Fail: {self.fail}')

        # Load ui
        self.init_ui()

    def init_ui(self):
        downloader_layout = QVBoxLayout()

        # File list box
        file_source_box = QGroupBox('File List')
        file_source_layout = QVBoxLayout()
        file_source_layout.addWidget(self.file_list_path)
        file_source_layout.addWidget(self.file_list_browse)
        file_source_box.setLayout(file_source_layout)

        # Directory target box
        target_directory_box = QGroupBox('Download Directory')
        target_directory_layout = QVBoxLayout()
        target_directory_layout.addWidget(self.target_dir_path)
        target_directory_layout.addWidget(self.directory_browse)
        target_directory_box.setLayout(target_directory_layout)

        # Download progress
        download_progress_box = QGroupBox('Download Progress')
        download_progress_box.setFixedHeight(400)
        download_progress_layout = QVBoxLayout()
        download_progress_layout.addWidget(self.download_table)
        download_progress_box.setLayout(download_progress_layout)

        # Progress bar
        progress_bar_box = QGroupBox('Progress')
        progress_bar_layout = QVBoxLayout()
        progress_bar_layout.addWidget(self.download_progress)
        progress_bar_box.setLayout(progress_bar_layout)

        # Actions button box
        action_buttons_box = QGroupBox('Actions')
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(self.check_link_btn)
        action_buttons_layout.addWidget(self.start_download_btn)
        action_buttons_layout.addWidget(self.save_log_btn)
        action_buttons_layout.addWidget(self.clean_download_btn)
        action_buttons_box.setLayout(action_buttons_layout)

        # Report box
        report_section_box = QGroupBox('Reports')
        report_sections_layout = QHBoxLayout()
        report_sections_layout.addWidget(self.download_total)
        report_sections_layout.addWidget(self.download_success)
        report_sections_layout.addWidget(self.download_fail)
        report_section_box.setLayout(report_sections_layout)


        # Main Layout
        downloader_layout.addWidget(file_source_box)
        downloader_layout.addWidget(target_directory_box)
        downloader_layout.addWidget(download_progress_box)
        downloader_layout.addWidget(progress_bar_box)
        downloader_layout.addWidget(action_buttons_box)
        downloader_layout.addWidget(report_section_box)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(downloader_layout)
        self.setCentralWidget(central_widget)
        self.show()

    def open_file_list(self):
        paths, _ = QFileDialog.getOpenFileNames(self, 'Select file', '', 'CSV File (*.csv)')
        if paths:
            self.file_list = paths[0]
            self.file_list_path.setText(f'List file: {self.file_list}')
            self.load_file_list()

    def open_target_dir(self, file):
        dir = QFileDialog.getExistingDirectory(self, 'Select target directory', options=QFileDialog.Option.ShowDirsOnly)
        if dir:
            self.target_dir = dir
            self.target_dir_path.setText(f'Target directory: {self.target_dir}')
            if os.access(dir, os.W_OK):
                self.check_link_btn.setDisabled(False)
                self.start_download_btn.setDisabled(False)
                self.save_log_btn.setDisabled(False)
                self.clean_download_btn.setDisabled(False)

    def load_file_list(self):
        if self.file_list:
            file_ext = os.path.splitext(self.file_list)[1]
            if file_ext == '.csv':
                with open(self.file_list, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    rows = list(reader)
                    self.data = rows[1:]
                    self.total = len(self.data)
                    self.download_table.setRowCount(self.total)
                    for index, row in enumerate(self.data):
                        self.download_table.setItem(index, 0, QTableWidgetItem(row[0]))
                        self.download_table.setItem(index, 1, QTableWidgetItem(row[1]))
                        self.download_table.setItem(index, 2, QTableWidgetItem(row[2]))
                self.download_total.setText(f'Total: {self.total}')

            if self.total > 0 and self.target_dir != '':
                self.check_link_btn.setDisabled(False)
                self.start_download_btn.setDisabled(False)
                self.save_log_btn.setDisabled(False)
                self.clean_download_btn.setDisabled(False)

    def start_download(self):
        if self.total > 0:
            file_urls = []
            self.success = 0
            self.fail = 0
            for row in self.data:
                save_path = row[0] + '/' + os.path.basename(row[0])
                file_urls.append(save_path)

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(self.download_file, url, f"{self.target_dir}/{os.path.basename(url)}") for url in file_urls]
                concurrent.futures.wait(futures)

    def download_file(self, url, save_path):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
                self.success += 1
        else:
            self.fail += 1

        self.download_success.setText(f'Success: {self.success}')
        self.download_fail.setText(f'Fail: {self.fail}')

    def check_file(self):
        if self.data:
            for row in self.data:
                url = row[0]
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    self.success += 1
                else:
                    self.fail += 1

        self.download_success.setText(f'Success: {self.success}')
        self.download_fail.setText(f'Fail: {self.fail}')

    def clean_download(self):
        for filename in os.listdir(self.target_dir):
            file_path = os.path.join(self.target_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f'Removed file: {file_path}')
            except Exception as e:
                print(f'Failed to remove {file_path}: {e}')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    exec = FilesDownloader()
    sys.exit(app.exec())