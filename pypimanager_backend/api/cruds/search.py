#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/14 下午3:58
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/14 下午3:58
# @Modified By: toddlerya


from utils.log import logger
from utils.db import DB
from utils.algo import fuzzy_match
from model.models import UploadRecord, User
from settings import PYPI_BASE_PACKAGE_URL


@logger.catch(reraise=True)
def query_package(package: str, db: DB):
    """
    从数据库模糊匹配查询可能的Python包
    Args:
        package:
        db:

    Returns:

    """
    # 先通过LIKE查询数据库，缩小匹配范围，更精确
    package_data = dict()
    message = '未查询到相似包，欢迎补充上传哦~'
    try:
        like_query_data = db.session.query(UploadRecord.package).filter(UploadRecord.package.like(f'%{package}%')).all()
    except Exception as err:
        logger.warning(f'未查询到相似Python包: {package}, 错误信息: {err}')
    else:
        # 如果数据库匹配有结果，则进行模糊匹配，按相似度排序，并生成结果
        if like_query_data:
            package_data = gen_package_search_result(package=package,
                                                     package_array=like_query_data,
                                                     db=db,
                                                     threshold=0.0)
        # 数据库没匹配中，则获取全部包，进行相似度匹配给出个低相关性的推荐结果
        else:
            all_query_data = db.session.query(UploadRecord.package).all()
            package_data = gen_package_search_result(package=package,
                                                     package_array=all_query_data,
                                                     db=db,
                                                     threshold=0.4)
    if package_data:
        message = 'ok'
    return package_data, message


def gen_package_search_result(package: str, package_array: tuple, db: DB, threshold=0.4):
    """
    模糊匹配评分排序，生成包查询到结果
    Args:
        package
        package_array:
        db:
        threshold:

    Returns:

    """
    package_data = list()
    package_list = [each[0] for each in package_array]
    fuzzy_list = fuzzy_match(package, package_list, threshold=threshold)
    for index, each in enumerate(fuzzy_list):
        package_name = list(each.values())[0]
        package_url = PYPI_BASE_PACKAGE_URL + package_name
        # upload_nick_name = {"nickname": "郭群"}
        upload_nick_name = db.session.query(User.nickname). \
            filter(UploadRecord.package == package_name,
                   UploadRecord.upload_user == User.username).first()
        package_data.append({'index': index + 1, 'package_name': package_name, 'url': package_url, **upload_nick_name})
    return package_data
