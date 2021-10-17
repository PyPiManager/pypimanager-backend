#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/17 下午3:27
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/17 下午3:27
# @Modified By: toddlerya

from utils.log import logger
from utils.db import DB
from model.models import UploadRecord, OperateRecord


@logger.catch(reraise=True)
def delete_package_from_db(package: str, operate_username: str, db: DB):
    """
    删除Python包，将该包的状态修改为禁用，用户必须精确到传入一个包文件名
    Args:
        package:
        operate_username：
        db:

    Returns:

    """
    message = 'ok'
    status = True
    try:
        # 查询要删除的包信息
        delete_package_info = db.session.query(UploadRecord.upload_user,
                                               UploadRecord.package,
                                               UploadRecord.create_time,
                                               UploadRecord.update_time,
                                               UploadRecord.remark).filter(UploadRecord.package == package).one()
        operate_record = {
            'operate_user': operate_username,
            'event': f'删除包: {delete_package_info}'
        }
        try:
            db.insert_or_update(OperateRecord, **operate_record)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            return False, f"记录用户操作日志失败: {err}"
        else:
            db.session.query(UploadRecord).filter(UploadRecord.package == package).delete()
    except Exception as err:
        message = f'查询待删除的包失败: {package}, 错误信息: {err}'
        logger.warning(message)
        status = False
    return status, message
