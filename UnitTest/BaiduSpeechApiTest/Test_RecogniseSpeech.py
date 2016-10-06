# -*- coding: utf-8 -*-
from BaiduSpeech.SpeechRecognizer import *
from UnitTest.BaiduSpeechApiTest.InstantialBaiduRecognizer import speech_recognizer


def speech_input_recognise_pretest():
    logging.warning("Test speech input recognise start ...")
    print("Test speech input recognise start!")
    speech_recognizer.speech_recognize_async(print, print)


if __name__ == '__main__':
    speech_input_recognise_pretest()
