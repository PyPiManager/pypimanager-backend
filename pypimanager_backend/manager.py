#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午11:51
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午11:51
# @Modified By: toddlerya

import pathlib
import logging
import json

from uvicorn import Config, Server

from settings import LOG_LEVEL, PORT
from utils.log import logger, LogManager
from utils.db import DB
from api.server import app
from api.base import get_password_hash
from model.models import Role, User
from model.fixture import ROLE_MAP, USER_ROLE_NAME


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding loguru level if exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # Find caller from where originated the loggerd message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(handlers: list):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)
    # remove every other logger's handlers
    # and propagate a root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    # configure loguru
    logger.configure(handlers=handlers)


class Manager:
    def __init__(self):
        self.log_config = LogManager(
            base_path=str(pathlib.Path(__file__).parent.absolute()),
            log_path='log',
            log_name='pypimanager.log',
            file_log_level='INFO',
            console_log_level='INFO'
        ).get_config()
        self.db = DB()

    @logger.catch(reraise=True)
    def __load_role_map__(self):
        """
        更新用户角色配置
        """
        logger.info(f'共计{len(ROLE_MAP)}个角色配置')
        for role in ROLE_MAP:
            self.db.insert_or_update(Role, **role)
        self.db.session.commit()

    @logger.catch(reraise=True)
    def __load_fixtures_auth_users__(self):
        """
        导入存档的用户信息
        """
        with open(file=pathlib.Path(__file__).parent.absolute().joinpath('fixtures').joinpath('auth_users.json'),
                  mode='r', encoding='utf-8') as r:
            auth_users_data = json.load(r)
            for user in auth_users_data:
                # 默认为普通用户，密码123456
                if user.get('role', None) is None:
                    user.update({'role': USER_ROLE_NAME})
                user.update({'hashed_password': get_password_hash('123456')})
                self.db.insert_or_update(User, **user)
            self.db.session.commit()

    @logger.catch(reraise=True)
    def run_server(self):
        """
        启动API服务
        """
        self.__load_role_map__()
        m.__load_fixtures_auth_users__()
        server = Server(
            Config(
                app=app,
                host='0.0.0.0',
                port=PORT
            )
        )
        setup_logging(self.log_config['handlers'])
        server.run()


if __name__ == '__main__':
    m = Manager()
    m.run_server()
