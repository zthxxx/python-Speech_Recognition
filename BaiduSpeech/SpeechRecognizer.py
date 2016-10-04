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
from ..WebCurl.WebCurl import *
from ..ConfigFileInfoParser.InitializationConfigParser import InitializationConfigParser
from ..WaveOperate.Sonic import *
from ..WaveOperate.AudioRecord import *
from ..WaveOperate.WaveFilter import *



def get_baidu_api_key_config(path):
    ini_Parser = InitializationConfigParser(path)
    Client_Credentials = ini_Parser.GetAllNodeItems("ClientCredentials")
    api_key = Client_Credentials.get("api_key")
    secret_key = Client_Credentials.get("secret_key")
    return api_key, secret_key

def get_baidu_token_config(path):
    ini_Parser = InitializationConfigParser(path)
    Client_Credentials = ini_Parser.GetAllNodeItems("ClientCredentials")
    access_token = Client_Credentials.get("access_token")
    return access_token

def get_baidu_token_url(api_key, secret_key):
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + api_key + "&client_secret=" + secret_key
    response = get_page_data(auth_url)
    json_str = str(response.decode())
    json_data = json.loads(json_str)
    access_token = json_data.get('access_token')
    return access_token

def save_baidu_token_config(path, access_token):
    ini_Parser = InitializationConfigParser(path)
    ini_Parser.SetOneKeyValue("ClientCredentials","access_token",access_token)

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return "-".join([mac[e:e + 2] for e in range(0, 11, 2)])

class BaiduSpeechRecognizer:
    def __init__(self, token, sonic_conf=Sonic(), record_conf=RecordConf()):
        self.token = token
        self.sonic_conf = sonic_conf
        self.record_conf = record_conf
        self.cuid = get_mac_address() #用户 ID，推荐使用设备mac 地址/手机IMEI 等设备唯一性参数

    def post_recognition(self,sonic):
        if not sonic.wave_bin_data or sonic.channels is not 1:
            raise Exception("wave_channels only support 1!")
        if isinstance(sonic.wave_bin_data, list):
            audio_data = bytearray()
            for data in sonic.wave_bin_data:
                audio_data.extend(data)
            audio_data = bytes(audio_data)
        elif not isinstance(sonic.wave_bin_data, bytes):
            raise Exception("Type of bin_data need bytes!")
        else:
            audio_data = sonic.wave_bin_data
        bin_data_length = sonic.sample_length * sonic.sample_width
        voice_service_url = 'http://vop.baidu.com/server_api' + '?cuid=' + self.cuid + '&token=' + self.token #+ '&lan=en'
        head = [
            'Content-Type: audio/pcm; rate=%d' % sonic.sample_frequency,
            'Content-Length: %d' % bin_data_length
        ]
        logging.info("Post start")
        page_data = post_page_data(voice_service_url, audio_data, head)
        logging.debug(page_data.decode())
        logging.info("Post end")
        json_data = json.loads(page_data.decode())
        err_no = json_data.get('err_no')
        if err_no:
            err_msg = json_data.get('err_msg')
            logging.debug("Speech recognition ERROR!")
            logging.debug("Error! " + err_msg)
            return err_no, "Error! " + err_msg
        else:
            result = json_data.get('result')
            logging.debug(result)
            return err_no, result

    def speech_recognize(self):
        recorder = AudioRecorder(self.sonic_conf)
        recording = recorder.record_speech(self.record_conf)
        for sonic in recording:
            yield self.post_recognition(sonic)

    def wav_file_recognition(self, filename):
        sonic = wav_file_read(filename)
        return self.post_recognition(sonic)

    def recognize_callback(self, sonic, callback=None, traceback=None):
        err_no, result = self.post_recognition(sonic)
        if err_no:
            if traceback:
                traceback(result)
        else:
            if callback:
                callback(err_no, result)

    def speech_recognize_async(self, callback=None, traceback=None):
        recorder = AudioRecorder(self.sonic_conf)
        recording = recorder.record_speech(self.record_conf)
        for sonic in recording:
            post_thread = threading.Thread(target=self.recognize_callback, args=(sonic, callback, traceback))
            post_thread.start()

    def wav_file_recognize_async(self, filename, callback=None, traceback=None):
        sonic = wav_file_read(filename)
        post_thread = threading.Thread(target=self.recognize_callback, args=(sonic, callback, traceback))
        post_thread.start()



