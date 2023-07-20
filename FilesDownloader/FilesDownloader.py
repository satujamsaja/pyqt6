import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QHeaderView, QProgressBar)


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
        self.directory_browse = QPushButton('Browse directory target')
        self.directory_browse.setFixedHeight(50)

        # Hold file path and folder path
        self.file_list = ''
        self.target_dir = ''

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
        self.start_download_btn = QPushButton('Start/Stop Download')
        self.save_log_btn = QPushButton('Save Log')
        self.clean_download_btn = QPushButton('Clean Download')

        # Report Label
        self.download_total = QLabel('Total:')
        self.download_success = QLabel('Success:')
        self.download_fail = QLabel('Fail:')

        # Flag
        self.download_start = False

        # Load ui
        self.init_ui()
        print('aaa')

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    exec = FilesDownloader()
    sys.exit(app.exec())