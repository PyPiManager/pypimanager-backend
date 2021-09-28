#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:02
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:02
# @Modified By: toddlerya


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import user

app = FastAPI(
    title='PyPiManager',
    description='就是好用',
    version='2.0.0'
)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(user.router)


@app.get('/')
async def root():
    return {'msg': 'Be Happy'}
