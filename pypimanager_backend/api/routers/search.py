#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/14 下午3:55
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/14 下午3:55
# @Modified By: toddlerya

from fastapi import Depends

import api.cruds.search as crud
from api.base import router, get_db
from api.schemas.base_schema import ResponseBase
from utils.db import DB


@router.get("/search", response_model=ResponseBase, tags=['search'])
async def search_package(package: str,
                         db: DB = Depends(get_db)):
    """
    查询Python包
    Args:
        package:
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
