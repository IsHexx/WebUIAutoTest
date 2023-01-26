"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : logger_util.py
@Author : putongrenji
@Time : 2022/4/29 18:23
@Motto:Don't ever let somebody tell you you can't do something
"""
import logging
import time
from config.config_util import get_project_path, get_yaml_config


class LoggerUtil:
    # 初始化文件和控制台的日志对象，日志级别，日志文件路径，日志格式等。
    def __init__(self, loggerName = '测试'):
        # 创建一个logger,loggerName就是给这个logger起一个名字。
        self.logger = logging.getLogger(loggerName)
        # 获取全局日志级别为DEBUG
        self.logger.setLevel(logging.DEBUG)
        # 设置日志文件的输入路径和名称
        self.log_path = get_project_path()+ '\\' + 'logs\\'
        self.log_time = time.strftime("%Y_%m_%d")
        self.log_path_and_name = self.log_path+get_yaml_config('log','log_name')+self.log_time+'.log'
        # 创建文件和控制台日志处理器
        self.file_handler = None
        self.console_handler = None

    # 创建文件日志
    def create_file_log(self):
        # 使用FileHandler创建文件日志处理器对象，向指定文件输出日志信息。
        print(self.log_path_and_name)
        self.file_handler=logging.FileHandler(self.log_path_and_name,encoding='utf-8')
        # 设置日志处理器日志级别
        fileLogLevel = get_yaml_config('log','file_log_level')
        if fileLogLevel.lower() == 'debug':
            self.file_handler.setLevel(logging.DEBUG)
        elif fileLogLevel.lower() == 'info':
            self.file_handler.setLevel(logging.INFO)
        elif fileLogLevel.lower() == 'warning':
            self.file_handler.setLevel(logging.WARNING)
        elif fileLogLevel.lower() == 'error':
            self.file_handler.setLevel(logging.ERROR)
        elif fileLogLevel.lower() == 'critical':
            self.file_handler.setLevel(logging.CRITICAL)
        else:
            self.file_handler.setLevel(logging.INFO)
        # 设置日志处理器的日志格式
        self.formatter = logging.Formatter(get_yaml_config('log','file_log_format'))
        self.file_handler.setFormatter(self.formatter)
        # 将日志处理器加入日志对象。
        self.logger.addHandler(self.file_handler)

    # 创建控制台日志
    def create_console_log(self):
        # 使用StreamHandler可以向类似与sys.stdout或者sys.stderr的任何文件对象输出信息。
        self.console_handler=logging.StreamHandler()
        # 设置日志处理器的日志级别
        consoleLogLevel = get_yaml_config('log','console_log_level')
        if consoleLogLevel.lower() == 'debug':
            self.console_handler.setLevel(logging.DEBUG)
        elif consoleLogLevel.lower() == 'info':
            self.console_handler.setLevel(logging.INFO)
        elif consoleLogLevel.lower() == 'warning':
            self.console_handler.setLevel(logging.WARNING)
        elif consoleLogLevel.lower() == 'error':
            self.console_handler.setLevel(logging.ERROR)
        elif consoleLogLevel.lower() == 'critical':
            self.console_handler.setLevel(logging.CRITICAL)
        else:
            self.console_handler.setLevel(logging.INFO)
        # 设置日志处理器的日志格式
        self.formatter = logging.Formatter(get_yaml_config('log','console_log_format'))
        self.console_handler.setFormatter(self.formatter)
        # 将日志处理器加入日志对象。
        self.logger.addHandler(self.console_handler)

    #从日志对象中移除日志处理器。（防止日志重写）
    def remove_handler(self):
        # 关闭日志处理器输出流和移除日志处理器
        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)
        # 关闭日志处理器输出流和移除日志处理器
        self.console_handler.close()
        self.logger.removeHandler(self.console_handler)

    #获得日志对象
    def get_logger(self):
        self.create_file_log()
        self.create_console_log()
        return self.logger

if __name__ == '__main__':
    logger = LoggerUtil().get_logger()
    logger.info("普通信息")
    logger.debug("调试信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误")