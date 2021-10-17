#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/15 下午2:11
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/15 下午2:11
# @Modified By: toddlerya


import requests
from lxml import etree
from fastapi import Form, Depends, HTTPException, status

from api.base import router, get_db
from api.auth import get_current_active_user
from api.schemas.base_schema import ResponseBase
from api.schemas.user import UserManage
from api.cruds.package import delete_package_from_db
from model.fixture import ADMIN_ROLE_NAME, MANAGE_ROLE_NAME
from settings import PYPI_SIMPLE_INDEX_URL
from utils.log import logger
from utils.db import DB
from utils.twine_tool import twine_delete


def get_pypi_simple_index():
    """
    获取pypi simple 索引信息
    Returns:

    """
    __status = False
    data = list()
    message = "ok"
    try:
        resp = requests.get(PYPI_SIMPLE_INDEX_URL)
    except Exception as err:
        message = f'无法访问pypi simple index: {err}'
        logger.error(message)
    else:
        if resp.status_code != 200:
            message = f'pypi simple index服务异常: {resp.status_code}'
            logger.error(message)
        else:
            content = resp.text.encode('utf-8')
            html = etree.HTML(content)
            __data = html.xpath('//a/text()')
            data = [{'package': ele} for ele in __data]
            __status = True
    return __status, message, data


@router.get("/package", response_model=ResponseBase, tags=['package'])
async def get_package_info():
    """
    获取全部包概览信息
    Returns:

    """
    __status, message, data = get_pypi_simple_index()
    resp_data = ResponseBase(
        description='获取simple索引信息',
        data=data,
        message=message,
        status=__status
    )
    return resp_data.dict()


@router.post('/package/delete', response_model=ResponseBase, tags=['package'])
async def delete_package(package: str = Form(..., description='待删除的Python包名称'),
                         current_user: UserManage = Depends(get_current_active_user),
                         db: DB = Depends(get_db)):
    """
    删除Python包
    Args:
        package:
        current_user:
        db:

    Returns:

    """
    logger.warning(f'正在执行删除操作！操作人: {current_user.username} {current_user.nickname} {current_user.role} '
                   f'删除对象: {package}')
    # 普通用户无权删除
    if current_user.role not in [MANAGE_ROLE_NAME, ADMIN_ROLE_NAME]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no privilege",
        )
    delete_status, delete_message = delete_package_from_db(package, current_user.username, db)
    resp_data = ResponseBase(
        description='删除Python包',
        data=delete_status,
        message=delete_message
    )
    # 将Python包从pypiserver的索引区移动到回收站
    __recycle_status, __recycle_message = twine_delete(package)
    if __recycle_status is True:
        # 移动到回收站成功，提交事物
        db.session.flush()
        db.session.commit()
    else:
        # 否则回滚
        db.session.rollback()
        resp_data.data = False,
        resp_data.message = __recycle_message
    return resp_data.dict()
