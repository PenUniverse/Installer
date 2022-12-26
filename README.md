# Installer
这是一个快捷方便的PenMods安装程序，关于PenMods的介绍请看[这里](https://github.com/PenUniverse/PenMods-release)

### Noice
 - 这是安装程序而非升级程序，请勿对已修改过的系统使用此程序
 - Installer 需要 Win8 或更新版本的操作系统（参见pyinstaller[官方文档](https://pyinstaller.org/en/latest/requirements.html)）
 - Release 提供的版本打包自 `Installer.py`，您也可以使用 Python 3.8 及以上版本直接运行
 ```
 python Installer.py
 ```
 - 暂时不支持Linux

### Feature
 - 若`PATH`中没有adb，自动下载并安装
 - 根据型号等信息自动匹配合适的PenMods，自动下载
 - 自动根据已知的密码解锁词典笔

### Usage
 - 下载最新的 [Release](https://github.com/PenUniverse/Installer/releases) 版本
 - 准备好词典笔，双击 `start.cmd` 启动
 - 等候出现连接词典笔的提示，按照指引打开ADB
 - 根据指引和提示，等待程序执行完成即可（一般整个过程不超过1分钟）
 
### Donate
 - 如果你觉得不错，请考虑捐赠 👉[爱发电](https://afdian.net/a/kbs007)
