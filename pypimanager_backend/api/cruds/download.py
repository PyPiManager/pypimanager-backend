#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/18 下午4:41
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/18 下午4:41
# @Modified By: toddlerya

from utils.log import logger
from utils.db import DB
from utils.log_tool import extract_download_record
from model.models import DownloadRecord


@logger.catch(reraise=True)
def load_download_record(db: DB):
    """
    将从日志中提取的下载信息入库用于统计
    Returns:

    """
    for record in extract_download_record():
        try:
            db.insert_or_update(DownloadRecord, **record)
        except Exception as err:
            logger.error(f'下载日志信息入库失败! 待入库数据: {record}, 错误信息: {err}')
            db.session.rollback()
            return False
    # 若无报错，则在入库完成后提交事务
    db.session.flush()
    db.session.commit()
    return True


