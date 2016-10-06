# -*- coding: utf-8 -*-
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .AudioRecord import *


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

