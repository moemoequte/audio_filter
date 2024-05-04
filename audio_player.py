from scipy.signal import firwin, lfilter
import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import audio_filters as af

class AudioPlayer:
    def __init__(self, plot_callback):
        self.plot_callback = plot_callback
        self.stream = None

    def loadAudio(self, filepath):
        self.samplerate, self.data = wavfile.read(filepath)
        self.data = self.data.astype(np.float32) / np.max(np.abs(self.data))
        
        # 根据文件名中的关键词选择滤波器类型
        if 'Hnoise.wav' in filepath:
            self.filtered_data = af.apply_lowpass_filter(self.data, self.samplerate)
        elif 'Lnoise.wav' in filepath:
            self.filtered_data = af.apply_highpass_filter(self.data, self.samplerate)
        elif 'Snoise.wav' in filepath:
            self.filtered_data = af.apply_bandpass_filter(self.data, self.samplerate)
        elif 'Mnoise.wav' in filepath:
            self.filtered_data = af.apply_bandstop_filter(self.data, self.samplerate)
        
        self.update_plots()

    def playOriginalAudio(self):
        if hasattr(self, 'data'):
            sd.stop()  # Stop any currently playing streams
            sd.play(self.data, self.samplerate)

    def playFilteredAudio(self):
        if hasattr(self, 'filtered_data'):
            sd.stop()  # Stop any currently playing streams
            sd.play(self.filtered_data, self.samplerate)

    def stopAudio(self):
        sd.stop()

    def update_plots(self):
        if hasattr(self, 'data') and hasattr(self, 'filtered_data'):
            self.plot_callback(self.data, self.filtered_data, self.samplerate)

