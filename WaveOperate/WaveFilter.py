# -*- coding: utf-8 -*-
import functools
import numpy
from scipy import signal


def polynomials_filter(polynomial_creater):
    @functools.wraps(polynomial_creater)
    def filter_creater(*args, **kwargs):
        iir_polynomial = polynomial_creater(*args, **kwargs)
        def bandpass_filter(data):
            filtered_data = signal.lfilter(*iir_polynomial, data)
            return filtered_data
        return bandpass_filter
    return filter_creater

@polynomials_filter
def butter_bandpass(low_cut, high_cut, sample_frequency, order=6):
    nyquist_f = 0.5 * sample_frequency
    low_point = low_cut / nyquist_f
    high_point = high_cut / nyquist_f
    b, a = signal.butter(order, (low_point, high_point), btype='bandpass')
    iir_polynomial = (b, a)
    return iir_polynomial

@polynomials_filter
def cheby1_bandpass(low_cut, high_cut, sample_frequency, order=6, rp=0.1):
    nyquist_f = 0.5 * sample_frequency
    low_point = low_cut / nyquist_f
    high_point = high_cut / nyquist_f
    b, a = signal.cheby1(order, rp, (low_point, high_point), btype='bandpass')
    iir_polynomials = (b, a)
    return iir_polynomials


