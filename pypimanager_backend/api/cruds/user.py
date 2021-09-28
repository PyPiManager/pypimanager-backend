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
    user_dict = db.session.query(User).filter(User.username == username).one()
    if user_dict:
        return UserManage(**jsonable_encoder(user_dict))


@logger.catch(reraise=True)
def get_user_secret(username: str, db: DB):
    """
    获取用户密码hash
    Args:
        db:
        username:

    Returns:

    """
    user_dict = db.session.query(User).filter(User.username == username).one()
    if user_dict:
        return UserSecret(**jsonable_encoder(user_dict))


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
    if not verify_password(password, user.hashed_password):
        return False
    return user
