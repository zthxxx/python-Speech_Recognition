# -*- coding: utf-8 -*-
import numpy
from scipy import signal


def butter_bandpass(low_cut, high_cut, sample_frequency, order=3):
    nyquist_f = 0.5 * sample_frequency
    low_point = low_cut / nyquist_f
    high_point = high_cut / nyquist_f
    b, a = signal.butter(order, (low_point, high_point), btype='bandpass')
    iir_polynomials = (b, a)
    return iir_polynomials

def butter_bandpass_filter(low_cut, high_cut, sample_frequency, **kwargs):
    iir_polynomials = butter_bandpass(low_cut, high_cut, sample_frequency, **kwargs)
    def bandpass_filter(data):
        filtered_data = signal.filtfilt(*iir_polynomials, data)
        return filtered_data
    return bandpass_filter

