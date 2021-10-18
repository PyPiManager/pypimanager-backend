#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/18 下午5:38
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/18 下午5:38
# @Modified By: toddlerya


from fastapi import Depends

from api.routers.package import get_pypi_simple_index
import api.cruds.statistics as crud
from api.base import router, get_db
from api.schemas.base_schema import ResponseBase
from utils.db import DB


@router.get('/stat/trend', response_model=ResponseBase, tags=['stat'])
async def trend(db: DB = Depends(get_db)):
    """
    获取趋势图统计数据
    Args:
        db:

    Returns:

    """
    message, result = crud.stat_download_trend(db)
    resp_data = ResponseBase(
        description='获取下载量趋势图统计数据',
        data=result,
        message=message
    )
    return resp_data.dict()


@router.get('/stat/package_count', response_model=ResponseBase, tags=['stat'])
async def package_count():
    """
    统计包总数
    Returns:

    """
    __status, message, data = get_pypi_simple_index()
    if __status:
        result = len(data)
    else:
        result = 0
    resp_data = ResponseBase(
        description='统计包总数',
        data=result,
        message=message
    )
    return resp_data.dict()


@router.get('/stat/file_count', response_model=ResponseBase, tags=['stat'])
async def file_count(db: DB = Depends(get_db)):
    """
    统计上传的文件总数
    Args:
        db:

    Returns:

    """
    message, result = crud.stat_total_file_count(db)
    resp_data = ResponseBase(
        description='获取上传的文件总数',
        data=result,
        message=message
    )
    return resp_data.dict()


@router.get('/stat/download_user_count', response_model=ResponseBase, tags=['stat'])
async def download_user_count(db: DB = Depends(get_db)):
    """
    统计累计下载用户数量
    Args:
        db:

    Returns:

    """
    message, result = crud.stat_download_user_count(db)
    resp_data = ResponseBase(
        description='统计累计下载用户数量',
        data=result,
        message=message
    )
    return resp_data.dict()


@router.get('/stat/download_total_count', response_model=ResponseBase, tags=['stat'])
async def download_total_count(db: DB = Depends(get_db)):
    """
    统计下载总量
    Args:
        db:

    Returns:

    """
    message, result = crud.stat_download_total_count(db)
    resp_data = ResponseBase(
        description='统计下载总量',
        data=result,
        message=message
    )
    return resp_data.dict()


@router.get('/stat/save_time_hour', response_model=ResponseBase, tags=['stat'])
async def save_time_hour(db: DB = Depends(get_db)):
    """
    累计节省人时，按下载安装一个包需要2分钟为例
    Args:
        db:

    Returns:

    """
    message, result = crud.stat_download_total_count(db)
    hour = int(result * 60 * 2 / 3600)
    # 若小于0则保留1位小数
    # if hour < 0:
    #     from decimal import Decimal, ROUND_HALF_UP
    #     hour = Decimal(hour).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
    #     hour = '{:.1f}'.format(hour)
    resp_data = ResponseBase(
        description='累计节省人时',
        data=hour,
        message=message
    )
    return resp_data.dict()
