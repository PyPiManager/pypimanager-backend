#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/13 下午2:38
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/13 下午2:38
# @Modified By: toddlerya

import aiofiles
from fastapi import Depends, Form, File, UploadFile


from api.base import router, get_db, get_current_active_user
from api.schemas.base_schema import ResponseBase
from api.schemas.user import UserManage
from api.cruds.upload import record_upload_event
from utils.db import DB
from utils.twine_tool import twine_upload

from utils.log import logger
from utils.error_code import error_code
from model.fixture import ADMIN_ROLE_NAME, USER_ROLE_NAME


@router.post("/upload", response_model=ResponseBase)
async def upload(upload_file: UploadFile = File(..., description='上传的Python包文件'),
                 current_user: UserManage = Depends(get_current_active_user),
                 db: DB = Depends(get_db)):
    resp_data = ResponseBase(
        description='上传Python包',
        data=False
    )
    # TODO 校验用户是否有上传权限
    username = current_user.username
    file_name = upload_file.filename
    content_type = upload_file.content_type
    # 异步保存上传的文件到本地
    async with aiofiles.open(file_name, 'wb') as save_file:
        content = await upload_file.read()
        await save_file.write(content)
    # 调用twines上传到pypiserver
    twine_status, twine_message = twine_upload(file_name)
    if twine_status:
        # 上传成功将此次结果记录到数据库中
        record_status, record_message = record_upload_event(username=username, package=file_name, db=db)
        if record_status:
            resp_data.data = True
        else:
            logger.error(f'上传事件记录失败, 用户: {username}, 包: {file_name}, 错误信息: {record_message}')
            resp_data.message = '上传信息记录错误'
    else:
        # 上传失败则不记录
        logger.error(f'twine上传失败, 用户: {username}, 包: {file_name}, 错误信息: {twine_message}')
        resp_data.message = '上传到PyPi服务错误'
    return resp_data.dict()
