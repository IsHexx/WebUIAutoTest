# Selenium+Pytest+POM+Excle数据驱动

#### 前言

使用的技术框架：Selenium+Pytest+POM+Excle数据驱动

本文所述框架特点
1.代码与测试数据完全分离，可以做到不懂代码的测试人员也可以参与到自动化测试过程（测试用例与代码没有强关联）。
2.使用Excel管理测试用例，与手工测试用例编写方式相同。
3.基于关键字驱动方式，可以对关键字扩展满足更复杂的测试场景。

理解本文所述的内容你需要
1.掌握一定的python基础-至少明白类与对象、封装、继承
2.需要有一定的selenium基础-至少掌握八种定位方式

#### 整体目录

| 目录/文件   | 说明                                    | 是否为py包 |      |
| ----------- | --------------------------------------- | ---------- | ---- |
| base        | 存放对selnium方法的二次封装             | y          |      |
| common      | 存放通用的类，如读取excle文件、配置文件 | y          |      |
| config      | 配置文件目录                            | y          |      |
| data        | 测试数据都放在这里                      | n          |      |
| logs        | 日志目录                                | n          |      |
| pageobject  | 页面对象封装                            | y          |      |
| TestCase    | 所有测试用例集                          | y          |      |
| utile       | 工具集                                  | y          |      |
| config.yaml | 测试地址、密码、log路径存放             | n          |      |
|             |                                         |            |      |

<u>上面是一个这个框架简单的结构，在开始之前先按照上面的指引建好每一项目录</u>

#### 添加配置文件

​	配置文件在项目中是不可缺少的部分，将整个项目中固定不变的信息存放至固定文件中有利于项目后续的维护

​	在项目主目录创建config.yaml,测试地址、测试密码、账号、log路径都配置在这里

```yaml
##浏览器选择(不区分大小写，谷歌浏览器：Chrome；火狐浏览器：Firefox；IE浏览器:Ie)
browser:
    browser_name: Chrome

#全局基本路径和被测项目地址
url:
    ui_test_url: https://mail.163.com/  #UI被测项目地址，我这里放的是163邮箱登录地址

#全局日志格式设置（分别为日志文件前缀，文件日志级别，文件日志格式，控制台日志级别，控制台日志格式）日志级别共五级（不区分大小写，默认为INFO）：DEBUG,INFO,WARNING,ERROR,CRITICAL
log:
    log_name: log_
    file_log_level: info
    file_log_format: '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s'
    console_log_level: info
    console_log_format: '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s'

#全局框架报告设置（报告文件名称设置）
report:
    report_name: report_

#UI：前端登录默认的用户名和密码
default_login:
    username: admin  #测试进行前需要将这里改成自己测试使用的账号
    password: abc12345	#测试进行前需要将这里改成自己测试使用的账号
```

#### 读取配置文件

​	配置文件创建完成后，我们需要读取配置，在config目录下建一个config_util.py文件。

```python
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import yaml
from selenium import webdriver


# 全局
def get_project_path():
    '''全局：获得项目路径'''
    realpath = os.path.dirname(os.path.dirname(__file__))
    return realpath


# 读取yaml配置文件
def get_yaml_config(one_name,two_name):
    '''全局：读取全局配置yaml文件'''
    with open(str(get_project_path())+'\\' + 'config.yaml','r',encoding='utf-8') as f:
        # cfg = yaml.load(f.read(), Loader=yaml.FullLoader)
        cfg=yaml.safe_load(f.read())
        return cfg[one_name][two_name]


# 获得配置文件config.ini中的浏览器信息，返回driver对象。
def get_config_browser():
    browserName = get_yaml_config('browser','browser_name')
    global driver
    if browserName.lower() == "chrome":
        driver = webdriver.Chrome()
    elif browserName.lower() == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Ie()
    return driver


if __name__ == '__main__':
    print(get_project_path())
    print(get_yaml_config("browser","browser_name"))
    # get_config_browser()
```

#### 记录操作日志

​	日志，是一个项目中非常重要的部分，详细准确的日志可以帮我我们快速定位程序出错的地点。在自动化测试过程中一个用例执行是需要多个步骤，记录用例执行步骤可以很好的帮助我们回溯测试过程。

​	在utils目录下新建一个文件logger_util.py文件

```python

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import time
from utils.config_util import get_project_path, get_yaml_config


class LoggerUtil:
    # 初始化文件和控制台的日志对象，日志级别，日志文件路径，日志格式等。
    def __init__(self, loggerName = 'ceshi'):
        # 创建一个logger,loggerName就是给这个logger起一个名字。
        self.logger = logging.getLogger(loggerName)
        # 获取全局日志级别为DEBUG
        self.logger.setLevel(logging.DEBUG)
        # 设置日志文件的输入路径和名称
        self.log_path = get_project_path()+ '\\' + 'logs\\'
        self.log_time = time.strftime("%Y_%m_%d")
        self.log_path_and_name = self.log_path+get_yaml_config('log','log_name')+self.log_time+'.log'
        # 创建文件和控制台日志处理器
        self.file_handler = None
        self.console_handler = None

    # 创建文件日志
    def create_file_log(self):
        # 使用FileHandler创建文件日志处理器对象，向指定文件输出日志信息。
        print(self.log_path_and_name)
        self.file_handler=logging.FileHandler(self.log_path_and_name,encoding='utf-8')
        # 设置日志处理器日志级别
        fileLogLevel = get_yaml_config('log','file_log_level')
        if fileLogLevel.lower() == 'debug':
            self.file_handler.setLevel(logging.DEBUG)
        elif fileLogLevel.lower() == 'info':
            self.file_handler.setLevel(logging.INFO)
        elif fileLogLevel.lower() == 'warning':
            self.file_handler.setLevel(logging.WARNING)
        elif fileLogLevel.lower() == 'error':
            self.file_handler.setLevel(logging.ERROR)
        elif fileLogLevel.lower() == 'critical':
            self.file_handler.setLevel(logging.CRITICAL)
        else:
            self.file_handler.setLevel(logging.INFO)
        # 设置日志处理器的日志格式
        self.formatter = logging.Formatter(get_yaml_config('log','file_log_format'))
        self.file_handler.setFormatter(self.formatter)
        # 将日志处理器加入日志对象。
        self.logger.addHandler(self.file_handler)

    # 创建控制台日志
    def create_console_log(self):
        # 使用StreamHandler可以向类似与sys.stdout或者sys.stderr的任何文件对象输出信息。
        self.console_handler=logging.StreamHandler()
        # 设置日志处理器的日志级别
        consoleLogLevel = get_yaml_config('log','console_log_level')
        if consoleLogLevel.lower() == 'debug':
            self.console_handler.setLevel(logging.DEBUG)
        elif consoleLogLevel.lower() == 'info':
            self.console_handler.setLevel(logging.INFO)
        elif consoleLogLevel.lower() == 'warning':
            self.console_handler.setLevel(logging.WARNING)
        elif consoleLogLevel.lower() == 'error':
            self.console_handler.setLevel(logging.ERROR)
        elif consoleLogLevel.lower() == 'critical':
            self.console_handler.setLevel(logging.CRITICAL)
        else:
            self.console_handler.setLevel(logging.INFO)
        # 设置日志处理器的日志格式
        self.formatter = logging.Formatter(get_yaml_config('log','console_log_format'))
        self.console_handler.setFormatter(self.formatter)
        # 将日志处理器加入日志对象。
        self.logger.addHandler(self.console_handler)

    #从日志对象中移除日志处理器。（防止日志重写）
    def remove_handler(self):
        # 关闭日志处理器输出流和移除日志处理器
        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)
        # 关闭日志处理器输出流和移除日志处理器
        self.console_handler.close()
        self.logger.removeHandler(self.console_handler)

    #获得日志对象
    def get_logger(self):
        self.create_file_log()
        self.create_console_log()
        return self.logger

if __name__ == '__main__':
    logger = LoggerUtil().get_logger()
    logger.info("普通信息")
    logger.debug("调试信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误")
```

#### POM设计模式

​		Selenium二次封装以及将页面封装成类（Page Object）这两种思想都是POM设计模式的重要组成部分，所以在这里不得不介绍一下POM设计模式。

​	POM设计模式是用来维护一组web元素集的对象库，这种设计模式是非常有利于庞大的UI自动化项目。

​	了解过Selenium的读者应该知道，基于Python Selenium2开始UI自动化并不是什么艰巨的任务。只要定位到元素，执行对应的操作就可以。

```python
from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.implicitly_wait(30)

# 启动浏览器，访问百度
driver.get("http://www.baidu.com")

# 定位 百度搜索框，并输入selenium
driver.find_element_by_id("kw").send_keys("selenium")

# 定位 百度一下 按钮并单击进行搜索
driver.find_element_by_id("su").click()
time.sleep(5)

driver.quit()
```

​	上述代码是初次尝试使用Selenium写代码都会经历的阶段吧！从代码上看，我们所能做的就是定位到元素，然后键盘输入或鼠标动作。就这个小程序，维护起来看起来是很容易的，简单明了初次写完颇具成就感。然而随着我们尝试用这个方式写更多的用例时会发现，用例越写越多，代码越来越臃肿。

我们需要考虑：这样的代码我们该如何维护？一个元素变动每个用例都更改一次？当一个元素定位失效我们该如何排查......

​	上面说了这么多其实都是为了引出我们的POM模型，在本文中所述的这套框架按照POM模型将Selenium二次封装，再将每个页面元素及元素操作封装成一个类。

##### Selenium二次封装

在base目录下新建一个base_page.py文件

```python
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    # 加载网页
    def get(self, url):
        self.driver.get(url)

    # 定位元素
    def locate_element(self,args):
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(args), '没找到元素')
        return self.driver.find_element(*args)

    # 窗口最大化
    def maxWindows(self):
        self.driver.maximize_window()

    # 设置元素等待
    def element_Wait(self, args, secs=10):
        WebDriverWait(self.driver, secs, 0.5).until(EC.presence_of_element_located(args), '没找到元素')

    # 等待元素消失
    def element_Wait_disappear(self, args, secs=10):
        WebDriverWait(self.driver, secs).until_not(EC.presence_of_element_located(args), '没找到元素')

    # 设置值
    def send_keys(self,args,value):
        self.locate_element(args).send_keys(value)

    # 清空输入框
    def clear(self, args):
        self.element_Wait(args)
        self.locate_element(args).clear()

    # 按下Enter键
    def Enter(self,args):
        self.element_Wait(args)
        self.locate_element(args).send_keys(Keys.ENTER)

    # 单击
    def click(self, args):
        self.locate_element(args).click()

    # 移动鼠标到指定元素(默认在元素的中间位置)
    def movetotargetelement(self, args):
        self.element_Wait(args)
        ActionChains(self.driver).move_to_element(self.locate_element(args)).perform()

    # 进入iframe
    def goto_frame(self, frame_name):
        self.driver.switch_to.frame(self.locate_element(frame_name))

    # 多次进入iframe
    def goto_frame_mult(self, *frame_name):
        if not frame_name:
            print("请传入iframe定位方式和元素标志")
        else:
            value_str = ",".join(str(x) for x in frame_name)
            self.out_frame()
            for i in frame_name:
                self.driver.switch_to.frame(self.locate_element(i))

    # 返回iframe主窗口
    def out_frame(self):
        self.driver.switch_to.default_content()

    # 返回iframe父窗口
    def out_frame_parent(self):
        self.driver.switch_to.parent_frame()

    # 下拉框
    def choice_select_by_value(self, args, value):
        Select(self.locate_element(args)).select_by_visible_text(value)

    # 执行指定的js代码
    def js(self, jsScript):
        # jsScript = ("arguments[0].removeAttribute('readonly');", self.locate_element(args))
        self.driver.execute_script(jsScript)

    # 获取文本值
    def get_value(self, args):
        return self.locate_element(args).text

    # 获取元素属性值
    def get_attribute(self, args, attributevalues):
        return self.locate_element(args).get_attribute(attributevalues)

    # 关闭弹窗
    def alertClose(self):
        self.driver.switch_to.alert.accept()

    # 弹框警告-确认
    def alertAccept(self):
        self.driver.switch_to.alert.accept()

    # 弹框警告-取消
    def alertDismiss(self):
        # self.driver.switch_to_alert().dismiss() 废弃的方式
        self.driver.switch_to.alert.dismiss()

    # 判断元素是否存在
    def is_element_exist(self, args):
        flag = True
        try:
            self.locate_element(args)
            return flag
        except:
            flag = False
            return flag

    # 关闭浏览器驱动
    def quit(self):
        self.driver.quit()
```

##### 页面对象封装PageObject

​	在pageobject下新建table_commit.py文件存放页面元素定位方式以及页面操作步骤

```python
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
```

#### 测试数据存放与读取

​	无论编写代码将代码和数据分离都是明智之举，显然自动化测试也需要这样做。在本文所述的这套框架中，我们使用存放数据的方式是Excle。

​	在本文介绍的框架中存放数据的目录是“data”,你也可以选择放在其他位置，只要你能找到就可以。

​	数据存放好之后需要在我们代码运行的时候能够读取到，这里使用到了‘openpyxl’模块。

​	请在common目录下新建excle_export.py文件

```python
import  openpyxl

def excle_read(excle_url, sheet_name):
    # 加载工作薄
    wb = openpyxl.load_workbook(excle_url)
    # 获取sheet对象
    sheet = wb[sheet_name]
    # 获取最大行和最大列
    all_list = []
    for row in range(2, sheet.max_row+1):
        row_list=[]
        for column in range(1, sheet.max_column+1):
            row_list.append(sheet.cell(row, column).value)
        all_list.append(row_list)
    return all_list
```

#### 测试用例TestCase

​	数据、页面对象、定位方式都已封装完成，就可以开始我们测试用例的编写了。

​	在编写用例时我们使用到了pytest，关于pytest内容这里不做介绍。有关教程可以在官网<http://www.pytest.org/en/latest/>或者https://www.cnblogs.com/yoyoketang/tag/pytest/，找到相关资料。

​	在TestCase目录新建文件test_table.py

```python
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
```

#### conftest.py文件

​	conftest.py是pytest用作前后置方法编写用到的文件，里面用到了fixture的方法，封装并传递出了driver。

```pytest
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from selenium import webdriver
from utils.config_util import get_config_browser
from utils.logger_util import LoggerUtil


@pytest.fixture(name = 'beginandend')
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
```

#### 运行程序

​	用例执行结束后结果是我们需要得到的最终产出物，也就是测试报告，这里我们使用allure来生成比较直观的测试报告，在执行用例前请先安装allure插件。allure安装教程地址：https://zhuanlan.zhihu.com/p/375592805

​	以上我们已经完成了测试框架的搭建与测试用例的编写运行主目录下的run_test.py文件我们的用例就开始执行了

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import pytest

if __name__ == '__main__':
    pytest.main(['-vs', './TestCase', '--alluredir=./result', '-n=5', '--reruns=2'])
    time.sleep(1)
    os.system('allure generate ./result -o ./report --clean')
```

#### 发送邮件

```txt
很遗憾，发送邮件代码还没有开发出来,敬请期待后续补充......
```

#### 后期扩展

```txt
在本套框架中仍然有许多需要完善的部分，在一个自动化测试项目中我们还需要补充以下几部分：
1.测试用例执行过程中的详细日志，需要在logs文件和Allure报告中体现出来。
2.对测试用例执行结束之后数据图表化。
3.增加jenkins+Git持续集成管理代码。
4.可以根据项目中工具使用的数量考虑是否开发Web应用。
5.编写明确的代码命名规范文档，有利于编码顺利进行、后期维护。
```

#### 结语

​	到这里这个框架介绍结束，如果将本套框架能够在项目中运用起来，相信你在自动化测试的道路上又上了一层台阶

#### 参考文献

```
文笔借鉴：https://www.cnblogs.com/wxhou/p/selenium-pytest-test-framework.html
https://www.cnblogs.com/lym51/p/6646033.html

```

