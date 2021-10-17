#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/15 下午3:52
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/15 下午3:52
# @Modified By: toddlerya


from sqlalchemy import func, desc

from utils.log import logger
from utils.db import DB
from model.models import UploadRecord, User
from settings import PYPI_BASE_PACKAGE_URL


def stat_user_upload_count(db: DB):
    """
    统计用户上传数量
    Args:
        db:

    Returns:

    """
    user_upload_count_data = list()
    message = 'ok'
    try:
        user_upload_count_data = db.session.query(User.nickname,
                                                  User.username,
                                                  func.count(UploadRecord.package).label('count')) \
            .filter(UploadRecord.upload_user == User.username). \
            group_by(UploadRecord.upload_user). \
            order_by(desc('count')).all()
    except Exception as err:
        message = f'统计错误: {err}'
        logger.error(message)
    return message, user_upload_count_data


def query_person_upload_detail(username: str, db: DB):
    """
    查询用户上传详情数据
    Args:
        username:
        db:

    Returns:

    """
    detail_data = list()
    message = 'ok'
    try:
        data = db.session.query(UploadRecord.package, User.nickname). \
            filter(UploadRecord.upload_user ==
                   username, User.username == username,
                   User.username == UploadRecord.upload_user).filter(UploadRecord.deleted is False).all()
    except Exception as err:
        message = f'查询用户上传详情失败: {err}'
    else:
        for each in data:
            each_data = dict(each)
            package_url = PYPI_BASE_PACKAGE_URL + each.package
            each_data.update({'url': package_url})
            detail_data.append(each_data)
    return message, detail_data
