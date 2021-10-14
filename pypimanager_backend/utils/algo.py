#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/14 下午4:12
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/14 下午4:12
# @Modified By: toddlerya


import difflib
import re
from collections import defaultdict, OrderedDict


def fuzzy_match(key, value_list, threshold=0.2):
    """
    根据目标关键字，匹配相似文本，评分最高的相似度最高
    Args:
        key:
        value_list:
        threshold:

    Returns:

    """
    threshold = float(threshold)
    diff_value_map = defaultdict(list)
    for item in value_list:
        re_extract_prefix = re.split(r'-\d.*', item)[0]
        seq = difflib.SequenceMatcher(None, key, re_extract_prefix).quick_ratio()
        diff_value_map[seq].append(item)
    order_dict = OrderedDict(sorted(diff_value_map.items(), reverse=True))
    limit_result = list()
    for i in order_dict.items():
        if i[0] >= threshold:
            for each in i[1]:
                each_dict = {
                    i[0]: each
                }
                limit_result.append(each_dict)
    return limit_result
