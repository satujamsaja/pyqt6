from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QFileDialog, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QIcon
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import pygame

class AudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Player")
        self.setGeometry(100, 100, 555, 600)
        # Define open audio file button
        self.open_button = QPushButton("Open Audio File")
        # Define playlist and current track
        self.playlist = QTableWidget(1, 4)
        # Define track progress bar
        self.track_progress = QProgressBar()
        self.track_progress.setMinimum(0)
        self.track_progress.setMaximum(100)
        # Define buttons control
        button_style = """
        QPushButton {
            background: transparent;
            border: none;
            padding: 0px;
        }
        """
        icon_size = QSize(48, 48)
        self.prev_button = QPushButton("Previous")
        self.prev_button.setIcon(QIcon("images/previous.png"))
        self.prev_button.setText('')
        self.prev_button.setStyleSheet(button_style)
        self.prev_button.setIconSize(icon_size)
        self.play_pause_button = QPushButton("Play/Pause")
        self.play_pause_button.setIcon(QIcon("images/play.png"))
        self.play_pause_button.setStyleSheet(button_style)
        self.play_pause_button.setIconSize(icon_size)
        self.play_pause_button.setText('')
        self.next_button = QPushButton("Next")
        self.next_button.setIcon(QIcon("images/next.png"))
        self.next_button.setText('')
        self.next_button.setStyleSheet(button_style)
        self.next_button.setIconSize(icon_size)

        # Define volume control
        self.volume_slider = QSlider()

        # Connect buttons to actions
        self.open_button.clicked.connect(self.open_audio_file)
        self.prev_button.clicked.connect(self.previous_track)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.next_button.clicked.connect(self.next_track)

        # Connect volume slider to a method (placeholder)
        self.volume_slider.valueChanged.connect(self.adjust_volume)

        # Load ui
        self.init_ui()

        # Load player settings
        self.init_player()

    def init_ui(self):
        # Section for layout
        file_section = QGroupBox('File')
        playlist_section = QGroupBox('Playlist')
        control_section = QGroupBox('Audio Controls')
        track_progess_section = QGroupBox('Track Progress')
        volume_section = QGroupBox('Volume Control')

        # Set layout for file section
        file_layout = QVBoxLayout()
        file_layout.addWidget(self.open_button)
        file_section.setLayout(file_layout)

        # Set layout for playlist section
        playlist_layout = QVBoxLayout()
        playlist_layout.addWidget(self.playlist)
        playlist_section.setLayout(playlist_layout)

        # Set layout for control section
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.play_pause_button)
        control_layout.addWidget(self.next_button)
        control_section.setLayout(control_layout)

        # Set layout for track progress section
        track_progress_layout = QVBoxLayout()
        track_progress_layout.addWidget(self.track_progress)
        track_progess_section.setLayout(track_progress_layout)


        # Set layout for volume section
        volume_layout = QVBoxLayout()
        volume_layout.addWidget(self.volume_slider)
        volume_section.setLayout(volume_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(file_section)
        main_layout.addWidget(playlist_section)
        main_layout.addWidget(control_section)
        main_layout.addWidget(track_progess_section)
        main_layout.addWidget(volume_section)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.show()

    def init_player(self):
        # Set initial state
        self.playlist.setColumnCount(6)
        self.log_table_header = self.playlist.horizontalHeader()
        self.playlist.setHorizontalHeaderLabels(["Path", "Track", "Artist", "Album", "Duration", "Bitrate"])
        self.playlist.setRowCount(0)
        self.volume_slider.setOrientation(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)

        # Init pygame mixer
        pygame.mixer.init()
        self.volume_slider.setValue(50)
        self.adjust_volume(50)

        # Initialize playlist settings
        self.playlist.cellDoubleClicked.connect(self.play_track)
        self.playlist.hideColumn(0)
        self.playlist.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.playlist.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.playlist.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Initialize track progress bar timer
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_track_progress)
        self.current_track_length = 0
        self.is_paused = False


    def open_audio_file(self):
        # Open file dialog to select an audio file
        file_filter = "Audio Files (*.mp3)"
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Audio File", "", file_filter)
        for file_path in file_paths:
            self.add_to_playlist(file_path)

    def previous_track(self):
        row_count = self.playlist.rowCount()
        current_row = self.playlist.currentRow()
        if row_count == 0:
            return
        prev_row = (current_row - 1) % row_count
        self.playlist.selectRow(prev_row)
        self.play_track(prev_row, 0)

    def toggle_play_pause(self):
        if pygame.mixer.music.get_busy():
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.play_pause_button.setIcon(QIcon('images/pause.png'))
                self.timer.start()
            else:
                pygame.mixer.music.pause()
                self.play_pause_button.setIcon(QIcon('images/play.png'))
                self.timer.stop()
            self.is_paused = not self.is_paused
        else:
            current_row = self.playlist.currentRow()
            if current_row >= 0:
                self.play_track(current_row, 0)
            else:
                print("No track selected to play")

    def next_track(self):
        row_count = self.playlist.rowCount()
        current_row = self.playlist.currentRow()
        if row_count == 0:
            return
        next_row = (current_row + 1) % row_count
        self.playlist.selectRow(next_row)
        self.play_track(next_row, 0)

    def adjust_volume(self, value):
        volume = value / 100.0
        pygame.mixer.music.set_volume(volume)

    def add_to_playlist(self, file_path):
        audio_info = {}
        tag_info = {}
        # Get audio information using mutagen
        try:
            audio = MP3(file_path, ID3=ID3)
            # Convert length (seconds) to mm:ss format
            length_sec = int(audio.info.length or 0)
            length_str = f"{length_sec // 60}:{length_sec % 60:02d}"

            # Convert bitrate (bps) to kbps
            bitrate_bps = int(audio.info.bitrate or 0)
            bitrate_kbps = f"{bitrate_bps // 1000} kbps"

            audio_info = {
                'length': length_str,
                'bitrate': bitrate_kbps,
            }
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return
        # Get id3 tags if available
        try:
            audio_tags = ID3(file_path)
            tag_info = {
                'title': audio_tags.get('TIT2').text[0] if audio_tags.get('TIT2') else 'Unknown Title',
                'artist': audio_tags.get('TPE1').text[0] if audio_tags.get('TPE1') else 'Unknown Artist',
                'album': audio_tags.get('TALB').text[0] if audio_tags.get('TALB') else 'Unknown Album',
            }
        except Exception as e:
            print(f"Error reading ID3 tags: {e}")

        # Add the selected file to the playlist
        row_position = self.playlist.rowCount()
        self.playlist.insertRow(row_position)
        self.playlist.setItem(row_position, 0, QTableWidgetItem(file_path))
        self.playlist.setItem(row_position, 1, QTableWidgetItem(tag_info['title']))
        self.playlist.setItem(row_position, 2, QTableWidgetItem(tag_info['artist']))
        self.playlist.setItem(row_position, 3, QTableWidgetItem(tag_info['album']))
        self.playlist.setItem(row_position, 4, QTableWidgetItem(audio_info['length']))
        self.playlist.setItem(row_position, 5, QTableWidgetItem(audio_info['bitrate']))

    def play_track(self, row, column):
        track_path = self.playlist.item(row, 0).text()
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.play_pause_button.setIcon(QIcon('images/pause.png'))
        # Reset track progress bar
        try:
            audio = MP3(track_path, ID3=ID3)
            self.current_track_length = int(audio.info.length)
            self.track_progress.setMaximum(self.current_track_length)
            self.track_progress.setValue(0)
            self.timer.start()
        except Exception as e:
            self.current_track_length = 0
            self.track_progress.setMaximum(0)
            self.track_progress.setValue(0)
            print(f"Error loading track: {e}")

    def update_track_progress(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms == -1:
            self.timer.stop()
            self.track_progress.setValue(self.current_track_length)
            # Play next track automatically
            self.next_track()
            return
        pos_sec = pos_ms // 1000
        self.track_progress.setValue(pos_sec)

if __name__ == "__main__":
    app = QApplication([])
    window = AudioPlayer()
    window.show()
    app.exec()
