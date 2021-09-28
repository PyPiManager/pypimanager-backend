#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 上午10:50
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 上午10:50
# @Modified By: toddlerya


USER_ROLE_NAME = '用户'
MANAGE_ROLE_NAME = '包管理员'
ADMIN_ROLE_NAME = '超级管理员'

ROLE_MAP = [
    {
        'role_name': USER_ROLE_NAME,
        'role_desc': '普通用户',
        'upload': True,
        'delete': False,
        'user_manage': False
    },
    {
        'role_name': MANAGE_ROLE_NAME,
        'role_desc': '有包的删除管理权限',
        'upload': True,
        'delete': True,
        'user_manage': False
    },
    {
        'role_name': ADMIN_ROLE_NAME,
        'role_desc': '至高无上的超管',
        'upload': True,
        'delete': True,
        'user_manage': True
    }
]