# -*- coding: utf-8 -*-
import logging
from WaveOperate.WavePlot import *
from WaveOperate.WaveFilter import *
from WaveOperate.WaveRealtimePlot import *


sonic_conf = {
    'channels':1,
    'sample_width':2,
    'sample_frequency':16000,
    'sample_length':2048
}
sonic_conf = Sonic(**sonic_conf)

def wav_file_plot_pretest():
    logging.warning("Test wav file plot start ...")
    wav_file_plotting('WaveOperate/ding.wav')
    wav_file_plotting("WaveOperate/Ring01.wav", block=True)
    logging.warning("Test wav file plot OK")

def speech_wave_plot_pretest(speech_filter=None):
    logging.warning("Test speech input realtime plot start ...")
    recorder = AudioRecorder(sonic_conf)
    recording = recorder.record_realtime(speech_filter)
    def data_generator():
        for bin_audio_data in recording:
            audio_data = numpy.fromstring(bin_audio_data, dtype=number_type.get(sonic_conf.sample_width))
            fft_data = numpy.abs(numpy.fft.rfft(audio_data) * 2 / sonic_conf.sample_length)
            yield numpy.array(audio_data), numpy.array(fft_data)
    bit_deep = 2 ** (8 * sonic_conf.sample_width - 1)
    sonic_curve_conf = {
        'axis_lim' : [0, sonic_conf.sample_length, -bit_deep, bit_deep],
        'axes_x' : list(range(0,sonic_conf.sample_length)),
        'axes_y' : [0] * sonic_conf.sample_length
    }
    fft_curve_conf = {
        'axis_lim' : [0, sonic_conf.sample_frequency // 2 + 1, 0, 3000],
        'axes_x' : [
            (i - 1) * sonic_conf.sample_frequency / sonic_conf.sample_length
            for i in range(0,sonic_conf.sample_length // 2 + 1)
        ],
        'axes_y' : [0] * (sonic_conf.sample_length // 2 + 1)
    }
    lines_conf = [RealtimeLine(**sonic_curve_conf), RealtimeLine(**fft_curve_conf)]
    realtime_plot(lines_conf, data_generator)
    logging.warning("Test speech input realtime plot OK")

def speech_wave_filter_pretest():
    bandpass_filter = butter_bandpass(150, 2000, sonic_conf.sample_frequency)
    speech_wave_plot_pretest(bandpass_filter)


if __name__ == '__main__':

    # wav_file_plot_pretest()

    # speech_wave_plot_pretest()

    speech_wave_filter_pretest()
