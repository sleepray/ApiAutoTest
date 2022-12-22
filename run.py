#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: run.py
@ide: PyCharm
@time: 2020/12/16
@github: https://github.com/zy7y
@site: https://cnblogs.com/zy7y
@desc: 运行文件
"""

import os
import shutil
from test.conftest import pytest
from tools import logger
from tools.read_file import ReadFile
from tools.send_email import EmailServe

file_path = ReadFile.read_config('$.file_path')
email = ReadFile.read_config('$.email')


def run():
    if os.path.exists('report/'):
        #递归的删除文件
        shutil.rmtree(path='report/')

    # 不输出到控制台
    logger.remove()
    logger.add(file_path['log'], enqueue=True, encoding='utf-8',retention=10) # retention 保留日志数量
    logger.info("""
                 _    _         _      _____         _
  __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
 / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
| (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
 \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
      |_|
      Starting      ...     ...     ...
    """)
    pytest.main(
        args=[
            '-sv', #显示执行进度
            'test/test_api.py',
            f'--alluredir={file_path["report"]}/data'])

    # 自动以服务形式打开报告
    # os.system(f'allure serve {file_path["report"]}/data')

    # 本地生成报告
    os.system(
        f'allure generate {file_path["report"]}/data -o {file_path["report"]}/html --clean')
    logger.success('报告已生成')

    # # 发送邮件带附件报告
    # EmailServe.send_email(email, file_path['report'])
    #
    # # 删除本地附件
    # os.remove(email['enclosures'])


if __name__ == '__main__':
    run()
