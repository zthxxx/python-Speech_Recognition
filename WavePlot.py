# -*- coding: utf-8 -*-
import wave
import pylab
import numpy

def wave_plotting(sonic,block = False):
    #读取参数
    wave_channels = sonic.get('wave_channels')
    sample_width = sonic.get('sample_width')
    sample_frequency = sonic.get('sample_frequency')
    sample_length = sonic.get('sample_length')
    bin_data = sonic.get('bin_data')

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
    # 打开WAV文档
    wav_file = wave.open(filename, "rb")
    # 读取格式信息
    wave_parameter = wav_file.getparams()
    #声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wav非压缩，因此忽略最后两个信息
    # (wave_channels, sample_width, sample_frequency, sample_length, compress_type, compress_comment)
    wave_channels, sample_width, sample_frequency, sample_length = wave_parameter[:4]

    # readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据
    bin_data = wav_file.readframes(sample_length)
    wav_file.close()

    sonic = {
        'wave_channels':wave_channels,
        'sample_width':sample_width,
        'sample_frequency':sample_frequency,
        'sample_length':sample_length,
        'bin_data':bin_data
            }
    wave_plotting(sonic, block)



if __name__ == '__main__':
    # wav_file_plotting('wav1.wav')
    wav_file_plotting("Ring01.wav", True)
    # wav_file_plotting('wav1.wav', True)