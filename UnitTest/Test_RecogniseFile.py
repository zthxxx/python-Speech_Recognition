# -*- coding: utf-8 -*-
import os
import logging
from BaiduSpeech.SpeechRecognizer import *


def test_file_recognise():
    logging.info("Test file recognise start ...")
    baidu_oauth_conf = 'BaiduSpeech/BaiduOAuth.ini'
    # api_key, secret_key = get_baidu_api_key_config(baidu_oauth_conf)
    # access_token = get_baidu_token_url(api_key, secret_key)
    # save_baidu_token_config(baidu_oauth_conf, access_token)
    access_token = get_baidu_token_config(baidu_oauth_conf)
    if not access_token:
        access_token = os.getenv('BAIDU_ACCESS_TOKEN')
        if not access_token:
            raise Exception("BAIDU_TEST_TOKEN not found.")
    speech_recognizer = BaiduSpeechRecognizer(access_token)
    # ['RecordExample.wav', 'RecordFilteredExample.wav']
    for filename in ['RecordFilteredExample.wav']:
        err_no, result = speech_recognizer.wav_file_recognition('WaveOperate/' + filename)
        assert err_no is 0
        assert True in ['把空调调到25度' in item for item in result]
    logging.info("Test file recognise OK.")


if __name__ == '__main__':
    print("Main test start.")
    print(os.getcwd())
    test_file_recognise()