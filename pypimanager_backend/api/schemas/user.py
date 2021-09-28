#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午10:15
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午10:15
# @Modified By: toddlerya


"""
用户信息以及用户认证
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, Extra

from model.fixture import USER_ROLE_NAME


class User(BaseModel, extra=Extra.forbid):
    """用户信息数据结构定义"""
    username: str = Field(..., description='用户名')
    nickname: str = Field(..., description='用户昵称')
    email: str = Field(..., description='用户邮箱')
    role: Optional[str] = Field(USER_ROLE_NAME, description='用户角色')
    disabled: Optional[bool] = Field(False, description='用户是否被禁用')


class UserSecret(User):
    """用户密码hash"""
    hashed_password: str = Field(..., description='用户密码hash值')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None