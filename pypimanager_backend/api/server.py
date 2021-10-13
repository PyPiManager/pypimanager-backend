#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:02
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:02
# @Modified By: toddlerya

import pathlib

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.routers import user
from api.routers import upload

app = FastAPI(
    title='PyPiManager',
    description='就是好用',
    version='2.0.0',
    docs_url=None,
    redoc_url=None
    )

__api_path__ = pathlib.Path(__file__).parent.absolute()

app.mount('/static', StaticFiles(directory=__api_path__.joinpath('static').absolute()), name='static')

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
app.include_router(upload.router)


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + '- Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger-ui.css',
        swagger_favicon_url='/static/favicon.png'
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get('/redoc', include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + '- ReDoc',
        redoc_js_url='/static/redoc.standalone.js'
    )


@app.get('/')
async def root():
    return {'msg': 'Be Happy'}
