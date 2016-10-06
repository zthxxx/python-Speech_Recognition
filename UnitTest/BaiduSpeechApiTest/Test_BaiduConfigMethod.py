# -*- coding: utf-8 -*-
import random
from BaiduSpeech.SpeechRecognizer import *


def baidu_token_read_save_test():
    logging.warning("Test baidu config token read and save ...")
    config_sample_path = "BaiduSpeech/BaiduOAuthSample.ini"
    original = get_baidu_token_config(config_sample_path)
    check_data = str(random.random())
    save_baidu_token_config(config_sample_path, check_data)
    read_data = get_baidu_token_config(config_sample_path)
    save_baidu_token_config(config_sample_path, original)
    assert str(read_data) == check_data
    logging.warning("Test baidu config token read and save method OK.")


if __name__ == '__main__':
    baidu_token_read_save_test()
