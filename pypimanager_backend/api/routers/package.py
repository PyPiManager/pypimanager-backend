#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/15 下午2:11
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/15 下午2:11
# @Modified By: toddlerya


from lxml import etree
import requests

from api.base import router
from api.schemas.base_schema import ResponseBase
from settings import PYPI_SIMPLE_INDEX_URL
from utils.log import logger


def get_pypi_simple_index():
    """
    获取pypi simple 索引信息
    Returns:

    """
    status = False
    data = list()
    message = "ok"
    try:
        resp = requests.get(PYPI_SIMPLE_INDEX_URL)
    except Exception as err:
        message = f'无法访问pypi simple index: {err}'
        logger.error(message)
    else:
        if resp.status_code != 200:
            message = f'pypi simple index服务异常: {resp.status_code}'
            logger.error(message)
        else:
            content = resp.text.encode('utf-8')
            html = etree.HTML(content)
            __data = html.xpath('//a/text()')
            data = [{'package': ele} for ele in __data]
            status = True
    return status, message, data


@router.get("/package", response_model=ResponseBase, tags=['search'])
async def get_package_info():
    """
    获取全部包概览信息
    Returns:

    """

    status, message, data = get_pypi_simple_index()
    resp_data = ResponseBase(
        description='获取simple索引信息',
        data=data,
        message=message,
        status=status
    )
    return resp_data.dict()
