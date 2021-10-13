#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/13 下午4:17
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/13 下午4:17
# @Modified By: toddlerya

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from api.schemas.user import TokenData, UserManage
from api.cruds.user import query_user_info
from api.base import oauth2_scheme, get_db, DB, SECRET_KEY, ALGORITHM


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
    user = query_user_info(username=token_data.username, db=db)
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
