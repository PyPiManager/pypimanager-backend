#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 10:10
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 10:10
# @Modified By: toddlerya


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base

from pypimanager_backend.settings import SQLALCHEMY_URL, SQLALCHEMY_ECHO, SQLALCHEMY_AUTO_FLUSH, SQLALCHEMY_AUTO_COMMIT
from pypimanager_backend.utils.log import logger


Base = declarative_base()


class DB:
    @logger.catch(reraise=True)
    def __init__(self):
        """
        初始化数据库对象
        """
