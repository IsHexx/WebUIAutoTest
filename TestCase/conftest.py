"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : conftest.py
@Author : putongrenji
@Time : 2022/5/4 11:17
@Motto:Don't ever let somebody tell you you can't do something
"""
import pytest
from selenium import webdriver
from utils.logger_util import LoggerUtil


@pytest.fixture(name='beginandend')
def beginToend():
    lu = LoggerUtil()
    logger = lu.get_logger()
    logger.info("----------测试用例执行开始----------")
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield (driver, logger)
    logger.info("----------测试用例执行结束----------\n")
    driver.quit()
    lu.remove_handler()