# -*- coding: utf-8 -*-
import logging
from WaveOperate.AudioPlay import *
from WaveOperate.WaveFilter import *
from WaveOperate.AudioRecord import *


recorder_main = None
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
    'block_min_count':16,
    'speech_filter':bandpass_filter
}
record_conf = RecordConf(**record_conf)

def instantial_recorder():
    # 此测试中录音播放均需硬件支持，无法通过 CI 的build
    global recorder_main
    recorder_main = AudioRecorder(sonic_conf, input_device_index=1)

def voice_record_save_pretest():
    logging.warning("Test record wav start ...")
    recorder_main.record_speech_wav(record_conf)
    logging.warning("Test record wav start OK")

def voice_record_repeat_pretest():
    logging.warning("Test record repeat start ...")
    wave_player = WavePlayer(sonic_conf)
    recording = recorder_main.record_speech(record_conf)
    for sonic in recording:
        audio_data = sonic.wave_bin_data
        wave_player.wave_play(audio_data)
    logging.warning("Test record repeat start OK")

def record_realtime_play_pretest():
    logging.warning("Test record realtime play start ...")
    recording_main = recorder_main.record_realtime(bandpass_filter)
    wave_player = WavePlayer(sonic_conf)
    for bin_audio_data in recording_main:
        wave_player.wave_play_async(bin_audio_data)


if __name__ == '__main__':
    instantial_recorder()

    # voice_record_save_pretest()

    voice_record_repeat_pretest()

    # record_realtime_play_pretest()
