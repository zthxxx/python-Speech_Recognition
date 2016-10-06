# -*- coding: utf-8 -*-
from BaiduSpeech.SpeechRecognizer import *
from UnitTest.BaiduSpeechApiTest.ReadLocalBaiduToken import _BAIDU_ACCESS_TOKEN
from WaveOperate.WaveFilter import *

sonic_conf = {
    'channels':1,
    'sample_width':2,
    'sample_frequency':16000,
    'sample_length':2048
}
sonic_conf = Sonic(**sonic_conf)
bandpass_filter = butter_bandpass(150, 2000, sonic_conf.sample_frequency)
record_conf = {
    'gate_value':700,
    'series_min_count':30,
    'block_min_count':8,
    'speech_filter':bandpass_filter
}
record_conf = RecordConf(**record_conf)
speech_recognizer = BaiduSpeechRecognizer(_BAIDU_ACCESS_TOKEN, sonic_conf, record_conf)
if not speech_recognizer:
    raise Exception("Can`t instantiate BaiduSpeechRecognizer")
