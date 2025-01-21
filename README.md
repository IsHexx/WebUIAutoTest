## 项目概述

`WebUIAutoTest` 是一个基于 `Selenium + Pytest + POM`（页面对象模型）搭建的 Web UI 自动化测试框架。该框架旨在提供一个可维护、可扩展且易于使用的自动化测试解决方案，以帮助开发团队和测试人员更高效地进行 Web UI 的自动化测试工作。
## 目录结构

以下是本仓库的主要目录结构：


```plaintext
WebUIAutoTest/
├── README.md                 # 项目说明文档
├── config.yaml               # 全局配置文件
├── main.py                   # 项目主入口文件
├── requirements.txt          # 项目依赖库列表
├── run_test.py               # 运行测试的脚本文件
├── result/                   # 存储测试结果相关文件
│   ├── *.json                # 测试结果JSON文件
│   └── *.txt                 # 测试结果文本文件
├── TestCase/                 # 测试用例目录
│   ├── __init__.py           # 包初始化文件
│   └── conftest.py           # Pytest配置文件
├── data/                     # 测试数据目录
├── config/                   # 配置文件目录
├── .idea/                    # JetBrains系列IDE项目配置目录
├── pageobject/               # 页面对象模型目录
├── common/                   # 通用工具类目录
├── base/                     # 基础类目录
├── report/                   # 测试报告目录
├── logs/                     # 日志文件目录
└── utils/                    # 实用工具类目录
```

## 运行步骤

### 1. 克隆仓库

首先，将本仓库克隆到本地：


```sh
git clone https://github.com/IsHexx/WebUIAutoTest.git
cd WebUIAutoTest
```

### 2. 安装依赖

安装 `requirements.txt` 文件中列出的所有依赖库：


```sh
pip install -r requirements.txt
```

### 3. 配置文件

根据需要修改 `config.yaml` 文件中的配置信息，如测试环境的 URL、浏览器类型等。

### 4. 运行测试

运行 `run_test.py` 文件启动测试：


```sh
python run_test.py
```

## 主要技术栈

* **Selenium**：用于模拟用户在 Web 浏览器中的操作，实现 Web UI 的自动化测试。
* **Pytest**：一个功能强大的 Python 测试框架，方便编写和管理测试用例，支持测试用例的参数化、测试夹具等功能。
* **POM（页面对象模型）** ：将页面元素和操作封装成类，提高代码的复用性和可维护性。

## 项目特点

* **模块化设计**：采用模块化的设计思想，将不同功能的代码封装在不同的模块中，提高代码的可维护性和可扩展性。
* **易于使用**：通过简单的配置和命令即可运行测试，降低了使用门槛。
* **丰富的报告**：测试运行后会生成详细的测试报告，方便查看测试结果和分析问题。

## 贡献指南

如果你发现了任何问题或者有改进的建议，欢迎提交 Issue 或者 Pull Request。在提交 Pull Request 之前，请确保你的代码符合项目的代码规范和风格。## 许可证

本项目使用 [MIT License](https://opensource.org/licenses/MIT) 许可证。
