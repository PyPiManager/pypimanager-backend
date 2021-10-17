#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/13 下午5:57
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/13 下午5:57
# @Modified By: toddlerya

import shutil
import os
import pathlib

from utils.log import logger


def delete_file(file_path):
    """
    删除文件
    Args:
        file_path:

    Returns:

    """
    if pathlib.Path(file_path).is_file():
        try:
            os.remove(file_path)
        except Exception as err:
            logger.error(f'删除文件失败: {file_path}, 错误信息: {err}')
            return False
        else:
            return True
    else:
        logger.warning(f'文件不存在: {file_path}')
        return False


def move(src, dst):
    """
    移动文件
    Args:
        src:
        dst:

    Returns:

    """
    if pathlib.Path(src).exists():
        try:
            shutil.move(src=src, dst=dst)
        except Exception as err:
            logger.error(f'移动失败, src: {src}, dst: {dst}, 报错信息: {err}')
            return False
        else:
            return True
    else:
        logger.error(f'未发现文件或目录，请确认源目标是否正确: {src}')
        return False
