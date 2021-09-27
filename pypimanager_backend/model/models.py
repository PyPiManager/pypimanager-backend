#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 10:05
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 10:05
# @Modified By: toddlerya


from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, UniqueConstraint, func, text, inspect
from sqlalchemy.orm import declarative_base, declared_attr, declarative_mixin

Base = declarative_base()


@declarative_mixin
class CommonTableArgsMixin:

    @declared_attr
    def __table_args__(cls):
        print(cls.__dict__)
        args = list()
        __args_map__ = {
                'mysql_charset': 'utf8mb4',
                'mysql_collate': 'utf8mb4_unicode_ci'
            }
        if cls.__dict__.get('__table_args_map__'):
            __args_map__.update(cls.__table_args_map__)
        if cls.__dict__.get('__table_args_array__'):
            args.extend(cls.__table_args_array__)
        args.append(__args_map__)
        return tuple(args)


@declarative_mixin
class CommonColumnMixin:
    """
    基础模型公共字段基础类
    """
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    remark = Column(String(length=128), default='', comment='备注')
    create_time = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime(timezone=False), nullable=False,
                         server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment='更新时间')


class User(CommonTableArgsMixin, CommonColumnMixin, Base):
    """
    用户信息表
    """
    __tablename__ = 'user'
    __table_args_map__ = {
        'comment': '用户信息表',
    }
    username = Column(String(length=16), unique=True, index=True, comment='用户名')
    nickname = Column(String(length=32), nullable=False, comment='用户昵称')
    email = Column(String(length=32), nullable=False, index=True, comment='用户邮箱')
    password_hash = Column(String(length=128), nullable=False, comment='用户密码hash值')
