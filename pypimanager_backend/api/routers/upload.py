#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/13 下午2:38
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/13 下午2:38
# @Modified By: toddlerya
import pathlib

import aiofiles
from fastapi import Depends, File, UploadFile, HTTPException, status

from api.base import router, get_db
from api.auth import get_current_active_user
from api.schemas.base_schema import ResponseBase
from api.schemas.user import UserManage
from api.cruds.upload import record_upload_event, query_package_owner
from utils.db import DB
from utils.twine_tool import twine_upload
from utils.log import logger
from utils.file_tool import delete_file


@router.post("/upload", response_model=ResponseBase, tags=['upload'])
async def upload(upload_file: UploadFile = File(..., description='上传的Python包文件'),
                 current_user: UserManage = Depends(get_current_active_user),
                 db: DB = Depends(get_db)):
    """
    上传Python包
    Args:
        upload_file:
        current_user:
        db:

    Returns:

    """
    resp_data = ResponseBase(
        description='上传Python包',
        data=False
    )
    username = current_user.username
    file_name = upload_file.filename
    package_owner = query_package_owner(package=file_name, db=db)
    # 当前上传的包有所属人，则进行逻辑判定：
    # 1. 本人上传过的文件，允许重复上传，进行覆盖更新
    # 2. 若不是本人上传过的，则不允许上传，给出提示信息
    # 以此保留记录上传用户的贡献度
    if package_owner is not None and username != package_owner:
        resp_data.message = '包已存在，无需重复上传'
        # raise HTTPException(
        #     status_code=status.HTTP_409_CONFLICT,
        #     detail=f'包已存在，无需重复上传',
        # )
    else:
        # 异步保存上传的文件到本地
        async with aiofiles.open(file_name, mode='wb') as save_file:
            content = await upload_file.read()
            await save_file.write(content)
        # 调用twines上传到pypiserver
        twine_status, twine_message = twine_upload(file_name)
        if twine_status:
            # 上传成功将此次结果记录到数据库中
            record_status, record_message = record_upload_event(username=username, package=file_name, db=db)
            if record_status:
                resp_data.data = True
                delete_file(pathlib.Path(file_name).absolute())
            else:
                logger.error(f'上传事件记录失败, 用户: {username}, 包: {file_name}, 错误信息: {record_message}')
                resp_data.message = '上传信息记录错误'
                delete_file(pathlib.Path(file_name).absolute())
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail=f'上传信息记录错误',
                )
        else:
            # 上传失败则不记录
            logger.error(f'twine上传失败, 用户: {username}, 错误信息: {twine_message}')
            resp_data.message = f'上传到PyPi服务错误: {twine_message}'
            delete_file(pathlib.Path(file_name).absolute())
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f'请确认Python包是否正确',
            )
    return resp_data.dict()
