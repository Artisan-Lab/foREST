# coding:utf-8
import json
import logging
import sys
from logging.handlers import RotatingFileHandler
import colorlog
import time
import os



log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class Log:
    def __init__(self, log_name = None,log_path = None):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        if not log_path:
            log_path = os.path.join(os.path.dirname(cur_path), 'log\logs')
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
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
        creen_handle = colorlog.StreamHandler()
        creen_handle.setLevel(logging.DEBUG)
        creen_handle.setFormatter(self.formatter)

        if level == 'info':
            self.logger.addHandler(file_handle)
            self.logger.info(message)
            self.logger.removeHandler(file_handle)
        elif level == 'debug':
            self.logger.addHandler(creen_handle)
            self.logger.debug(message)
            self.logger.removeHandler(creen_handle)
        elif level == 'warning':
            self.logger.addHandler(creen_handle)
            self.logger.addHandler(file_handle)
            self.logger.warning(message)
            self.logger.removeHandler(creen_handle)
            self.logger.removeHandler(file_handle)
        elif level == 'json':
            with open(self.log_name, 'w') as f:
                f.write(json.dumps(message, indent=4))
        elif level == 'object':
            with open(self.log_name, 'w') as f:
                f.write(json.dumps(message, default=lambda o: o.__dict__, indent=4))
        file_handle.close()

    def print(self, message):
        self.__console('print', message)

    def save(self, message):
        self.__console('save', message)

    def save_and_print(self, message):
        self.__console('save_and_print', message)

    def save_object(self, message):
        self.__console('object', message)

    def save_json(self, message):
        self.__console('json', message)


program_log = Log(log_name="program_running_status")
summery_log = Log(log_name='summery')
requests_log = Log(log_name='total_request')
status_2xx_log = Log(log_name='2xx_request')
status_4xx_log = Log(log_name='4xx_request')
status_3xx_log = Log(log_name='3xx_request')
status_5xx_log = Log(log_name='5xx_request')
status_timeout_log = Log(log_name='timeout_request')
external_log = Log(log_name='hit_external_field')
summery_count = {
    'api number': 0,
    'already send requests number': 0,
    '2xx requests number': 0,
    '4xx requests number': 0,
    '3xx requests number': 0,
    '5xx requests number': 0,
    'timeout requests number': 0
}
