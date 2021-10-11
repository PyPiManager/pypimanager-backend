#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:40
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:40
# @Modified By: toddlerya

from datetime import timedelta

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from api.base import oauth2_scheme, create_access_token, router, get_db, get_password_hash, SECRET_KEY, ALGORITHM, \
    ACCESS_TOKEN_EXPIRE_MINUTES
from api.schemas.base_schema import ResponseBase
from api.schemas.user import TokenData, UserManage, Token
from api.cruds.user import get_user_info, authenticate_user, update_user_secret
from utils.db import DB
from utils.log import logger


async def get_current_user(token: str = Depends(oauth2_scheme), db: DB = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_info(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    _ = await get_current_user(token)
    return token


async def get_current_active_user(current_user: UserManage = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: DB = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/info/", response_model=ResponseBase)
async def read_user_info(current_user: UserManage = Depends(get_current_active_user), db: DB = Depends(get_db)):
    user_info = get_user_info(current_user.username, db=db)
    resp_data = ResponseBase(
        description='获取当前用户信息',
        data=user_info
    ).dict()
    return resp_data


@router.post("/password", response_model=ResponseBase)
async def update_user_password(username: str = Form(..., description='用户名称'),
                               old_pass: str = Form(..., description='旧密码'),
                               new_pass: str = Form(..., description='新密码'),
                               current_user: UserManage = Depends(get_current_active_user),
                               db: DB = Depends(get_db)):
    """
    更新指定的用户密码
    Args:
        username: 需要修改密码的用户名
        old_pass: 旧密码
        new_pass: 新密码
        current_user:
        db:

    Returns:

    """
    resp_data = ResponseBase(
        description='修改用户密码',
        data=False
    )
    current_user_info = get_user_info(current_user.username, db=db)
    current_role = current_user_info.role
    # 如果是超管，可以修改任何用户的密码
    if current_role == "ADMIN_ROLE_NAME":
        # 更新密码，让用户重新登录
        if update_user_secret(username=username, hashed_password=get_password_hash(password=new_pass), db=db):
            resp_data.data = True
    # 不是超管，则只能修改当前用户的密码
    elif username == current_user_info.username:
        # 校验旧密码是否正确
        if authenticate_user(username=username, password=old_pass, db=db):
            # 旧密码校验通过，更新密码，让用户重新登录
            if update_user_secret(username=username, hashed_password=get_password_hash(password=new_pass), db=db):
                resp_data.data = True
        else:
            resp_data.message = '旧密码错误'
    else:
        msg = '非超管用户只能修改自己的密码'
        resp_data.message = msg
    return resp_data.dict()
