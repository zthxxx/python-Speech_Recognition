# -*- coding: utf-8 -*-
import os
from BaiduSpeech.SpeechRecognizer import *


_baidu_oauth_conf = 'BaiduSpeech/BaiduOAuth.ini'
# api_key, secret_key = get_baidu_api_key_config(_baidu_oauth_conf)
# access_token = get_baidu_token_url(api_key, secret_key)
# save_baidu_token_config(_baidu_oauth_conf, access_token)
_BAIDU_ACCESS_TOKEN = get_baidu_token_config(_baidu_oauth_conf)
if not _BAIDU_ACCESS_TOKEN:
    _BAIDU_ACCESS_TOKEN = os.getenv('BAIDU_ACCESS_TOKEN')
    if not _BAIDU_ACCESS_TOKEN:
        raise Exception("BAIDU_TEST_TOKEN not found.")
