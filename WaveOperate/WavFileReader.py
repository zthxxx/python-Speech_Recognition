# -*- coding: utf-8 -*-
import wave
from WaveOperate.Sonic import *

def wav_file_block_read(filename, block_size=None):
    # 打开WAV文档
    wav_file = wave.open(filename, "rb")
    # 读取格式信息
    wave_parameter = wav_file.getparams()
    #声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wav非压缩，因此忽略最后两个信息
    # (wave_channels, sample_width, sample_frequency, sample_length, compress_type, compress_comment)
    wave_channels, sample_width, sample_frequency, sample_length = wave_parameter[:4]
    sonic_conf = {
        'channels':wave_channels,
        'sample_width':sample_width,
        'sample_frequency':sample_frequency
    }
    sonic = Sonic(**sonic_conf)

    # readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据
    if not block_size:
        block_size = sample_length
    wave_bin_data = wav_file.readframes(block_size)
    while wave_bin_data:
        sonic.update_wave_data(wave_bin_data, block_size)
        yield sonic
        wave_bin_data = wav_file.readframes(block_size)
    else:
        wav_file.close()

def wav_file_read(filename):
    # 打开WAV文档
    wav_file = wave.open(filename, "rb")
    # 读取格式信息
    wave_parameter = wav_file.getparams()
    #声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wav非压缩，因此忽略最后两个信息
    # (wave_channels, sample_width, sample_frequency, sample_length, compress_type, compress_comment)
    wave_channels, sample_width, sample_frequency, sample_length = wave_parameter[:4]
    # readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据
    wave_bin_data = wav_file.readframes(sample_length)
    wav_file.close()
    sonic_conf = {
        'channels':wave_channels,
        'sample_width':sample_width,
        'sample_frequency':sample_frequency,
        'sample_length':sample_length,
        'wave_bin_data' : wave_bin_data
    }
    sonic = Sonic(**sonic_conf)
    return sonic

