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
import api.cruds.user as crud
from utils.db import DB
from utils.log import logger
from utils.error_code import error_code
from model.fixture import ADMIN_ROLE_NAME, USER_ROLE_NAME


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
    user = crud.get_user_info(username=token_data.username, db=db)
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
    user = crud.authenticate_user(form_data.username, form_data.password, db=db)
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
    user_info = crud.get_user_info(current_user.username, db=db)
    resp_data = ResponseBase(
        description='获取当前用户信息',
        data=user_info
    ).dict()
    return resp_data


@router.get("/all/user/info", response_model=ResponseBase)
async def read_all_user_info(current_user: UserManage = Depends(get_current_active_user), db: DB = Depends(get_db)):
    resp_data = ResponseBase(
        description='全部当前用户信息',
        data=None
    )
    current_user_user_info = crud.get_user_info(current_user.username, db=db)
    # 超管才有权限
    if current_user_user_info.role == ADMIN_ROLE_NAME:
        all_user_info = crud.get_all_user_info(db=db)
        resp_data.data = all_user_info
    return resp_data.dict()


@router.post("/password", response_model=ResponseBase)
async def update_user_password(username: str = Form(..., description='用户名称'),
                               old_pass: str = Form(None, description='旧密码'),
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
    current_user_info = crud.get_user_info(current_user.username, db=db)
    current_role = current_user_info.role
    # 如果是超管，可以修改任何用户的密码
    if current_role == ADMIN_ROLE_NAME:
        # 更新密码，让用户重新登录
        crud_status, curd_msg = crud.update_user_secret(username=username,
                                                        hashed_password=get_password_hash(password=new_pass),
                                                        db=db)
        if crud_status:
            resp_data.data = True
        else:
            resp_data.message = curd_msg
    # 不是超管，则只能修改当前用户的密码
    elif username == current_user_info.username:
        # 校验旧密码是否正确，防止其他用户修改密码
        if crud.authenticate_user(username=username, password=old_pass, db=db):
            # 旧密码校验通过，更新密码，让用户重新登录
            crud_status, curd_msg = crud.update_user_secret(username=username,
                                                            hashed_password=get_password_hash(password=new_pass),
                                                            db=db)
            if crud_status:
                resp_data.data = True
            else:
                resp_data.message = curd_msg
        else:
            resp_data.message = '旧密码错误'
    else:
        resp_data.message = '非超管用户只能修改自己的密码'
    return resp_data.dict()


@router.post("/role", response_model=ResponseBase)
async def update_user_role(username: str = Form(..., description='用户名称'),
                           role: str = Form(..., description='用户角色'),
                           current_user: UserManage = Depends(get_current_active_user),
                           db: DB = Depends(get_db)):
    """
    修改用户角色
    Args:
        username:
        role:
        current_user:
        db:

    Returns:

    """
    resp_data = ResponseBase(
        description='修改用户角色',
        data=False
    )
    current_user_info = crud.get_user_info(current_user.username, db=db)
    current_role = current_user_info.role
    # 如果是超管，可以继续执行
    if current_role == ADMIN_ROLE_NAME:
        crud_status, crud_message = crud.update_user_privilege(username=username, role=role, db=db)
        if crud_status:
            resp_data.data = True
        else:
            resp_data.message = crud_message
    else:
        resp_data.message = '非超管用户无权限操作'
    return resp_data.dict()


@router.post("/user/add", response_model=ResponseBase)
async def add_new_user(username: str = Form(..., description='用户名称'),
                       nickname: str = Form(..., description='用户昵称'),
                       email: str = Form(..., description='邮箱'),
                       password: str = Form(..., description='密码'),
                       role: str = Form(USER_ROLE_NAME, description='角色'),
                       current_user: UserManage = Depends(get_current_active_user),
                       db: DB = Depends(get_db)):
    """
    增加新用户
    Args:
        username:
        nickname:
        email:
        password:
        role:
        current_user:
        db:

    Returns:

    """
    resp_data = ResponseBase(
        description='新增用户',
        data=False
    )
    current_user_info = crud.get_user_info(current_user.username, db=db)
    current_role = current_user_info.role
    # 如果是超管，可以修改任何用户的密码
    if current_role == ADMIN_ROLE_NAME:
        # 更新密码，让用户重新登录
        crud_status, crud_message = crud.add_new_user(username=username,
                                                      nickname=nickname,
                                                      email=email,
                                                      hashed_password=get_password_hash(password=password), db=db,
                                                      role=role)
        if crud_status:
            resp_data.data = True
        else:
            resp_data.data = False
            resp_data.message = error_code.DB_INSERT_OR_UPDATE_ERROR.get('description')
            resp_data.status = error_code.DB_INSERT_OR_UPDATE_ERROR.get('code')
            logger.warning(crud_message)
    else:
        msg = '非超管用户无权限操作'
        resp_data.message = msg
    return resp_data.dict()
