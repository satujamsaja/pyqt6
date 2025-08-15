from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
import numpy as np

class AudioVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.spectrum = np.zeros(32)
        self.setMinimumHeight(80)

    def update_spectrum(self, frame):
        # Compute FFT and take magnitude
        if len(frame) == 0:
            self.spectrum = np.zeros(32)
        else:
            fft = np.fft.fft(frame)
            spectrum = np.abs(fft[:len(fft)//2])
            # Downsample to 32 bars
            bins = np.array_split(spectrum, 32)
            self.spectrum = np.array([b.mean() for b in bins])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        w, h = self.width(), self.height()
        bar_w = w / len(self.spectrum)
        max_val = np.max(self.spectrum) or 1
        for i, val in enumerate(self.spectrum):
            bar_h = int((val / max_val) * (h - 10))
            painter.setBrush(QColor(15, 255, 80))
            painter.drawRect(int(i * bar_w), h - bar_h, int(bar_w) - 2, bar_h)