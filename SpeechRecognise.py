# -*- coding: utf-8 -*-
import json
import uuid
import logging
import threading
try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
from WaveOperate.WaveFilter import *
from BaiduSpeech.SpeechRecognizer import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    baidu_oauth_conf = 'BaiduSpeech./BaiduOAuth.ini'
    # api_key, secret_key = get_baidu_api_key_config(baidu_oauth_conf)
    # access_token = get_baidu_token_url(api_key, secret_key)
    # save_baidu_token_config(baidu_oauth_conf, access_token)
    access_token = get_baidu_token_config(baidu_oauth_conf)
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
    logging.warning("speech recognition record start.")
    speech_recognizer = BaiduSpeechRecognizer(access_token, sonic_conf, record_conf)

    # for err_no, result in speech_recognizer.speech_recognition():
    #     print(err_no, result)

    # speech_recognizer.wav_file_recognize_async('WaveOperate/RecordExample.wav', print, print)
    # speech_recognizer.wav_file_recognize_async('WaveOperate/RecordFilteredExample.wav', print, print)

    speech_recognizer.speech_recognize_async(print, print)

















