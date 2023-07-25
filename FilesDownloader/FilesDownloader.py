import sys
import os
import csv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QHeaderView, QProgressBar, QFileDialog, QTableWidgetItem)

from PyQt6.QtCore import Qt, QThreadPool
from FilesDownloaderThreads import DownloaderThread, DownloadClean

class FilesDownloader(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Files Downloader')
        self.setFixedWidth(1000)

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
        self.progress = 0
        self.fail = 0

        # Table
        self.download_table = QTableWidget(1, 5)
        self.download_table_header = self.download_table.horizontalHeader()
        self.download_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.download_table.setHorizontalHeaderLabels(["URL", "CHECKSUM", "PROGRESS", "STATUS", "CODE"])

        # Progress bar
        self.download_progress = QProgressBar()
        self.download_progress.setValue(0)

        # Actions button
        self.check_link_btn = QPushButton('Check File Links')
        self.check_link_btn.setDisabled(True)
        self.check_link_btn.clicked.connect(self.check_file)
        self.start_download_btn = QPushButton('Start Download')
        self.start_download_btn.setDisabled(True)
        self.start_download_btn.clicked.connect(self.start_download)
        self.save_log_btn = QPushButton('Save Log')
        self.save_log_btn.setDisabled(True)
        self.save_log_btn.clicked.connect(self.save_log)
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
                        self.download_table.setItem(index, 1, QTableWidgetItem(''))
                        self.download_table.setItem(index, 2, QTableWidgetItem(''))
                        self.download_table.setItem(index, 3, QTableWidgetItem(''))
                        self.download_table.setItem(index, 4, QTableWidgetItem(''))
                self.download_total.setText(f'Total: {self.total}')

            if self.total > 0 and self.target_dir != '':
                self.check_link_btn.setDisabled(False)
                self.start_download_btn.setDisabled(False)
                self.save_log_btn.setDisabled(False)
                self.clean_download_btn.setDisabled(False)

    def start_download(self):
        self.init_download()
        if self.total > 0:
            file_index = 0
            for row in self.data:
                url = row[0]
                checksum = row[1]
                file_name = os.path.basename(row[0])
                save_path = self.target_dir + '/' + file_name
                pool = QThreadPool.globalInstance()
                download_thread = DownloaderThread(file_index, url, save_path, checksum)
                download_thread.signals.total.connect(self.update_progress_bar)
                download_thread.signals.success.connect(self.update_success)
                download_thread.signals.fail.connect(self.update_fail)
                download_thread.signals.progress.connect(self.update_download_progress)
                download_thread.signals.checksum.connect(self.update_checksum)
                pool.start(download_thread)
                file_index += 1

    def init_download(self):
        self.success = 0
        self.fail = 0
        self.progress = 0
        self.download_progress.setValue(0)
        self.download_success.setText(f'Success: {self.success}')
        self.download_fail.setText(f'Fail: {self.fail}')
        for i in range(0, self.total):
            item_progress = QTableWidgetItem('0%')
            item_progress.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.download_table.setItem(i, 1, QTableWidgetItem(''))
            self.download_table.setItem(i, 2, item_progress)
            self.download_table.setItem(i, 3, QTableWidgetItem(''))
            self.download_table.setItem(i, 4, QTableWidgetItem(''))

    def update_progress_bar(self):
        self.progress += 1
        progress = int((self.progress / self.total) * 100)
        self.download_progress.setValue(progress)
    def update_success(self, file_index, status_code):
        self.success += 1
        self.download_success.setText(f'Success: { self.success }')
        item_success = QTableWidgetItem('OK')
        item_success.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 3, item_success)
        item_success_code = QTableWidgetItem(f'{status_code}')
        item_success_code.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 4, item_success_code)

    def update_fail(self, file_index, status_code):
        self.fail += 1
        self.download_fail.setText(f'Fail: {self.fail}')
        item_fail = QTableWidgetItem('FAIL')
        item_fail.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 3, item_fail)
        item_fail_code = QTableWidgetItem(f'{status_code}')
        item_fail_code.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 4, item_fail_code)

    def update_download_progress(self, file_index, progress):
        item_progress = QTableWidgetItem('{}%'.format(progress))
        item_progress.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 2, item_progress)

    def update_checksum(self, file_index, valid):
        item_checksum = QTableWidgetItem('{}'.format('Valid' if valid else 'Invalid'))
        item_checksum.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 1, item_checksum)

    def check_file(self):
        self.init_download()
        if self.total > 0:
            file_index = 0
            for row in self.data:
                url = row[0]
                checksum = row[1]
                file_name = os.path.basename(row[0])
                save_path = self.target_dir + '/' + file_name
                pool = QThreadPool.globalInstance()
                download_thread = DownloaderThread(file_index, url, save_path, checksum, True)
                download_thread.signals.total.connect(self.update_progress_bar)
                download_thread.signals.success.connect(self.update_success)
                download_thread.signals.fail.connect(self.update_fail)
                download_thread.signals.progress.connect(self.update_download_progress)
                pool.start(download_thread)
                file_index += 1

    def clean_download(self):
        self.init_download()
        if self.total > 0:
            file_index = 0
            for row in self.data:
                file_name = os.path.basename(row[0])
                save_path = self.target_dir + '/' + file_name
                pool = QThreadPool.globalInstance()
                clean_download_thread = DownloadClean(file_index, save_path)
                clean_download_thread.signals.deleted.connect(self.update_clean_download)
                clean_download_thread.signals.total.connect(self.update_progress_bar)
                pool.start(clean_download_thread)
                file_index += 1

    def update_clean_download(self, file_index, deleted):
        item_deleted = QTableWidgetItem(deleted)
        item_deleted.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.download_table.setItem(file_index, 3, item_deleted)

    def save_log(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)")

        if file_name:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                header_csv = [self.download_table.horizontalHeaderItem(col).text().lower() for col in range(self.download_table.columnCount())]
                writer.writerow(header_csv)

                for row in range(self.download_table.rowCount()):
                    row_data = [self.download_table.item(row, col).text() for col in range(self.download_table.columnCount())]
                    writer.writerow(row_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exec = FilesDownloader()
    sys.exit(app.exec())
