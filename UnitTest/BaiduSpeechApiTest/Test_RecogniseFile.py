# -*- coding: utf-8 -*-
from BaiduSpeech.SpeechRecognizer import *
from UnitTest.BaiduSpeechApiTest.InstantialBaiduRecognizer import speech_recognizer


def test_file_recognise():
    logging.warning("Test file recognise start ...")
    # ['RecordExample.wav', 'RecordFilteredExample.wav']
    for filename in ['RecordFilteredExample.wav']:
        err_no, result = speech_recognizer.wav_file_recognition('WaveOperate/' + filename)
        assert err_no is 0
        assert True in ['把空调调到25度' in item for item in result]
    logging.warning("Test file recognise OK.")


if __name__ == '__main__':
    test_file_recognise()
