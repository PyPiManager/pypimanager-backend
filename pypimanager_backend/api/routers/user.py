#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:40
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:40
# @Modified By: toddlerya


from datetime import timedelta

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.base import oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, router, get_db
from api.schemas.base_schema import ResponseBase
from api.schemas.user import TokenData, UserBase, UserManage
from api.cruds.user import get_user_info, authenticate_user
from utils.db import DB


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


async def get_current_active_user(current_user: UserManage = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=ResponseBase)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: DB = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        # resp_data = ResponseBase(
        #     description='登录以获取令牌',
        #     status=error_code.HTTP_401_UNAUTHORIZED_ERROR.get('code'),
        #     message=error_code.HTTP_401_UNAUTHORIZED_ERROR.get('description')
        # ).dict()
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        resp_data = ResponseBase(
            description='登录以获取令牌',
            data={"access_token": access_token, "token_type": "bearer"}
        ).dict()
    return resp_data


@router.get("/users/me/", response_model=ResponseBase)
async def read_users_me(current_user: UserManage = Depends(get_current_active_user)):
    resp_data = ResponseBase(
        description='获取当前用户信息',
        data=current_user
    ).dict()
    return resp_data


@router.get("/users/me/items/")
async def read_own_items(current_user: UserBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


