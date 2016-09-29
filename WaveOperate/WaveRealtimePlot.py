# -*- coding: utf-8 -*-
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from WaveOperate.AudioRecord import *


class RealtimeLine:
    def __init__(self, axis_lim, axes_x, axes_y):
        self.axis_lim = axis_lim    #坐标轴上下限 [xmin, xmax, ymin, ymax]
        self.axes_x = axes_x        #x轴坐标显示数值组
        self.axes_y = axes_y        #y轴坐标显示数值组

def realtime_plot(lines_conf, data_generator=None):
    fig = plt.figure()
    lines = []
    if not isinstance(lines_conf, list):
        lines_conf = [lines_conf]
    for index, line_conf in enumerate(lines_conf):
        axes = fig.add_subplot(len(lines_conf), 1, index + 1)
        axes.axis(line_conf.axis_lim)
        line = axes.plot(line_conf.axes_x, line_conf.axes_y)[0]
        lines.append(line)

    def update(lines_data):
        if len(lines) <= 1 and not isinstance(lines_data, list):
            lines_data = [lines_data]
        for index, line in enumerate(lines):
            line.set_ydata(lines_data[index])
        return lines

    ani = animation.FuncAnimation(fig, update, frames=data_generator, interval=20)
    plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sonic_conf = {
        'channels':1,
        'sample_width':2,
        'sample_frequency':16000,
        'sample_length':2048
    }
    sonic_conf = Sonic(**sonic_conf)
    recorder = AudioRecorder(sonic_conf)
    bandpass_filter = butter_bandpass_filter(150, 2000, sonic_conf.sample_frequency)
    recording = recorder.record_realtime(bandpass_filter)
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
    print('OK')