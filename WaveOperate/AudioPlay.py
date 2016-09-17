# -*- coding: utf-8 -*-
import pyaudio
import threading
try:
    import Queue
except:
    import queue as Queue
from WaveOperate.WavFileReader import *

class WavePlayer:
    def __init__(self, sound_conf = {}):
        wave_channels = sound_conf.get('wave_channels', 1)
        sample_width = sound_conf.get('sample_width', 2)
        sample_frequency = sound_conf.get('sample_frequency', 16000)
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
                format = self.player.get_format_from_width(sample_width),
                channels = wave_channels,
                rate = sample_frequency,
                output = True
        )

    def wave_play(self,bin_data):
        if isinstance(bin_data, list):
            for data in bin_data:
                self.stream.write(data)
        elif not isinstance(bin_data, bytes):
            raise Exception("Type of bin_data need bytes!")
        else:
            self.stream.write(bin_data)

    def wave_thread_play(self, bin_data):
        play_thread = threading.Thread(target=self.wave_play, args=(bin_data,))
        play_thread.start()

    def close(self):
        self.stream.close()
        self.player.terminate()


def wav_file_play(filename):
    audio_player = None
    chunk = 1024
    for sound_conf, bin_data in wav_file_block_read(filename, chunk):
        if not audio_player:
            audio_player = WavePlayer(sound_conf)
        audio_player.wave_play(bin_data)
    else:
        if hasattr(audio_player,'close'):
            audio_player.close()


if __name__ == '__main__':
    wav_file_play('Ring01.wav')


