#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/18 下午5:05
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/18 下午5:05
# @Modified By: toddlerya

import datetime


def last_day_of_month(any_day):
    """
    获取每月的最后一天日期
    Args:
        any_day:

    Returns:

    """
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


