# -*- coding: utf-8 -*-
import threading
import pyaudio
from .Sonic import *
from .WavFileReader import *

class WavePlayer:
    def __init__(self, sound_conf=None, **kwargs):
        if not sound_conf:
            sound_conf = Sonic()
        channels = sound_conf.channels
        sample_width = sound_conf.sample_width
        sample_frequency = sound_conf.sample_frequency

        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
            format = self.player.get_format_from_width(sample_width),
            channels = channels,
            rate = sample_frequency,
            output = True,
            **kwargs
        )

    def wave_play(self,wave_bin_data):
        if isinstance(wave_bin_data, list):
            for data in wave_bin_data:
                self.stream.write(data)
        elif not isinstance(wave_bin_data, bytes):
            raise Exception("Type of bin_data need bytes!")
        else:
            self.stream.write(wave_bin_data)

    def wave_play_async(self, wave_bin_data):
        play_thread = threading.Thread(target=self.wave_play, args=(wave_bin_data,))
        play_thread.start()

    def close(self):
        self.stream.close()
        self.player.terminate()


def wav_file_play(filename):
    audio_player = None
    chunk = 1024
    for sound in wav_file_block_read(filename, chunk):
        if not audio_player:
            audio_player = WavePlayer(sound)
        audio_player.wave_play(sound.wave_bin_data)
    else:
        if hasattr(audio_player,'close'):
            audio_player.close()

