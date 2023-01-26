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
        WebDriverWait(self.driver, 30, 0.5).until(EC.presence_of_element_located(args), '没找到元素')
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

    # 获取文本
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