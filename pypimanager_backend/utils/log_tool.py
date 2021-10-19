#!/usr/bin/env python
# coding: utf-8
# @Created Date: 2021/10/18 下午3:28
# @Author: toddlerya
# -----
# @Last Modified: 2021/10/18 下午3:28
# @Modified By: toddlerya

import codecs
import datetime

from settings import NGINX_ACCESS_PYPI_PACKAGE_LOG


def extract_download_record():
    """
    提取nginx的packages路由下的下载日志
    Returns:

    """
    with codecs.open(NGINX_ACCESS_PYPI_PACKAGE_LOG, encoding='utf-8', mode='r') as r:
        for line in r:
            """
            一行日志的内容如下：
            10.1.14.67 -  [18/Oct/2021:14:56:52 +0800] "GET /pypi/packages/requests-2.26.0-py2.py3-none-any.whl 
            HTTP/1.1" 200 62251 "" "pip/20.1.1 
            {"ci":null,"cpu":"x86_64","distro":{"id":"focal","libc":{"lib":"glibc","version":"2.31"},
            "name":"Ubuntu","version":"20.04"},"implementation":{"name":"CPython","version":"3.7.9"},
            "installer":{"name":"pip","version":"20.1.1"},
            "openssl_version":"OpenSSL 1.1.1f  31 Mar 2020","python":"3.7.9",
            "setuptools_version":"47.1.0","system":{"name":"Linux","release":"5.11.0-27-generic"}}" ""
            """
            line = line.strip()
            sp_line = line.split()
            remote_ip = sp_line[0]
            download_datetime = sp_line[2][1:]
            package = sp_line[5][10:]
            client = ' '.join(sp_line[10:-1])[1:-1]
            # print(f'remote: {remote_ip} datetime {download_datetime} package {package} client {client}')
            if package:
                download_data = {
                    'download_ip': remote_ip,
                    'package': package,
                    'client': client,
                    'download_datetime': datetime.datetime.strptime(download_datetime, '%d/%b/%Y:%H:%M:%S')
                }
                yield download_data


if __name__ == '__main__':
    for i in extract_download_record():
        print(i)
