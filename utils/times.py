"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : hbcjsutotest1.1
@File : times.py
@Author : lsXiangHe
@Time : 2022/4/29 18:32
@Motto:Don't ever let somebody tell you you can't do something
"""
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import datetime
from functools import wraps


def timestamp():
    """时间戳"""
    return time.time()


def dt_strftime(fmt="%Y%m"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    """
    time.sleep(seconds)


def running_time(func):
    """函数运行时间"""

    """"在我们使用了装饰器函数之后，我们的被装饰函数默认指向了装饰器的名字（内存地址）"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        """
        *args就是就是传递一个可变参数列表给函数实参，这个参数列表的数目未知，甚至长度可以为0。
        **kwargs则是将一个可变的关键字参数的字典传给函数实参，同样参数列表长度可以为0或为其他值
        """
        res = func(*args, **kwargs)
        print("Done！用时%.3f秒！" % (timestamp() - start))
        return res

    return wrapper


if __name__ == '__main__':
    print(dt_strftime("%Y%m%d%H%M%S"))
