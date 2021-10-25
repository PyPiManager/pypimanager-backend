#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 11:39
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 11:39
# @Modified By: toddlerya

import logging
import pathlib

LOG_LEVEL = logging.getLevelName("INFO")


# MySQL Config
MYSQL_DRIVER = 'pymysql'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_HOST = 'pypi_mysql'
MYSQL_PORT = '3306'
DB_NAME = 'pypimanager'
CHARSET = 'utf8mb4'

# SQLAlchemy Config
SQLALCHEMY_URL = f'mysql+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB_NAME}?charset={CHARSET}'
SQLALCHEMY_ECHO = False
SQLALCHEMY_AUTO_FLUSH = True
SQLALCHEMY_AUTO_COMMIT = False


# API Config
PORT = 5000

# PATH Config
PROJECT_ROOT_PATH = pathlib.Path(__file__).parent.parent.parent.absolute()

# PYPIServer Config
PYPI_REPOSITORY = 'http://pypi_server:8080'
PYPI_USERNAME = 'admin'
PYPI_PASSWORD = 'pypiadmin'
PYPI_BASE_PACKAGE_URL = f'{PYPI_REPOSITORY}/packages/'
PYPI_SIMPLE_INDEX_URL = f'{PYPI_REPOSITORY}/simple/'
PYPI_DATA_PATH = str(PROJECT_ROOT_PATH.joinpath('pypiserver/packages').absolute())
PYPI_RECYCLE_BIN_PATH = str(PROJECT_ROOT_PATH.joinpath('pypiserver/recycle_bin').absolute())

# NGINX Config
NGINX_ACCESS_PYPI_PACKAGE_LOG = str(PROJECT_ROOT_PATH.joinpath('pypimanager-nginx/logs/access.pypi.packages.log').absolute())
