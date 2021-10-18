#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/18 下午5:37
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/18 下午5:37
# @Modified By: toddlerya

from collections import OrderedDict

from sqlalchemy import func, distinct

from utils.log import logger
from utils.db import DB
from model.models import DownloadRecord, UploadRecord


@logger.catch(reraise=True)
def stat_download_trend(db: DB):
    """
    统计每天的下载数据量，用于渲染折线图
    Args:
        db:

    Returns:

    """
    message = 'ok'
    day_count_map = OrderedDict()
    dat_count_value = 0
    try:
        day_download_count_result = db.session.query(
                                        func.count(DownloadRecord.id).label('day_download_count'),
                                        func.DATE(DownloadRecord.download_datetime)
                                    ).group_by(
                                        func.DATE(DownloadRecord.download_datetime)
                                    ).all()
    except Exception as err:
        message = f'获取每日下载量统计数据失败，错误信息: {err}'
        logger.error(message)
    else:
        # 累加之前每天都数据，统计下载量逐天递增
        for each_day in day_download_count_result:
            each_day_date = each_day[1]
            each_day_count = each_day[0]
            dat_count_value += each_day_count
            day_count_map[each_day_date] = dat_count_value
    return message, day_count_map


@logger.catch(reraise=True)
def stat_total_file_count(db: DB):
    """
    统计上传的文件总数
    Args:
        db:

    Returns:

    """
    message = 'ok'
    count = 0
    try:
        count = db.session.query(func.count(UploadRecord.package)).scalar()
    except Exception as err:
        message = f'统计上传文件总数失败: {err}'
        logger.error(message)
    return message, count


@logger.catch(reraise=True)
def stat_download_user_count(db: DB):
    """
    统计累计下载用户数量
    Args:
        db:

    Returns:

    """
    message = 'ok'
    count = 0
    try:
        count = db.session.query(func.count(distinct(DownloadRecord.download_ip))).scalar()
    except Exception as err:
        message = f'统计累计下载用户数量失败: {err}'
        logger.error(message)
    return message, count


@logger.catch(reraise=True)
def stat_download_total_count(db: DB):
    """
    统计下载总量
    Args:
        db:

    Returns:

    """
    message = 'ok'
    count = 0
    try:
        count = db.session.query(func.count(DownloadRecord.id)).scalar()
    except Exception as err:
        message = f'统计下载总量失败: {err}'
        logger.error(message)
    return message, count
