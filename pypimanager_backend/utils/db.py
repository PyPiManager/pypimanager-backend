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
    def __init__(self, url: str=None, echo: bool=None, auto_flush: bool=None, auto_commit: bool=None):
        """
        初始化sqlalchemy数据库对象化

        Args:
            url (str, optional): 数据库连接串. Defaults to None.
            echo (bool, optional): 是否打印SQL执行详情. Defaults to None.
            auto_flush (bool, optional): 是否自动flush. Defaults to None.
            auto_commit (bool, optional): 是否自动commit. Defaults to None.
        """
        if not url:
            url = SQLALCHEMY_URL
        if not echo:
            echo = SQLALCHEMY_ECHO
        if not auto_flush:
            auto_flush = SQLALCHEMY_AUTO_FLUSH
        if not auto_commit:
            auto_commit = SQLALCHEMY_AUTO_COMMIT

        self.__engine = create_engine(url=url, echo=echo, future=True)
        __session_class = sessionmaker(bind=self.__engine, autoflush=auto_flush, autocommit=auto_commit)
        self.session = __session_class()

    @logger.catch(reraise=True)
    def insert_or_update(self, model_name, **kwargs):
        """
        使用SQL的ON DUPLICATE KEY UPDATE语法

        Args:
            model_name (str): 模型类名
        """
        if not kwargs:
            return
        insert_stmt = mysql.insert(getattr(model_name, '__table__')).values(kwargs)
        update_stmt = insert_stmt.on_duplicate_key_update(**kwargs)
        self.session.execute(update_stmt)

