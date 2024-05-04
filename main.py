import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from audio_player import AudioPlayer
import numpy as np

class AudioFilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.audioPlayer = AudioPlayer(self.update_plots)
        self.initUI()
        self.init_plots()

    def initUI(self):
        self.setWindowTitle('Audio Filter Application')
        self.layout = QVBoxLayout()

        self.btnLoad = QPushButton('Load Audio', self)
        self.btnLoad.clicked.connect(self.load_audio)
        self.layout.addWidget(self.btnLoad)

        self.btnPlayOriginal = QPushButton('Play Original Audio', self)
        self.btnPlayOriginal.clicked.connect(self.audioPlayer.playOriginalAudio)
        self.layout.addWidget(self.btnPlayOriginal)

        self.btnPlayFiltered = QPushButton('Play Filtered Audio', self)
        self.btnPlayFiltered.clicked.connect(self.audioPlayer.playFilteredAudio)
        self.layout.addWidget(self.btnPlayFiltered)

        self.btnStop = QPushButton('Stop Audio', self)
        self.btnStop.clicked.connect(self.audioPlayer.stopAudio)
        self.layout.addWidget(self.btnStop)

        self.canvas = FigureCanvas(Figure(figsize=(10, 8)))
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def init_plots(self):
        self.ax1 = self.canvas.figure.add_subplot(221)
        self.ax2 = self.canvas.figure.add_subplot(222)
        self.ax3 = self.canvas.figure.add_subplot(223)
        self.ax4 = self.canvas.figure.add_subplot(224)
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    def update_plots(self, data, filtered_data, samplerate):
        self.ax1.cla()
        self.ax1.plot(data, label="Original")
        self.ax1.set_title('Time Domain - Original')
        self.ax1.set_xlabel('Samples')
        self.ax1.set_ylabel('Amplitude')

        self.ax2.cla()
        self.ax2.plot(filtered_data, label="Filtered")
        self.ax2.set_title('Time Domain - Filtered')
        self.ax2.set_xlabel('Samples')
        self.ax2.set_ylabel('Amplitude')

        freq = np.fft.fftfreq(len(data), 1/samplerate)
        magnitude = np.abs(np.fft.fft(data))
        self.ax3.cla()
        self.ax3.plot(freq[:len(freq)//2], magnitude[:len(magnitude)//2])
        self.ax3.set_title('Frequency Domain - Original')
        self.ax3.set_xlabel('Frequency (Hz)')
        self.ax3.set_ylabel('Magnitude')

        freq_filtered = np.fft.fftfreq(len(filtered_data), 1/samplerate)
        magnitude_filtered = np.abs(np.fft.fft(filtered_data))
        self.ax4.cla()
        self.ax4.plot(freq_filtered[:len(freq_filtered)//2], magnitude_filtered[:len(magnitude_filtered)//2])
        self.ax4.set_title('Frequency Domain - Filtered')
        self.ax4.set_xlabel('Frequency (Hz)')
        self.ax4.set_ylabel('Magnitude')

        self.canvas.draw()

    def load_audio(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load WAV File", "", "Wave Files (*.wav)")
        if filepath:
            self.audioPlayer.loadAudio(filepath)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AudioFilterApp()
    ex.show()
    sys.exit(app.exec_())
