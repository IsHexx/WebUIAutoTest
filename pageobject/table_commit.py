"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Author : putongrenji
@Time : 2022/4/25 15:41
"""
import time

from selenium.webdriver.common.by import By
from base.base_page import BasePage
from config.config_util import get_yaml_config


class LoginPage(BasePage):

    # 页面元素定位
    full_name = (By.XPATH, '//*[@id="input"]')
    submit = (By.XPATH, '//*[@id="search-button"]')
    url = get_yaml_config('url', 'ui_test_url')

    # 元素动作
    def login_echop(self, fullname):

        # self.open_browser()
        self.get(self.url)
        self.send_keys(self.full_name, fullname)
        self.click(self.submit)
        time.sleep(1)

    # 登录成功断言
    def get_except_result_access(self):
        self.element_Wait(LoginPage.comm_access)
        return self.get_value(LoginPage.comm_access)

    # 登录失败断言
    def get_except_result_fail(self):
        self.element_Wait(LoginPage.login_fail)
        return self.get_value(LoginPage.login_fail)