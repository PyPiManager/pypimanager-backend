#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:22
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:22
# @Modified By: toddlerya


from api.schemas.user import UserSecret
from api.base import verify_password


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "nickname": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def get_user(username: str):
    """
    获取用户信息
    Args:
        username:

    Returns:

    """
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserSecret(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
