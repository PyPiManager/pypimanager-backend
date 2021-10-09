#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:02
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:02
# @Modified By: toddlerya

from typing import Optional
from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt


from utils.log import logger
from utils.db import DB

from settings import SQLALCHEMY_URL, SQLALCHEMY_ECHO, SQLALCHEMY_AUTO_FLUSH, SQLALCHEMY_AUTO_COMMIT


router = APIRouter(
    # prefix='/pypimanager/v1',
    responses={404: {'description': 'Not Found'}}
)


@logger.catch(reraise=True)
def get_db():
    db = DB(url=SQLALCHEMY_URL,
            echo=SQLALCHEMY_ECHO,
            auto_flush=SQLALCHEMY_AUTO_FLUSH,
            auto_commit=SQLALCHEMY_AUTO_COMMIT)
    try:
        yield db
    finally:
        db.session.close()


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "e9c39eb9f9e900e0acfe97681b6dbbdec23d830fcb62b9e57a0470f469247f47"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password: str, hashed_password: str):
    """
    校验密码
    Args:
        plain_password(str): 明文密码
        hashed_password(str): 密码hash值

    Returns: bool

    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """
    获取密码hash值
    Args:
        password: 密码明文

    Returns:

    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
