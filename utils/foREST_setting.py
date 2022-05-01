import configparser
import os
import nltk
import datetime


def read_config(title, key):
    conf = configparser.ConfigParser()
    root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../FoREST_config.conf")
    conf.read(root_path)
    return conf.get(title, key)

START_TIME = datetime.datetime.now()
TESTING_TIME = float(read_config('testing_setting', 'testing_time'))
SEND_TIMEOUT = read_config('request', 'send_timeout')
RECEIVED_TIMEOUT = read_config('request', 'received_timeout')
API_FILE_PATH = read_config('api_file', 'file_path')


class foRESTSetting(object):
    __instance = None


    @staticmethod
    def Instance():
        return foRESTSetting.__instance

    def __init__(self, ):
        self._testing_time = float(read_config('testing_setting', 'testing_time'))
        self._send_timeout = read_config('request', 'send_timeout')
        self._received_timeout = read_config('request', 'received_timeout')
        self._api_file_path = read_config('api_file', 'file_path')
        foRESTSetting.__instance = self

    @property
    def testing_time(self):
        return self._testing_time

    @property
    def send_request_timeout(self):
        return self._send_timeout

    @property
    def received_request_timeout(self):
        return self._received_timeout

    @property
    def api_file_path(self):
        return self._api_file_path

http_header = {
    'Content-Type': read_config('http_header', 'Content-Type'),
    'Authorization': read_config('http_header', 'Authorization')
               }
http_header_no_auth = {
    'Content-Type': read_config('http_header', 'Content-Type')
}
