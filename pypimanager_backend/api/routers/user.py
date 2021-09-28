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

from api.base import oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, router
from api.schemas.user import TokenData, Token, UserBase
from api.cruds.user import get_user, authenticate_user


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: UserBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


