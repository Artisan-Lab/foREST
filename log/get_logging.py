# coding:utf-8
import logging
import sys
from logging.handlers import RotatingFileHandler # 按文件大小滚动备份
import colorlog  # 控制台日志输入颜色
import time
import shutil
import datetime
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
        cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
        if not log_path:
            log_path = os.path.join(os.path.dirname(cur_path), 'log\logs')
        if os.path.isdir(log_path):
            self.delete_logs(log_path)
        else:
            os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个
        if not log_name:
            log_name = os.path.join(log_path, '%s' % time.strftime('%Y-%m-%d'))  # 文件的命名
        else:
            log_name = os.path.join(log_path, '%s' % log_name)
        self.error_log_name = os.path.join(log_path, 'ERROR')
        self.warning_log_name = os.path.join(log_path, 'warning')
        self.log_name = log_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s : %(message)s',
            log_colors=log_colors_config)  # 日志输出格式
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
        info_handle = RotatingFileHandler(filename=self.log_name, mode='a', encoding='utf-8')  # 使用RotatingFileHandler类，滚动备份日志
        info_handle.setLevel(logging.DEBUG)
        info_handle.setFormatter(self.formatter_file)
        creen_handle = colorlog.StreamHandler()
        creen_handle.setLevel(logging.DEBUG)
        creen_handle.setFormatter(self.formatter)
        # bug_handle = RotatingFileHandler(filename=self.error_log_name, mode='a', encoding='utf-8')
        # bug_handle.setLevel(logging.DEBUG)
        # bug_handle.setFormatter(self.formatter_file)
        #
        # warning_handle = RotatingFileHandler(filename=self.warning_log_name, mode='a', encoding='utf-8')
        # warning_handle.setLevel(logging.DEBUG)
        # bug_handle.setFormatter(self.formatter_file)

        if level == 'info':
            self.logger.addHandler(info_handle)
            self.logger.info(message)
            # 这两行代码是为了避免日志输出重复问题
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

        info_handle.close()  # 关闭打开的文件

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    # def get_file_sorted(self, file_path):
    #     """最后修改时间顺序升序排列 os.path.getmtime()->获取文件最后修改时间"""
    #     dir_list = os.listdir(file_path)
    #     if not dir_list:
    #         return
    #     else:
    #         dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
    #         return dir_list

    # def handle_logs(self):
    #     """处理日志过期天数和文件数量"""
    #     dir_list = ['report']  # 要删除文件的目录名
    #     for dir in dir_list:
    #         dirPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/' + dir  # 拼接删除目录完整路径
    #         file_list = self.get_file_sorted(dirPath)  # 返回按修改时间排序的文件list
    #         if file_list:  # 目录下没有日志文件
    #             for i in file_list:
    #                 file_path = os.path.join(dirPath, i)  # 拼接文件的完整路径
    #                 t_list = self.TimeStampToTime(os.path.getctime(file_path)).split('-')
    #                 now_list = self.TimeStampToTime(time.time()).split('-')
    #                 t = datetime.datetime(int(t_list[0]), int(t_list[1]),
    #                                       int(t_list[2]))  # 将时间转换成datetime.datetime 类型
    #                 now = datetime.datetime(int(now_list[0]), int(now_list[1]), int(now_list[2]))
    #                 if (now - t).days > 6:  # 创建时间大于6天的文件删除
    #                     self.delete_logs(file_path)
    #             if len(file_list) > 4:  # 限制目录下记录文件数量
    #                 file_list = file_list[0:-4]
    #                 for i in file_list:
    #                     file_path = os.path.join(dirPath, i)
    #                     print(file_path)
    #                     self.delete_logs(file_path)


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
