# -*- coding: utf-8 -*-
import wave
import pylab
import numpy
from WaveOperate.WavFileReader import *


def wave_plotting(sonic,block = False):
    #读取参数
    wave_channels = sonic.get('wave_channels')
    sample_width = sonic.get('sample_width')
    sample_frequency = sonic.get('sample_frequency')
    sample_length = sonic.get('sample_length')
    bin_data = sonic.get('bin_data')

    if isinstance(bin_data, list):
        bin_buffer = bytearray()
        for data in bin_data:
            bin_buffer.extend(data)
        bin_data = bytes(bin_buffer)
    elif not isinstance(bin_data, bytes):
        raise Exception("Type of bin_data need bytes!")

    #接下来需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组
    number_type = {1: numpy.int8, 2: numpy.int16, 3: numpy.int32}
    wave_data = numpy.fromstring(bin_data, dtype=number_type.get(sample_width))
    #现在我们得到的wave_data是一个一维的short类型的数组，但是因为我们的声音文件是双声道的，
    # 因此它由左右两个声道的取样交替构成：LRLRLRLR....LR（L表示左声道的取样值，R表示右声道取样值）。修改wave_data的sharp
    wave_data.shape = (sample_length, wave_channels)
    wave_data = wave_data.T
    time = numpy.arange(0, sample_length) * (1.0 / sample_frequency)

    # 绘制波形
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    pylab.figure()
    for index in range(0, wave_channels):
        pylab.subplot(wave_channels, 1, index + 1)
        pylab.plot(time, wave_data[index], colors[index % len(colors)])
    pylab.ylabel("quantization")
    pylab.xlabel("time (seconds)")
    pylab.ion()
    if block:
        pylab.ioff()
    pylab.show()


def wav_file_plotting(filename,block = False):
    sonic = wav_file_read(filename)
    wave_plotting(sonic, block)


if __name__ == '__main__':
    # wav_file_plotting('wav1.wav')
    wav_file_plotting("Ring01.wav", True)