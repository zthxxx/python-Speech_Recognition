# -*- coding: utf-8 -*-
import pyaudio
import wave


class WavePlayer:
    def __init__(self, sound_conf):
        wave_channels = sound_conf.get('wave_channels')
        sample_width = sound_conf.get('sample_width')
        sample_frequency = sound_conf.get('sample_frequency')
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
                format = self.player.get_format_from_width(sample_width),
                channels = wave_channels,
                rate = sample_frequency,
                output = True
        )

    def wave_play(self,bin_data):
        self.stream.write(bin_data)

    def close(self):
        self.stream.close()
        self.player.terminate()


def wav_file_play(filename):
    # 打开WAV文档
    wav_file = wave.open(filename, "rb")
    # 读取格式信息
    wave_parameter = wav_file.getparams()
    #声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wav非压缩，因此忽略最后两个信息
    # (wave_channels, sample_width, sample_frequency, sample_length, compress_type, compress_comment)
    wave_channels, sample_width, sample_frequency, sample_length = wave_parameter[:4]
    sound_conf = {
            'wave_channels':wave_channels,
            'sample_width':sample_width,
            'sample_frequency':sample_frequency
    }
    player = WavePlayer(sound_conf)

    # readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据
    chunk = 1024
    while True:
        bin_data = wav_file.readframes(chunk)
        if bin_data == "": break
        player.wave_play(bin_data)
    player.close()
    wav_file.close()


if __name__ == '__main__':
    wav_file_play('Ring01.wav')


