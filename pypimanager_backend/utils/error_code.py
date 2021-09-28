#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/09/27 03:04
# @Author: toddlerya
# -----
# @Last Modified: 2021/09/27 03:04
# @Modified By: toddlerya

class ErrorCode:
    """
    错误码指定原则:
    1. 快速溯源
    2. 简单易记
    3. 沟通标准化

    错误类型 + 错误编号

    错误类型:
        A --> 输入参数错误
        B --> 数据处理错误
        C --> 文件操作错误
        D --> 数据库错误
        E --> 网络请求错误

    错误编号:
        四位数字
        大类之间步长间距为100
    """

    def __init__(self):
        self.DEFAULT = {
            'code': '00000',
            'description': 'ok'
        }

        self.ARGS_MISS_ERROR = {
            'code': 'A1000',
            'description': '参数项缺失错误'
        }

        self.ARGS_NOT_FOUND_ERROR = {
            'code': 'A2000',
            'description': '参数值未找到'
        }

        self.DB_CONNECT_ERROR = {
            'code': 'D0000',
            'description': '数据库连接失败'
        }

        self.DB_INSERT_OR_UPDATE_ERROR = {
            'code': 'D1000',
            'description': '数据库INSERT or UPDATE错误'
        }

        self.DB_SQL_EXECUTE_ERROR = {
            'code': 'D2000',
            'description': '数据库SQL执行错误'
        }

        self.DB_SAFE_CHECK_ERROR = {
            'code': 'D3000',
            'description': '数据库查询SQL安全检查不通过'
        }

        self.HTTP_401_UNAUTHORIZED_ERROR = {
            'code': 'E4010',
            'description': '用户名或密码错误'
        }


error_code = ErrorCode()
