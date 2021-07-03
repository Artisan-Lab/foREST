import logging
import os
from logging import handlers
import time

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)))

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s: %(message)s'):
        self.level = level
        self.when = when
        self.backCount = backCount
        self.fmt = fmt
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(self.fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(self.level))#设置日志级别
        self.sh = logging.StreamHandler()#往屏幕上输出
        self.sh.setFormatter(format_str) #设置屏幕上显示的格式
        self.th = handlers.TimedRotatingFileHandler(filename=self.path+'/logging/'+filename,when=self.when,backupCount=self.backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        self.th.setFormatter(format_str)#设置文件里写入的格式

    def set_handlers(self):
        self.logger.addHandler(self.sh) #把对象加到logger里
        self.logger.addHandler(self.th)

    def clean_handlers(self):
        self.logger.handlers.pop()
        self.logger.handlers.pop()

    def print_debug(self, debug_info):
        self.set_handlers()
        self.logger.debug(debug_info)
        self.clean_handlers()

    def print_info(self, info_info):
        self.set_handlers()
        self.logger.info(info_info)
        self.clean_handlers()

    def print_warning(self, warning_info):
        self.set_handlers()
        self.logger.warning(warning_info)
        self.clean_handlers()

    def print_error(self, error_info):
        self.set_handlers()
        self.logger.info(error_info)
        self.clean_handlers()

    def print_crit(self,crit_info):
        self.set_handlers()
        self.logger.crit(crit_info)
        self.clean_handlers()


if __name__ == '__main__':
    log = Logger('request.log', level='debug')
    while True:
        log.print_debug('debug')
        time.sleep(1)
        log.print_info('info')
        time.sleep(1)
