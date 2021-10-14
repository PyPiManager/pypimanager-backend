#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/14 下午3:55
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/14 下午3:55
# @Modified By: toddlerya


import pathlib

import aiofiles
from fastapi import Depends, File, UploadFile, HTTPException, status

import api.cruds.search as crud
from api.base import router, get_db
from api.auth import get_current_active_user
from api.schemas.base_schema import ResponseBase
from api.schemas.user import UserManage

from utils.db import DB
from utils.log import logger


@router.get("/search", response_model=ResponseBase)
async def search_package(package: str,
                         db: DB = Depends(get_db)):
    """
    查询Python包
    Args:
        package:
        current_user:
        db:

    Returns:

    """
    query_result, query_msg = crud.query_package(package, db)
    resp_data = ResponseBase(
        description='查询Python包',
        data=query_result,
        message=query_msg,
    )
    return resp_data.dict()

