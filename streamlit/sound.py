#https://github.com/ayushkumarshah/Guitar-Chords-recognition/blob/master/app.py
import logging
import pyaudio, wave, pylab
import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt
# from pygame import mixer
from scipy.io.wavfile import write


INPUT_DEVICE = 0
MAX_INPUT_CHANNELS = 1  # Max input channels
DEFAULT_SAMPLE_RATE = 44100   # Default sample rate of microphone or recording device
DURATION = 3   # 3 seconds
CHUNK_SIZE = 1024
WAVE_OUTPUT_FILE="recorded.wav"




class Sound(object):
    def __init__(self):
        # Set default configurations for recording device
        # sd.default.samplerate = DEFAULT_SAMPLE_RATE
        # sd.default.channels = DEFAULT_CHANNELS
        self.format = pyaudio.paInt16
        self.channels = MAX_INPUT_CHANNELS
        self.sample_rate = DEFAULT_SAMPLE_RATE
        self.chunk = CHUNK_SIZE
        self.duration = DURATION
        self.path = WAVE_OUTPUT_FILE
        self.device = INPUT_DEVICE
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.device_info()


    def device_info(self):
        num_devices = self.audio.get_device_count()
        keys = ['name', 'index', 'maxInputChannels', 'defaultSampleRate']

        for i in range(num_devices):
            info_dict = self.audio.get_device_info_by_index(i)

    def record(self):
        # start Recording
        self.audio = pyaudio.PyAudio()
        stream = self.audio.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        input_device_index=self.device)
        self.frames = []
        for i in range(0, int(self.sample_rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            self.frames.append(data)
        # stop Recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.save()

    def save(self):
        waveFile = wave.open(self.path, 'wb')
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.audio.get_sample_size(self.format))
        waveFile.setframerate(self.sample_rate)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()


sound = Sound()

