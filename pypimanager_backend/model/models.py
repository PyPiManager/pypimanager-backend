#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 10:05
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 10:05
# @Modified By: toddlerya


from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint, func, text, BigInteger
from sqlalchemy.orm import declarative_base, declared_attr, declarative_mixin

Base = declarative_base()


@declarative_mixin
class CommonTableArgsMixin:
    """
    公共表参数基础类
    """
    @declared_attr
    def __table_args__(cls):
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
    公共字段基础类
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
    username = Column(String(length=16), unique=True, index=True, nullable=False, comment='用户名')
    nickname = Column(String(length=32), nullable=False, comment='用户昵称')
    email = Column(String(length=32), unique=True, index=True, nullable=False, comment='用户邮箱')
    hashed_password = Column(String(length=128), nullable=False, comment='用户密码hash值')
    role = Column(String(length=16), ForeignKey('role.role_name'), nullable=False, comment='用户角色')
    disabled = Column(Boolean, nullable=False, default=False, comment='用户是否被禁用')


class Role(CommonTableArgsMixin, CommonColumnMixin, Base):
    """
    用户角色权限表
    """
    __tablename__ = 'role'
    __table_args_map__ = {
        'comment': '用户角色权限表'
    }
    role_name = Column(String(length=16), unique=True, nullable=False, comment='角色名称')
    role_desc = Column(String(length=32), nullable=False, comment='角色描述')
    upload = Column(Boolean, nullable=False, comment='上传权限')
    delete = Column(Boolean, nullable=False, comment='删除权限')
    user_manage = Column(Boolean, nullable=False, comment='用户管理权限')
    disabled = Column(Boolean, nullable=False, default=False, comment='角色是否被禁用')


class UploadRecord(CommonTableArgsMixin, CommonColumnMixin, Base):
    """
    用户上传记录表
    """
    __tablename__ = 'upload_record'
    __table_args_map__ = {
        'comment': '用户上传记录表'
    }
    upload_user = Column(String(length=16), ForeignKey('user.username'), nullable=False, comment='上传用户')
    package = Column(String(length=256), nullable=False, unique=True, index=True, comment='Python包名称')


class OperateRecord(CommonTableArgsMixin, CommonColumnMixin, Base):
    """
    管理员操作事件记录表
    """
    __tablename__ = 'operate_record'
    __table_args_map__ = {
        'comment': '管理员操作事件记录表'
    }
    operate_user = Column(String(length=16), ForeignKey('user.username'), nullable=False, comment='操作人')
    event = Column(String(length=512), nullable=False, comment='操作事件')


class DownloadRecord(CommonTableArgsMixin, Base):
    """
    用户下载记录表
    """
    __tablename__ = 'download_record'
    __table_args_map__ = {
        'comment': '用户下载记录表'
    }
    __table_args_array__ = [UniqueConstraint('download_ip', 'package', 'download_datetime', name='uk_download')]
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键')
    download_ip = Column(String(length=32), nullable=False, comment='下载用户IP')
    package = Column(String(length=256), nullable=False, comment='包名')
    client = Column(String(length=512), nullable=False, comment='客户端信息')
    download_datetime = Column(DateTime(timezone=False), nullable=False, server_default=func.now(), comment='创建时间')
