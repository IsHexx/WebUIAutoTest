#!/usr/bin/env python
# -*-coding:utf-8 -*-
import time
import traceback

import allure
import pytest
from common.excle_export import excle_read
from pageobject.table_commit import LoginPage


@pytest.mark.usefixtures('beginandend')
@allure.feature('测试360搜索')
class Testtable:

    #@pytest.mark.skip('测试阶段')
    @pytest.mark.usefixtures('beginandend')
    @pytest.mark.parametrize("data", excle_read('./data/ele.xlsx', 'Sheet1'))
    def test_table_01(self, data, beginandend):
        num, Full_Name, case_description, result = data
        self.driver, self.logger = beginandend
        lp = LoginPage(self.driver)
        lp.login_echop(Full_Name)
        # 断言
        # if "登录成功" in case_description:
        #     # print(lp.get_except_result_access())
        #     assert lp.get_except_result_access() in result
        #     self.logger.info(case_description)
        # elif "登录失败" in case_description:
        #     # print(lp.get_except_result_fail())
        #     time.sleep(1)
        #     assert lp.get_except_result_fail() in result
        #     self.logger.info(case_description)






