Hash Checker 哈希校对器

一款基于 CustomTkinter 开发的跨平台图形化哈希校验工具，支持文本、单文件、文件夹全量差分扫描三种工作模式，内置 MD5 / SHA1 / SHA256 / SHA512 主流算法，异步多线程计算不阻塞 UI，支持主题自定义与 CSV 报告导出。

当前版本：v1.0 | 许可证：MIT | 适用系统：Windows /macOS/ Linux

✨ 功能特性

三大比对模式

文本比对：两段文本实时 SHA256 哈希计算与一致性校验

文件比对：支持双文件双向哈希比对，也支持文件与已知哈希字符串单向指纹校验

文件夹比对：跨目录全量文件差分扫描，自动识别缺失文件、内容不一致文件，支持单目录批量哈希生成

多算法支持：内置 MD5 / SHA1 / SHA256 / SHA512 四种主流哈希算法

异步无卡顿：所有哈希计算均在守护线程执行，界面实时显示扫描进度百分比

主题自定义：支持 System / Dark / Light 三种外观模式，blue /dark-blue/green 三套配色，配置自动持久化

结果可导出：文件夹比对结果支持一键导出 CSV 完整报告，包含全量文件哈希与比对状态

轻量单文件：核心逻辑全部集成在单个 Python 文件中，开箱即用

📋 环境要求

Python 3.11 及以上版本（依赖标准库 hashlib.file\_digest API）

第三方依赖：customtkinter

🚀 快速开始

1\. 安装依赖

bash

运行

pip install -r requirements.txt

或手动安装：

bash

运行

pip install customtkinter

2\. 运行程序

bash

运行

python main.py

📖 使用说明

文本比对

切换至「文本比对」标签页

在两个输入框中分别粘贴待比对的文本内容

点击「开始比对」，即可查看两段文本的 SHA256 哈希值与一致性结果

文件比对

切换至「文件比对」标签页

选择文件 A（待校验文件）

文件 B 处可选择另一个文件进行双向比对，也可直接粘贴已知哈希字符串进行单向指纹校验

下拉选择哈希算法，点击「开始比对」查看结果

文件夹比对

切换至「文件夹比对」标签页

分别选择目录 A 与目录 B；仅填写目录 A 时为单目录哈希批量生成模式

下拉选择哈希算法，点击「跨目录差分扫描」开始计算

扫描完成后，结果列表优先展示差异文件，可选择导出完整 CSV 报告

界面列表中哈希值仅展示前后 6 位，完整哈希请查看导出的 CSV 文件

差异项超过 1000 条时，界面默认截断显示，导出文件包含全部数据

主题配置

界面右上角可切换外观主题与配色方案

配置自动保存至程序同目录下的 config.ini 文件，下次启动自动加载

📁 项目结构与文件命名规范

如果你计划参与代码修改、提交 PR，请严格遵循以下命名与目录约定，保持项目风格统一。

当前项目结构（v1.0 单文件版本）

plaintext

hash-checker/

├── main.py              # 程序主入口，包含全部 UI 与业务逻辑

├── requirements.txt     # 项目依赖清单

├── README.md            # 项目说明文档

├── LICENSE              # 开源许可证

└── .gitignore           # Git 忽略规则

文件命名通用规则

Python 源码文件：统一使用 snake\_case（小写下划线） 命名，全小写，单词间用下划线分隔，见名知意。

正确示例：hash\_utils.py、ui\_components.py、file\_scanner.py

错误示例：HashUtils.py、fileScanner.py、中文文件名

目录名称：全小写，单词间可用下划线分隔，功能语义清晰。

推荐目录：ui/（界面模块）、utils/（工具函数）、assets/（静态资源）、core/（核心逻辑）

配置与资源文件：

运行时自动生成的文件（如 config.ini、日志、缓存）统一加入 .gitignore，不提交到仓库

静态图标、主题文件放入 assets/ 目录

示例文件、测试数据放入 examples/ 目录

文档类文件：首字母大写，其余小写，单词间短横线分隔。

示例：README.md、CHANGELOG.md、CONTRIBUTING.md

禁止项：文件名禁止使用中文、空格、特殊符号（!@#$% 等），避免跨系统兼容问题。

后续模块拆分建议

如果后续功能扩展需要拆分代码，推荐按以下分层结构组织：

plaintext

hash-checker/

├── main.py              # 程序入口

├── core/

│   ├── hash\_calculator.py   # 哈希计算核心逻辑

│   └── folder\_scanner.py    # 文件夹扫描与比对逻辑

├── ui/

│   ├── main\_window.py       # 主窗口

│   └── tabs/                # 各标签页组件

├── utils/

│   ├── config\_manager.py    # 配置读写

│   └── csv\_exporter.py      # CSV 导出

├── assets/                  # 图标、主题资源

├── requirements.txt

└── README.md

🛠️ 开发指南

代码架构说明

当前 v1.0 为单文件架构，核心分为三层：

UI 层：\_setup\_ui、\_build\_\*\_tab 系列方法，负责界面渲染与交互

业务层：calc\_file\_hash、scan\_folder\_hashes、on\_compare\_\* 系列方法，负责哈希计算与比对逻辑

控制层：start\_thread、write\_log 等工具方法，负责线程调度、日志输出与配置管理

依赖管理

新增第三方依赖时，请同步更新 requirements.txt

优先使用 Python 标准库实现功能，减少外部依赖，保持项目轻量

customtkinter 为核心 UI 依赖，建议兼容 ≥ 5.0 版本

本地开发流程

Fork 本仓库到自己的 GitHub 账号

克隆到本地：git clone https://github.com/你的用户名/hash-checker.git

创建开发分支：git checkout -b feature/你的功能名

修改代码并完成自测

提交代码，提交信息遵循语义化规范：

feat: 新增xxx功能

fix: 修复xxxbug

docs: 更新文档

perf: 优化性能

🤝 贡献指南

欢迎提交 Issue 和 Pull Request 参与项目改进！

可贡献方向

修复 Bug、优化大文件扫描性能

新增哈希算法、新增比对功能

优化界面交互、新增主题配色

补充代码注释、完善使用文档

跨平台打包适配、兼容性优化

提交 PR 注意事项

提交前请确保代码可正常运行，无语法错误与明显逻辑问题

保持代码风格与原项目一致，缩进统一使用 4 空格

单个 PR 尽量只完成一件事，避免功能、修复、文档混合提交

PR 描述请写清楚修改内容、解决的问题，涉及界面改动建议附上截图

📦 打包说明

可使用 PyInstaller 将程序打包为独立可执行文件：

bash

运行

pip install pyinstaller

pyinstaller -F -w main.py

打包完成后，可执行文件位于 dist 目录下。

⚠️ 注意事项

大文件或文件数量极多的目录扫描时，请耐心等待进度完成

程序运行时会在可执行文件同目录生成 config.ini 用于保存主题配置

CSV 导出默认使用 utf-8-sig 编码，Excel 打开可正常显示中文

📄 许可证

本项目基于 MIT License 开源，你可以自由使用、修改、分发，详见 LICENSE 文件。

