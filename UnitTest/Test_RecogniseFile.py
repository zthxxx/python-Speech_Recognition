# -*- coding: utf-8 -*-
from BaiduSpeech.SpeechRecognizer import *


_baidu_test_token = '24.244be7656f96f73085bade14fb17e2b2.2592000.1476288394.282335-8616796'

def test_file_recognise():
    '''
    本例中为了测试使用 _test_token，实际使用中应使用从配置文件中读取的 token
    以下为从配置文件读取的实例：
    # baidu_oauth_conf = 'BaiduSpeech./BaiduOAuth.ini'
    # # api_key, secret_key = get_baidu_api_key_config(baidu_oauth_conf)
    # # access_token = get_baidu_token_url(api_key, secret_key)
    # # save_baidu_token_config(baidu_oauth_conf, access_token)
    # access_token = get_baidu_token_config(baidu_oauth_conf)
    # speech_recognizer = BaiduSpeechRecognizer(access_token)
    '''
    speech_recognizer = BaiduSpeechRecognizer(_baidu_test_token)
    # ['RecordExample.wav', 'RecordFilteredExample.wav']
    for filename in ['RecordFilteredExample.wav']:
        err_no, result = speech_recognizer.wav_file_recognition('WaveOperate/' + filename)
        assert err_no is 0
        assert True in ['把空调调到25度' in item for item in result]

