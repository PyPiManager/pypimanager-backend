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
from model.fixture import USER_ROLE_NAME
from api.schemas.user import UserSecret, UserManage, UserInfo
from api.base import verify_password


@logger.catch(reraise=True)
def query_user_info(username: str, db: DB):
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
def get_all_user_info(db: DB):
    """
    获取全部用户信息
    Args:
        db:

    Returns:

    """
    try:
        all_user_data = db.session.query(User).all()
    except Exception as err:
        logger.error(f'获取全部用户信息失败, 错误信息: {err}')
        return None
    else:
        if all_user_data:
            data = list()
            for index, user in enumerate(all_user_data):
                each_user_data = UserInfo(**jsonable_encoder(user))
                each_user_data.index = index + 1
                data.append(each_user_data)
            return data
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


def update_user_secret(username: str, hashed_password: str, db: DB):
    """
    更新用户密码hash
    Args:
        username:
        hashed_password:
        db:

    Returns:

    """
    try:
        user = db.session.query(User).filter(User.username == username).one()
        user.hashed_password = hashed_password
        db.session.flush()
        db.session.commit()
    except Exception as err:
        message = f'查询用户信息失败, username: {username}, 错误信息: {err}'
        return False, message
    else:
        return True, ""


@logger.catch(reraise=True)
def update_user_privilege(username: str, role: str, db: DB):
    """
    更新用户角色以赋予新的权限
    Args:
        username:
        role:
        db:

    Returns:

    """
    try:
        user = db.session.query(User).filter(User.username == username).one()
        user.role = role
        db.session.flush()
        db.session.commit()
    except Exception as err:
        message = f'查询用户信息失败, username: {username}, 错误信息: {err}'
        return False, message
    else:
        return True, ""


@logger.catch(reraise=True)
def add_new_user(db: DB,
                 username: str,
                 nickname: str,
                 email: str,
                 hashed_password: str,
                 role: str = USER_ROLE_NAME
                 ):
    """
    增加新用户
    Args:
        db:
        username:
        nickname:
        email:
        hashed_password:
        role:

    Returns:

    """
    new_user_data = {
        "username": username,
        "nickname": nickname,
        "email": email,
        "hashed_password": hashed_password,
        "role": role
    }
    try:
        db.insert_or_update(User, **new_user_data)
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        return False, f"新增用户失败: {err}"
    else:
        return True, ''

