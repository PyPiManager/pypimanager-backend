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
        """
        初始化logger参数
        """
        self.__config = {
            'handlers': [
                {
                    'sink': pathlib.Path(base_path).joinpath(log_path).joinpath(log_name),
                    'colorze': False,
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
                    'colorze': True,
                    'level': console_log_level,
                    'enqueue': enqueue,
                    'encoding': log_encode
                }
            ]
        }
        logger.configure(**self.__config)

    def get_config(self):
        """获取logger参数"""
        return self.__config