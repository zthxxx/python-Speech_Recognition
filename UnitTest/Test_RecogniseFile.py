# -*- coding: utf-8 -*-
import os
print(os.getcwd())
from ..BaiduSpeech.SpeechRecognizer import *
logging.basicConfig(level=logging.INFO)

def test_file_recognise():
    baidu_oauth_conf = 'BaiduSpeech./BaiduOAuth.ini'
    # api_key, secret_key = get_baidu_api_key_config(baidu_oauth_conf)
    # access_token = get_baidu_token_url(api_key, secret_key)
    # save_baidu_token_config(baidu_oauth_conf, access_token)
    access_token = get_baidu_token_config(baidu_oauth_conf)
    speech_recognizer = BaiduSpeechRecognizer(access_token)

    for filename in ['RecordExample.wav', 'RecordFilteredExample.wav']:
        err_no, result = speech_recognizer.wav_file_recognition('WaveOperate/' + filename)
        assert err_no is 0
        assert True in ['把空调调到25度' in item for item in result]

