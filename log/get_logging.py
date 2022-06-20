# coding:utf-8
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
        if os.path.isdir(log_path):
            self.delete_logs(log_path)
        else:
            os.mkdir(log_path)
        if not log_name:
            log_name = os.path.join(log_path, '%s' % time.strftime('%Y-%m-%d'))
        else:
            log_name = os.path.join(log_path, '%s' % log_name)
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
            file_list = os.listdir(file_path)
            for f in file_list:
                f_path = os.path.join(file_path, f)
                os.remove(f_path)
        except PermissionError as e:
            print('Failed to delete log directory: {}'.format(e))
            sys.exit()

    def __console(self, level, message):
        info_handle = RotatingFileHandler(filename=self.log_name, mode='a', encoding='utf-8')
        info_handle.setLevel(logging.DEBUG)
        info_handle.setFormatter(self.formatter_file)
        creen_handle = colorlog.StreamHandler()
        creen_handle.setLevel(logging.DEBUG)
        creen_handle.setFormatter(self.formatter)

        if level == 'info':
            self.logger.addHandler(info_handle)
            self.logger.info(message)
            self.logger.removeHandler(info_handle)
        elif level == 'debug':
            self.logger.addHandler(creen_handle)
            self.logger.debug(message)
            self.logger.removeHandler(creen_handle)
        # elif level == 'warning':
        #     self.logger.addHandler(creen_handle)
        #     self.logger.addHandler(warning_handle)
        #     self.logger.warning(message)
        #     self.logger.removeHandler(creen_handle)
        #     self.logger.removeHandler(warning_handle)
        # elif level == 'error':
        #     self.logger.addHandler(creen_handle)
        #     self.logger.addHandler(bug_handle)
        #     self.logger.error(message)
        #     self.logger.removeHandler(creen_handle)
        #     self.logger.removeHandler(bug_handle)

        info_handle.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


DebugLog = Log()
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
