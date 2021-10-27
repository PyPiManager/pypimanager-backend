#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/27 下午12:07
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/27 下午12:07
# @Modified By: toddlerya

import requests
from lxml import etree

from utils.log import logger
from settings import PYPI_SIMPLE_INDEX_URL
from api.base import CACHE, Cache


def pypi_simple_index_cache(mode: str = 'fetch', cache: Cache = CACHE):
    """
    缓存pypi simple index索引信息
    Args:
        mode:
        cache:

    Returns:

    """
    message = "ok"
    status = False
    if mode == 'update':
        __status, __message, data = get_pypi_simple_index()
        if __status:
            cache.PYPI_SIMPLE_INDEX = data
        message = __message
        status = __status
    if cache.PYPI_SIMPLE_INDEX:
        status = True
    else:
        message = '获取pypi simple index索引信息错误'
    return status, message, cache.PYPI_SIMPLE_INDEX


def get_pypi_simple_index():
    """
    获取pypi simple 索引信息
    Returns:

    """
    __status = True
    data = list()
    message = "ok"
    try:
        resp = requests.get(PYPI_SIMPLE_INDEX_URL)
    except Exception as err:
        message = f'无法访问pypi simple index: {err}'
        __status = False
        logger.error(message)
    else:
        if resp.status_code != 200:
            __status = False
            message = f'pypi simple index服务异常: {resp.status_code}'
            logger.error(message)
        else:
            content = resp.text.encode('utf-8')
            html = etree.HTML(content)
            __data = html.xpath('//a/text()')
            data = [{'package': ele} for ele in __data]
    return __status, message, data
