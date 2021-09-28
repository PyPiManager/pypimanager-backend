#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/9/28 下午3:31
# @Author: toddlerya
# -----
# @Last Modified: 2021/9/28 下午3:31
# @Modified By: toddlerya


from typing import Any

from pydantic import BaseModel, Field, Extra

from utils.error_code import error_code


class ResponseBase(BaseModel, extra=Extra.forbid):
    """响应体结构定义"""
    description: str = Field(..., description='描述信息')
    status: str = Field(error_code.DEFAULT.get('code'), description='响应数据系统状态码')
    message: str = Field(error_code.DEFAULT.get('description'), description='错误信息')
    data: Any = Field(None, description='响应数据内容')
