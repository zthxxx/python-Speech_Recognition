# -*- coding: utf-8 -*-
import logging
import threading
from datetime import datetime
try:
    import queue
except:
    import Queue as queue
import pyaudio
import numpy
from .Sonic import *


class RecordConf:
    def __init__(self, gate_value=700, series_min_count=30, block_min_count=8, record_max_second=10, speech_filter=None):
        self.gate_value = gate_value                #采样量化值静音判定门限
        self.series_min_count = series_min_count    #块序列采样波能量判定点数
        self.block_min_count = block_min_count      #有效块记录最小个数
        self.record_max_second = record_max_second  #录音最大时间秒数
        self.speech_filter = speech_filter

class AudioRecorder:
    def __init__(self, sonic=None, block_size=None, **kwargs):
        if not sonic:
            sonic = Sonic()
        self.sonic = sonic
        self.channels = sonic.channels     #声道数
        self.sample_width = sonic.sample_width     #量化宽度(byte)
        self.sample_frequency = sonic.sample_frequency #采样频率
        if block_size:
            self.block_size = block_size  #wave录音块与缓冲大小
        else:
            self.block_size = sonic.sample_length  #wave录音块与缓冲大小
        self.wave_buffer = list()#录音保存块
        self.record_cache = queue.Queue()
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
            format = self.player.get_format_from_width(self.sample_width),
            channels = self.channels,
            rate = self.sample_frequency,
            frames_per_buffer = self.block_size,
            input = True,
            **kwargs
        )

    def save_wave_file(self, filename, wave_buffer=None):
        if not wave_buffer:
            wave_buffer = self.wave_buffer
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sample_width)
        wf.setframerate(self.sample_frequency)
        if isinstance(wave_buffer, list):
            for data_block in wave_buffer:
                wf.writeframes(data_block)
        elif not isinstance(wave_buffer, bytes):
            raise Exception("Type of bin_data need bytes!")
        else:
            wf.writeframes(wave_buffer)
        wf.close()

    def record_realtime(self, speech_filter=None):
        def record_async(self):
            while True:
                bin_audio_data = self.stream.read(self.block_size)
                self.record_cache.put(bin_audio_data)

        record_thread = threading.Thread(target=record_async, args=(self,))
        record_thread.setDaemon(True)
        record_thread.start()
        half_block_size = self.block_size // 2
        bin_audio_data = self.record_cache.get()
        last_data = bin_audio_data[-self.block_size:]
        while True:
            bin_audio_data = self.record_cache.get()
            if speech_filter:
                audio_data = numpy.fromstring(last_data + bin_audio_data, dtype=number_type.get(self.sample_width))
                audio_data = speech_filter(audio_data)
                audio_data = audio_data[half_block_size:]
                audio_data = number_type.get(self.sample_width)(audio_data)
                last_data = bin_audio_data[-self.block_size:]
                bin_audio_data = bytes(audio_data)
            yield bin_audio_data

    def record_speech(self, record_conf):
        squeak_min_count = 4
        last_audio_data = bytes()   #上一个数据包
        block_inverse_count = 0     #当前录音块离结束的距离
        for bin_audio_data in self.record_realtime(record_conf.speech_filter):
            audio_data = numpy.fromstring(bin_audio_data, dtype=number_type.get(self.sample_width))
            large_threshold_count = numpy.sum(audio_data > record_conf.gate_value)#超过阈值的点的个数
            logging.debug((large_threshold_count, numpy.max(audio_data)))
            if large_threshold_count > record_conf.series_min_count:
                block_inverse_count = record_conf.block_min_count
            if block_inverse_count > 0:
                block_inverse_count -= 1
                self.wave_buffer.append(last_audio_data)
                if len(self.wave_buffer) >= record_conf.record_max_second * self.sample_frequency / self.block_size \
                or block_inverse_count == 0:
                    if len(self.wave_buffer) - record_conf.block_min_count < squeak_min_count:
                        self.wave_buffer = list()
                        continue
                    del self.wave_buffer[-4:]   #去掉结尾部分的一些空音
                    self.sonic.update_wave_data(self.wave_buffer, len(self.wave_buffer) * self.block_size)
                    yield self.sonic
                    self.wave_buffer = list()
            last_audio_data = bin_audio_data

    def record_speech_wav(self, record_conf, filename=None):
        if not filename:
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
        self.record_speech(record_conf).__next__()
        self.save_wave_file(filename)
        print(filename, "saved")
