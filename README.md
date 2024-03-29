# Installer
这是一个快捷方便的 PenMods[^1] 安装程序，关于 PenMods 的介绍请看[这里](https://github.com/PenUniverse/PenMods-release)

### Noice
 - 这是安装程序而非升级程序，请勿对已修改过的系统使用此程序
 - Installer 需要 Win7 或更新版本的操作系统（参见pyinstaller[官方文档](https://pyinstaller.org/en/latest/requirements.html)）
 - Release 提供的版本打包自 `Installer.py`，您也可以使用 Python 3.8 及以上版本直接运行
 ```
 python Installer.py
 ```
 - 暂时不支持Linux

### Attention
```diff
- 这是免费项目，未经许可任何人不得使用本仓库的任何内容进行商业活动。
- 若您发现有人非法盗卖 PenMods，请立即向相关交易平台举报并申请退款，盗卖者的每一笔订单都使项目向死亡方向更进一步！
```

### Feature
 - 若`PATH`中没有adb，自动下载并安装
 - 根据型号等信息自动匹配合适的PenMods，自动下载
 - 自动根据已知的密码解锁词典笔

### Usage
 - 下载最新的 [Release](https://github.com/PenUniverse/Installer/releases) 版本
 - 准备好词典笔，双击 `start.cmd` 启动
 - 等候出现连接词典笔的提示，按照指引打开ADB
 - 根据指引和提示，等待程序执行完成即可（一般整个过程不超过1分钟）

### Contact Us
 - 遇到问题，请在 👉[这里](https://github.com/PenUniverse/PenMods-release/issues) 反馈，异常模块选择 `Installer`
 - 如果你觉得不错，请考虑捐赠 👉[爱发电](https://afdian.net/a/kbs007)'

[^1]: PenMods by [RedbeanW](https://github.com/Redbeanw44602)

