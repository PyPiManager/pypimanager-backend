#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/13 下午3:28
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/13 下午3:28
# @Modified By: toddlerya


from twine.commands.upload import main as upload

from settings import PYPI_REPOSITORY, PYPI_USERNAME, PYPI_PASSWORD
from utils.log import logger


@logger.catch(reraise=True)
def twine_upload(python_package_file):
    """
    调用twine进行上传
    Args:
        python_package_file:

    Returns:

    """
    try:
        upload([
            python_package_file,
            '--repository-url',
            PYPI_REPOSITORY,
            '-u',
            PYPI_USERNAME,
            '-p',
            PYPI_PASSWORD
        ])
    except Exception as err:
        message = f'上传{python_package_file}失败！错误信息: {err}'
        return False, message
    else:
        return True, ''


if __name__ == '__main__':
    twine_upload("/home/evi1/Downloads/pip_download/requests/requests-2.26.0-py2.py3-none-any.whl")
