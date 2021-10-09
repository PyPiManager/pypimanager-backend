#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:22
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:22
# @Modified By: toddlerya

from fastapi.encoders import jsonable_encoder

from utils.log import logger
from utils.db import DB
from model.models import User
from api.schemas.user import UserSecret, UserManage
from api.base import verify_password


@logger.catch(reraise=True)
def get_user_info(username: str, db: DB):
    """
    获取用户信息
    Args:
        db:
        username:

    Returns:

    """
    try:
        user_dict = db.session.query(User).filter(User.username == username).one()
    except Exception as err:
        logger.error(f'获取用户信息失败, username: {username}, 错误信息: {err}')
        return None
    else:
        if user_dict:
            return UserManage(**jsonable_encoder(user_dict))
        else:
            return None


@logger.catch(reraise=True)
def get_user_secret(username: str, db: DB):
    """
    获取用户密码hash
    Args:
        db:
        username:

    Returns:

    """
    try:
        user_dict = db.session.query(User).filter(User.username == username).one()
    except Exception as err:
        logger.error(f'查询用户信息失败, username: {username}, 错误信息: {err}')
        return None
    else:
        if user_dict:
            return UserSecret(**jsonable_encoder(user_dict))
        else:
            return None


def authenticate_user(username: str, password: str, db: DB):
    """
    认证用户
    Args:
        username:
        password:
        db:

    Returns:

    """
    user = get_user_secret(username, db=db)
    if not user:
        return False
    elif not verify_password(password, user.hashed_password):
        return False
    else:
        return user
