import os
import requests
import time
import json
import zipfile
import shutil

PENMODS_SERVER_ADDR    = "https://dictpen.amd.rocks/"
PENMODS_PUBLIC_PACKS   = PENMODS_SERVER_ADDR + "public_packs"
PENMODS_VERSION_PACKS  = PENMODS_SERVER_ADDR + "mod_versions"

DICTPEN_ADB_PASSWD = [
    'CherryYoudao',
    'x3sbrY1d2@dictpen'
]

def printLogo():
    print("""

    ╔═╗┌─┐┌┐┌╔╦╗┌─┐┌┬┐┌─┐
 -  ╠═╝├┤ │││║║║│ │ ││└─┐ -
    ╩  └─┘┘└┘╩ ╩└─┘─┴┘└─┘

    
Welcome to use PenMods!
Developer: RedbeanW;""")

def initDirs():
    os.makedirs('dependents', exist_ok=True)
    shutil.rmtree('temp', ignore_errors=True)
    os.makedirs('temp', exist_ok=True)

class ADB:

    # the serial number.
    connected_device = ''

    def __init__(self) -> None:
        pass

    """ get installed adb command prefix """
    def getCommand(self) -> str:
        adb = 'dependents\\platform-tools\\adb.exe'
        return adb if os.path.exists(adb) else 'adb'

    """ check adb install """
    def check(self) -> bool:
        return os.popen(self.getCommand()).readline().find('Android Debug Bridge') != -1 \

    """ automatic bypass adb auth """
    def bypassVerification(self) -> bool:
        for pwd in DICTPEN_ADB_PASSWD:
            if os.popen('echo "%s" | %s -s %s shell auth' % (pwd,self.getCommand(),self.connected_device)).read().find('success') != -1:
                return True
        return False

    """ test current device """
    def test(self) -> bool:
        res = self._execute('shell uname -a').readline()
        if res.find('login with "adb shell auth" to continue') != -1:
            assert self.bypassVerification(), 'Failed to unlock dictpen.'
        return res.find('Linux') != -1

    """ protected execute adb command """
    def execute(self, cmd):
        if not self.check():
            assert self.install(), 'ADB service is necessary.'
        if not self.test():
            assert self.connect(), 'Please connect your device.'
        return self._execute(cmd)

    """ only generate command, without protect """
    def _execute(self, cmd):
        return os.popen('%s -s %s %s' % (self.getCommand(),self.connected_device,cmd))

    """ automatic install adb service """
    def install(self) -> bool:
        if self.check():
            return True
        try:
            obj = json.loads(requests.get(PENMODS_PUBLIC_PACKS).content)
            assert obj['adb']
        except:
            print('无法获取软件包列表。')
            return False
        assert Utils.download(obj['adb'],'temp/adb.zip'),'无法下载Platform-Tools，ADB安装失败。'
        file = zipfile.ZipFile('temp/adb.zip')
        shutil.rmtree('dependents/', ignore_errors=True)
        file.extractall(path='dependents/')
        if self.check():
            print('ADB安装成功。')
            return True
        return False

    """ automatic connect adb device """
    def connect(self) -> bool:
        print('# 请将词典笔与电脑连接，并开启ADB调试。')
        print('# 如果您还未安装PenMods，请进入 [更多设置]->[关于]->[法律监管] 后快速连续点击5次屏幕即可打开ADB调试。')
        print('# 如果您已经安装PenMods，请进入 [更多设置]->[关于]->[开发者选项]->[ADB服务] 中打开ADB调试。')
        waitingTime = 0
        while True:
            waitingTime += 1
            if (waitingTime > 120):
                print('\n长时间未与设备建立连接，进程退出')
                return False
            devices = []
            preText = '正在等待'
            for line in os.popen(self.getCommand() + ' devices').readlines():
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
                        if self.connected_device != '' and device[0] != self.connected_device:
                            preText = '! 这是断线重连，请不要连接不同的设备'
                        else:
                            print('\n设备 %s 已连接' % device[0])
                            print('# 在安装程序运行过程中，请保持设备连接。')
                            self.connected_device = device[0]
                            return True
            print('\r%s...%ss' % (preText,waitingTime),end='')
            time.sleep(1)

class Utils:

    def __init__(self) -> None:
        pass

    @staticmethod
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


if __name__ == '__main__':
    printLogo()
    initDirs()
    adb = ADB()

