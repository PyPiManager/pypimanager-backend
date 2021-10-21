#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/15 下午3:50
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/15 下午3:50
# @Modified By: toddlerya

from fastapi import Depends

import api.cruds.rank as crud
from api.base import router, get_db
from api.schemas.base_schema import ResponseBase
from utils.db import DB


@router.get('/rank', response_model=ResponseBase, tags=['rank'])
async def rank(limit: int = 0, db: DB = Depends(get_db)):
    """
    获取排行榜数据
    Args:
        limit
        db:

    Returns:

    """
    message, result = crud.stat_user_upload_count(limit_num=limit, db=db)
    resp_data = ResponseBase(
        description='查询用户上传贡献统计数据',
        data=result,
        message=message
    )
    return resp_data.dict()


@router.get('/rank/person/detail', response_model=ResponseBase, tags=['rank'])
async def detail(username: str, db: DB = Depends(get_db)):
    """
    查询用户上传详情数据
    Args:
        username:
        db:

    Returns:

    """
    message, result = crud.query_person_upload_detail(username, db)
    resp_data = ResponseBase(
        description='查询用户上传详情数据',
        data=result,
        message=message
    )
    return resp_data.dict()
