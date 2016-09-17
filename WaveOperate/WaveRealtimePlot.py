# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import logging
from WaveOperate.AudioRecord import *



def realtime_plot(lines_conf, data_generator = None):
    fig = plt.figure()
    lines = []
    if not isinstance(lines_conf, list):
        lines_conf = [lines_conf]
    for index, line_conf in enumerate(lines_conf):
        axes = fig.add_subplot(len(lines_conf), 1, index + 1)
        axes.axis(line_conf['axis_lim'])
        line = axes.plot(line_conf['axes_x'], line_conf['axes_y'])[0]
        lines.append(line)

    def update(lines_data):
        if len(lines) <= 1 and not isinstance(lines_data, list):
            lines_data = [lines_data]
        for index, line in enumerate(lines):
            line.set_ydata(lines_data[index])
        return lines

    ani = animation.FuncAnimation(fig, update, frames = data_generator, interval = 20)
    plt.show()




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sonic_conf = {
        'wave_channels':1,
        'sample_width':2,
        'sample_frequency':16000,
        'block_size':2048
    }
    recorder = AudioRecorder(sonic_conf)
    recording = recorder.record_realtime()

    def data_generator():
        number_type = {1: numpy.int8, 2: numpy.int16, 3: numpy.int32}
        for bin_audio_data in recording:
            audio_data = numpy.fromstring(bin_audio_data, dtype=number_type.get(sonic_conf['sample_width']))
            fft_data = numpy.abs(numpy.fft.rfft(audio_data) * 2 / sonic_conf['block_size'])
            yield np.array(audio_data), np.array(fft_data)

    bit_deep = 2 ** (8 * sonic_conf['sample_width'] - 1)

    lines_conf = [
        {
            'axis_lim' : [0, sonic_conf['block_size'], -bit_deep, bit_deep],
            'axes_x' : list(range(0,sonic_conf['block_size'])),
            'axes_y' : [0] * sonic_conf['block_size']
        },
        {
            'axis_lim' : [0, sonic_conf['sample_frequency'] // 2 + 1, 0, 3000],
            'axes_x' : [
                (i - 1) * sonic_conf['sample_frequency'] / sonic_conf['block_size']
                for i in range(0,sonic_conf['block_size'] // 2 + 1)
            ],
            'axes_y' : [0] * (sonic_conf['block_size'] // 2 + 1)
        }
    ]

    realtime_plot(lines_conf, data_generator)
    print('OK')