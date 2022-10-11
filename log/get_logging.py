# coding:utf-8
import json
import logging
import threading
import sys
from logging.handlers import RotatingFileHandler
import colorlog
import time
import os
from foREST_setting import foRESTSettings

lock = threading.Lock()

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class Log:
    def __init__(self, log_name=None, log_path=None):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        if not log_path:
            log_path = os.path.join(os.path.dirname(cur_path), 'log/logs')
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        self.base_name = log_name
        if not log_name:
            log_name = os.path.join(log_path, '%s' % time.strftime('%Y-%m-%d'))
        else:
            log_name = os.path.join(log_path, '%s' % log_name)
        if os.path.exists(log_name):
            self.delete_logs(log_name)
        self.error_log_name = os.path.join(log_path, 'ERROR')
        self.warning_log_name = os.path.join(log_path, 'warning')
        self.log_name = log_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s : %(message)s',
            log_colors=log_colors_config)
        self.formatter_file = logging.Formatter(
            '%(asctime)s : %(message)s')

    def out_put(self, path):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(cur_path, path)
        self.log_name = os.path.join(path, self.base_name)
        if not os.path.isdir(path):
            os.mkdir(path)
        if os.path.exists(self.log_name):
            self.delete_logs(self.log_name)

    def delete_logs(self, file_path):
        try:
            os.remove(file_path)
        except PermissionError as e:
            print('Failed to delete log directory: {}'.format(e))
            sys.exit()

    def __console(self, level, message):
        file_handle = RotatingFileHandler(filename=self.log_name, mode='a', encoding='utf-8')
        file_handle.setLevel(logging.DEBUG)
        file_handle.setFormatter(self.formatter_file)
        screen_handle = colorlog.StreamHandler()
        screen_handle.setLevel(logging.DEBUG)
        screen_handle.setFormatter(self.formatter)

        if level == 'save':
            self.logger.addHandler(file_handle)
            self.logger.info(message)
            self.logger.removeHandler(file_handle)
        elif level == 'print':
            self.logger.addHandler(screen_handle)
            self.logger.debug(message)
            self.logger.removeHandler(screen_handle)
        elif level == 'save_and_print':
            self.logger.addHandler(screen_handle)
            self.logger.addHandler(file_handle)
            self.logger.warning(message)
            self.logger.removeHandler(screen_handle)
            self.logger.removeHandler(file_handle)
        elif level == 'json':
            with open(self.log_name, 'w') as f:
                f.write(json.dumps(message, indent=4))
        elif level == 'object':
            with open(self.log_name, 'w') as f:
                f.write(json.dumps(message, default=lambda o: o.__dict__))
        file_handle.close()

    def print(self, message):
        lock.acquire()
        print("\r", "\n", end="")
        self.__console('print', message)
        lock.release()

    def save(self, message):
        pass
        # self.__console('save', message)

    def save_and_print(self, message):
        lock.acquire()
        self.__console('save_and_print', message)
        lock.release()

    def save_object(self, message):
        self.__console('object', message)

    def save_json(self, message):
        self.__console('json', message)

foREST_log = Log(log_name="program_running_status.txt")
summery_log = Log(log_name='summery.txt')
requests_log = Log(log_name='total_request.txt')
status_2xx_log = Log(log_name='2xx_request.txt')
status_4xx_log = Log(log_name='4xx_request.txt')
status_3xx_log = Log(log_name='3xx_request.txt')
status_5xx_log = Log(log_name='5xx_request.txt')
status_timeout_log = Log(log_name='timeout_request.txt')
external_log = Log(log_name='hit_external_field.txt')
inconsistent_parameter = Log(log_name='inconsistent_parameter.txt')
no_reference_log = Log("no_reference_key.json")
result_log = Log(log_name="result.txt")

def set_out_put(path):
    foREST_log.out_put(path)
    summery_log.out_put(path)
    requests_log.out_put(path)
    status_timeout_log.out_put(path)
    status_5xx_log.out_put(path)
    status_4xx_log.out_put(path)
    status_3xx_log.out_put(path)
    status_2xx_log.out_put(path)
    external_log.out_put(path)
    no_reference_log.out_put(path)
    inconsistent_parameter.out_put(path)
    result_log.out_put(path)
