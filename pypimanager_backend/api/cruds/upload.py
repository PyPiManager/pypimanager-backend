#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/13 下午2:39
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/13 下午2:39
# @Modified By: toddlerya


from fastapi.encoders import jsonable_encoder

from utils.log import logger
from utils.db import DB
from model.models import UploadRecord
from model.fixture import USER_ROLE_NAME
from api.schemas.user import UserSecret, UserManage, UserInfo
from api.base import verify_password


@logger.catch(reraise=True)
def record_upload_event(username: str, package: str, db: DB):
    """
    记录Python包上传记录
    Args:
        username:
        package:
        db:

    Returns:

    """
    record = {
        'upload_user': username,
        'package': package
    }
    try:
        db.insert_or_update(UploadRecord, **record)
    except Exception as err:
        db.session.rollback()
        message = f'记录上传事件失败, username: {username}, package: {package} 错误信息: {err}'
        return False, message
    else:
        db.session.commit()
        return True, ''
