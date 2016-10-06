# -*- coding: utf-8 -*-
import logging
from WaveOperate.AudioPlay import *


def wav_file_play_pretest():
    logging.warning("Test wav file play start ...")
    wav_file = "WaveOperate/Ring01.wav"
    wav_file_play(wav_file)
    logging.warning("Test wav file play OK")


if __name__ == '__main__':
    wav_file_play_pretest()
