import os
import requests
import time
import json
import zipfile
import shutil

PENMODS_SERVER_ADDR    = "https://dictpen.amd.rocks/"
PENMODS_PUBLIC_PACKS   = PENMODS_SERVER_ADDR + "public_packs"
PENMODS_VERSION_PACKS  = PENMODS_SERVER_ADDR + "mod_versions"

def printLogo():
    print("""

    ╔═╗┌─┐┌┐┌╔╦╗┌─┐┌┬┐┌─┐
 -  ╠═╝├┤ │││║║║│ │ ││└─┐ -
    ╩  └─┘┘└┘╩ ╩└─┘─┴┘└─┘

    
Welcome to use PenMods!
Developer: RedbeanW;""")

def getAdbCommand():
    adb = 'dependents\\platform-tools\\adb.exe'
    return adb if os.path.exists(adb) else 'adb'


def checkIsAdbAvailable():
    return os.popen(getAdbCommand()).readline().find('Android Debug Bridge') != -1 \

def download(url, path:str):  # from: https://blog.csdn.net/weixin_43347550/article/details/105248223
    start = time.time()
    response = requests.get(url, stream=True)
    size = 0
    chunk_size = 1024
    content_size = int(response.headers['content-length'])
    try:
        if response.status_code == 200:
            print('Downloading ... ({size:.2f} Mb).'.format(
                size=content_size / chunk_size / 1024))
            with open(path, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r   '+'%s %.2f%%' % ('━' * int(size * 50 / content_size),
                          float(size / content_size * 100)), end=' ')
        end = time.time()
        print('\nCompleted, time cost %.2f second(s).' % (end - start))
        return True
    except:
        print("Fail to download %s!" % url)
        return False


def tryInstallAdb():
    try:
        obj = json.loads(requests.get(PENMODS_PUBLIC_PACKS).content)
        assert(obj['adb'])
    except:
        print('无法获取软件包列表。')
        exit(-1)
    assert(download(obj['adb'],'temp/adb.zip'),'无法下载Platform-Tools，ADB安装失败。')
    file = zipfile.ZipFile('temp/adb.zip')
    shutil.rmtree('dependents/', ignore_errors=True)
    file.extractall(path='dependents/')
    if (checkIsAdbAvailable()):
        print('ADB安装成功。')
        return True
    return False


def initDirs():
    os.makedirs('dependents', exist_ok=True)
    shutil.rmtree('temp', ignore_errors=True)
    os.makedirs('temp', exist_ok=True)

def tryConnectDictPen():
    print('# 请将词典笔与电脑连接，并开启ADB调试。')
    print('# 如果您还未安装PenMods，请进入 [更多设置]->[关于]->[法律监管] 后快速连续点击5次屏幕即可打开ADB调试。')
    print('# 如果您已经安装PenMods，请进入 [更多设置]->[关于]->[开发者选项]->[ADB服务] 中打开ADB调试。')
    waitingTime = 0
    while True:
        waitingTime += 1
        if (waitingTime > 120):
            print('\n长时间未与设备建立连接，进程退出')
            exit(-1)
        devices = []
        preText = '正在等待'
        for line in os.popen(getAdbCommand() + ' devices').readlines():
            if (len(line) < 5 or line.find('List of devices attached') != -1):
                continue
            dev = line.split('\t')
            devices.append((dev[0],dev[1].removesuffix('\n')))
        if len(devices) > 0:
            device = devices[0]
            if (len(devices) > 1):
                preText = '! 请不要连接多个设备'
            else:
                if (device[1] != 'device'):
                    preText = '! 设备 %s 已连接，但设备状态不正确(%s)，请检查' % (device[0],device[1])
                else:
                    print('设备 %s 已连接' % device[0])
                    print('# 在安装程序运行过程中，请保持连接，且不要插入其他ADB设备。')
                    break
        print('\r%s...%ss' % (preText,waitingTime),end='')
        time.sleep(1)


if __name__ == '__main__':
    printLogo()
    initDirs()
    if (not checkIsAdbAvailable()):
        assert(tryInstallAdb(), 'adb service is necessary.')
    tryConnectDictPen() # exit if failed.

    
