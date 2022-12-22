#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: __init__.py.py
@ide: PyCharm
@time: 2020/7/31
"""
import json
import re
from string import Template

import allure

from jsonpath import jsonpath
from loguru import logger

from tools.hooks import *


def exec_func(func: str) -> str:
    """执行函数(exec将字符转化为Python语句，用于执行Python代码)
    :params func 字符的形式调用函数
    : return 返回的将是个str类型的结果
    """
    # 之前的处理方法
    # 得到一个局部的变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
    # loc = locals()
    # exec(f"result = {func}")
    # return str(loc['result'])

    # 现在的方法
    # eval() 函数将去掉两个引号，去掉引号的作为python语句执行，之前的字符串将会被其解释为一个变量，
    # 由于之前没有定义过hello变量，解释器会报错，所以这里使用两层引号
    # 不加双层引号跑 pytest框架能运行，暂不知道这里逻辑

    return str(eval(f"{func}"))


def extractor(obj: dict, expr: str = '.') -> object:
    """
    根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    $.0.1 提取字典中的第一个列表中的第二个的值
    """
    try:
        result = jsonpath(obj, expr)[0]
    except Exception as e:
        logger.error(f'{expr} - 提取不到内容，丢给你一个错误！{e}')
        result = expr
    return result


def rep_expr(content: str, data: dict) -> str:
    """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
    :param content: 原始的字符串内容
    :param data: 提取的参数变量池
    return content： 替换表达式后的字符串
    """
    # 替换${}模板类型的原始字符串
    content = Template(content).safe_substitute(data)
    for func in re.findall('\\${(.*?)}', content):
        try:
            # 执行${}中的函数，并返回执行结果进行替换
            # replace添加参数1保证只替换一次，修复多次调用同一函数时值相同的bug
            content = content.replace('${%s}' % func, exec_func(func),1)
            logger.info(f"exec_func(func),{exec_func(func)}")
            logger.info(f"content,{content}")
        except Exception as e:
            logger.error(e)
    return content


def convert_json(dict_str: str) -> dict:
    """
    :param dict_str: 长得像字典的字符串
    return json格式的内容
    """
    try:
        if 'None' in dict_str:
            dict_str = dict_str.replace('None', 'null')
        elif 'True' in dict_str:
            dict_str = dict_str.replace('True', 'true')
        elif 'False' in dict_str:
            dict_str = dict_str.replace('False', 'false')
        dict_str = json.loads(dict_str)
    except Exception as e:
        if 'null' in dict_str:
            dict_str = dict_str.replace('null', 'None')
        elif 'true' in dict_str:
            dict_str = dict_str.replace('true', 'True')
        elif 'false' in dict_str:
            dict_str = dict_str.replace('false', 'False')
        dict_str = eval(dict_str)
        logger.error(e)
    return dict_str


def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(
            json.dumps(
                var,
                ensure_ascii=False,
                indent=4),
            step,
            allure.attachment_type.JSON)


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass

def he():
    s = "123das"
    print("hello 1")
    return s


if __name__ == '__main__':
    # print(exec_func(random_choice("aaa,bbb,ccc")))
    print(exec_func(random_int("1,100")))
    # print(exec_func(he()))