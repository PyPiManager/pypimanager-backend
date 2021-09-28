#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 11:46
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 11:46
# @Modified By: toddlerya

import pathlib
import sys

from loguru import logger


class LogManager:
    def __init__(self, base_path, log_path, log_name,
        log_format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module} {function}:{line}</cyan> - <level>{message}</level>',
        file_log_level='INFO',
        console_log_level='INFO',
        rotation='32 MB',
        compression='zip',
        log_encode='utf-8',
        enqueue=True):
        """初始化logger参数

        Args:
            base_path (str): 日志目录的基础目录，可以是项目根目录，**绝对路径**
            log_path (str): 存放日志文件的目录，举个例子，可以设置为logs，`base_path`的相对路径
            log_name (str): 日志文件名称
            log_format (str, optional): 日志内容格式. Defaults to '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module} {function}:{line}</cyan> - <level>{message}</level>'.
            file_log_level (str, optional): 文件日志级别. Defaults to 'INFO'.
            console_log_level (str, optional): 终端窗口日志级别. Defaults to 'INFO'.
            rotation (str, optional): 日志的回转分卷配置. Defaults to '32 MB'.
            compression (str, optional): 历史日志压缩格式. Defaults to 'zip'.
            log_encode (str, optional): 日志的编码格式. Defaults to 'utf-8'.
            enqueue (bool, optional): 多线程安全设置. Defaults to True.
        """
        
        self.__config = {
            'handlers': [
                {
                    'sink': pathlib.Path(base_path).joinpath(log_path).joinpath(log_name),
                    'colorize': False,
                    'format': log_format,
                    'level': file_log_level,
                    'rotation': rotation,
                    'compression': compression,
                    'enqueue': enqueue,
                    'encoding': log_encode
                },
                {
                    'sink': sys.stdout,
                    'format': log_format,
                    'colorize': True,
                    'level': console_log_level,
                    'enqueue': enqueue
                }
            ]
        }
        logger.configure(**self.__config)

    def get_config(self):
        """获取logger参数"""
        return self.__config
