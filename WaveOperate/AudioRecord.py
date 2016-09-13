# -*- coding: utf-8 -*-
from datetime import datetime
import pyaudio
import numpy
import wave
from WaveOperate.WavePlot import *
from WaveOperate.AudioPlay import *
import logging

class AudioRecorder:
    def __init__(self, sonic_conf = dict()):
        self.wave_channels = sonic_conf.get('wave_channels', 1) #声道数
        self.sample_width = sonic_conf.get('sample_width', 2)   #量化宽度(byte)
        self.sample_frequency = sonic_conf.get('sample_frequency', 16000)#采样频率
        self.block_size = sonic_conf.get('block_size', 2000)#wave录音块与缓冲大小
        self.wave_buffer = list()#录音保存块
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
                format = self.player.get_format_from_width(self.sample_width),
                channels = self.wave_channels,
                rate = self.sample_frequency,
                frames_per_buffer = self.block_size,
                input = True
        )

    def save_wave_file(self, filename, wave_buffer = None):
        if not wave_buffer:
            wave_buffer = self.wave_buffer
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.wave_channels)
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

    def recording(self, record_conf, record_max_second = 10):
        threshold_value = record_conf.get('threshold_value', 700)   #判断开始结束量化声音大小的阈值
        series_min_count = record_conf.get('series_min_count', 30)  #判定开始的序列中大于阈值的点的最小数目
        block_min_count = record_conf.get('block_min_count', 8)     #做为最小时间和块间延时的大小
        squeak_min_count = 4
        last_audio_data = bytes()   #上一个数据包
        block_inverse_count = 0     #当前录音块离结束的距离

        while True:
            string_audio_data = self.stream.read(self.block_size)
            number_type = {1: numpy.int8, 2: numpy.int16, 3: numpy.int32}
            audio_data = numpy.fromstring(string_audio_data, dtype=number_type.get(self.sample_width))
            large_threshold_count = numpy.sum(audio_data > threshold_value)#超过阈值的点的个数
            logging.debug((large_threshold_count, numpy.max(audio_data)))
            if large_threshold_count > series_min_count:
                block_inverse_count = block_min_count
            if block_inverse_count > 0:
                block_inverse_count -= 1
                self.wave_buffer.append(last_audio_data)
                if len(self.wave_buffer) >= record_max_second * self.sample_frequency / self.block_size \
                or block_inverse_count == 0:
                    if len(self.wave_buffer) - block_min_count < squeak_min_count:
                        self.wave_buffer = list()
                        continue
                    del self.wave_buffer[-4:]   #去掉结尾部分的一些空音
                    sonic = {
                        'wave_channels':self.wave_channels,
                        'sample_width':self.sample_width,
                        'sample_frequency':self.sample_frequency,
                        'bin_data':self.wave_buffer,
                        'sample_length':len(self.wave_buffer) * self.block_size
                    }
                    yield sonic
                    self.wave_buffer = list()
            last_audio_data = string_audio_data

    def record_wav(self, record_conf, filename = None, **kwargs):
        if not filename:
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".wav"
        self.recording(record_conf, **kwargs).__next__()
        self.save_wave_file(filename)
        print(filename, "saved")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sonic_conf = {
        'wave_channels':1,
        'sample_width':2,
        'sample_frequency':16000,
        'block_size':2000
    }
    wave_player = WavePlayer(sonic_conf)
    recorder = AudioRecorder(sonic_conf)
    record_conf = {
        'threshold_value':700,
        'series_min_count':30,
        'block_min_count':8
    }
    # recorder.record_wav(record_conf)
    recording = recorder.recording(record_conf)
    for sonic in recording:
        audio_data = sonic.get('bin_data')
        # recorder.save_wave_file(datetime.now().strftime("%Y%m%d%H%M%S") + ".wav", wave_data)
        wave_player.wave_play(audio_data)
        # wave_plotting(sonic,True)
    print("OK!")



