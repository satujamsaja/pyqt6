import os
import requests
import requests.exceptions
import hashlib
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

class DownLoaderSignal(QObject):
    fail = pyqtSignal(int, int)
    success = pyqtSignal(int, int)
    progress = pyqtSignal(int, int)
    total = pyqtSignal()
    checksum = pyqtSignal(int, bool)

class CleanSignal(QObject):
    deleted = pyqtSignal(int, str)
    total = pyqtSignal()

class DownloaderThread(QRunnable):
    def __init__(self, file_index, url, save_path, checksum, check_link=False):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.signals = DownLoaderSignal()
        self.file_index = file_index
        self.checksum = checksum
        self.check_link = check_link

    def run(self):
        response = requests.get(self.url, stream=True)
        if response.status_code == 200:
            if not self.check_link:
                total_length = int(response.headers.get('content-length'))
                bytes_downloaded = 0
                with open(self.save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        progress = int((bytes_downloaded / total_length) * 100)
                        self.signals.progress.emit(self.file_index, progress)
                        if progress == 100:
                            self.signals.success.emit(self.file_index, response.status_code)

                if len(self.checksum) > 0:
                    md5_sum = hashlib.md5()
                    with open(self.save_path, "rb") as f:
                        # Read the file in chunks to handle large files efficiently
                        while chunk := f.read(8192):
                            md5_sum.update(chunk)
                    if self.checksum == md5_sum.hexdigest():
                        self.signals.checksum.emit(self.file_index, True)
                    else:
                        self.signals.checksum.emit(self.file_index, False)
            else:
                self.signals.success.emit(self.file_index, response.status_code)
        else:
            self.signals.fail.emit(self.file_index, response.status_code)
            self.signals.checksum.emit(self.file_index, False)

        self.signals.total.emit()

class DownloadClean(QRunnable):
    def __init__(self, file_index, save_path):
        super().__init__()
        self.file_index = file_index
        self.save_path = save_path
        self.signals = CleanSignal()

    def run(self):
        try:
            os.remove(self.save_path)
            self.signals.deleted.emit(self.file_index, 'Deleted')
        except FileNotFoundError:
            self.signals.deleted.emit(self.file_index, 'File Not Found')
        except PermissionError:
            self.signals.deleted.emit(self.file_index, 'Permission Error')
        except Exception as e:
            self.signals.deleted.emit(self.file_index, 'Unknown Error')

        self.signals.total.emit()