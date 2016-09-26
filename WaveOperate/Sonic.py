# -*- coding: utf-8 -*-
import wave

class Sonic:
    def __init__(self, channels=1, sample_width=2, sample_frequency=16000, sample_length=0, wave_bin_data=None):
        self.channels = channels                #声道数
        self.sample_width = sample_width        #采样字节宽度
        self.sample_frequency = sample_frequency#采样频率
        self.sample_length = sample_length      #采样长度点数
        self.wave_bin_data = wave_bin_data      #采样二进制数据

    def update_wave_data(self, wave_bin_data, sample_length=0):
        if wave_bin_data and not sample_length:
            sample_length = len(wave_bin_data) / self.sample_width
        self.wave_bin_data = wave_bin_data
        self.sample_length = sample_length

