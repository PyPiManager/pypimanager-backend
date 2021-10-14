#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 11:39
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 11:39
# @Modified By: toddlerya

import logging

LOG_LEVEL = logging.getLevelName("INFO")


# MySQL Config
MYSQL_DRIVER = 'pymysql'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_HOST = '192.168.41.4'
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

# PYPIServer Config
PYPI_REPOSITORY = 'http://192.168.41.3:8080'
PYPI_USERNAME = 'admin'
PYPI_PASSWORD = 'pypiadmin'
PYPI_BASE_PACKAGE_URL = f'{PYPI_REPOSITORY}/packages/'
