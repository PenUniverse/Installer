import os
import requests
import time
import json
import zipfile
import shutil
import sys

PENMODS_SERVER_ADDR    = "https://dictpen.amd.rocks/"
PENMODS_PUBLIC_PACKS   = PENMODS_SERVER_ADDR + "public_packs"
PENMODS_MOD_PACKS      = PENMODS_SERVER_ADDR + "mod_packs"

MOD_PACK_VERSION    = 100
PUBLIC_PACK_VERSION = 100

VERSION = "1.0.0"

def printLogo():
    print("""

    ╔═╗┌─┐┌┐┌╔╦╗┌─┐┌┬┐┌─┐
    ╠═╝├┤ │││║║║│ │ ││└─┐
    ╩  └─┘┘└┘╩ ╩└─┘─┴┘└─┘

    
Welcome to use PenMods!
Developer:  RedbeanW;
Repo:       https://github.com/PenUniverse/Installer
Version:    %s""" % VERSION)

def initDirs():
    os.makedirs('dependents', exist_ok=True)
    shutil.rmtree('temp', ignore_errors=True)
    os.makedirs('temp', exist_ok=True)

class ADB:

    first_connected_device = None

    def __init__(self) -> None:
        pass

    """ get installed adb command prefix """
    def getCommand(self) -> str:
        adb = 'dependents\\platform-tools\\adb.exe'
        return adb if os.path.exists(adb) else 'adb'

    """ check adb install """
    def check(self) -> bool:
        return Utils.run(self.getCommand()).find('Android Debug Bridge') != -1 \

    """ automatic bypass adb auth """
    def bypassVerification(self) -> bool:
        if not self.first_connected_device:
            return False
        if self._execute('shell ls').find('login with "adb shell auth" to continue') != -1:
            if Utils.run('echo CherryYoudao | %s shell auth' % self.getCommand()).find('success') != -1:
                print('DictPen is unlocked.')
                return True
            else:
                return False
        return True

    """ test current device """
    def test(self) -> bool:
        return self._execute('shell uname -a').find('Linux') != -1

    """ protected execute adb command """
    def execute(self, cmd):
        if not self.check():
            assert self.install(), 'ADB服务是必须的。'
        if not self.test():
            assert self.connect(), '请连接你的设备。'
        self.bypassVerification()
        return self._execute(cmd)

    """ only generate command, without protect """
    def _execute(self, cmd):
        return Utils.run('%s %s' % (self.getCommand(),cmd))

    """ automatic install adb service """
    def install(self) -> bool:
        if self.check():
            return True
        try:
            assert public_pack['adb']
        except:
            print('无法获取软件包列表。')
            return False
        assert Utils.download(public_pack['adb'],'temp/adb.zip'), '无法下载Platform-Tools，ADB安装失败。'
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
        print('# 请进入 [更多设置]->[关于]->[法律监管] 后快速连续点击5次屏幕即可打开ADB调试。')
        waitingTime = 0
        while True:
            waitingTime += 1
            if (waitingTime > 120):
                print('\n长时间未与设备建立连接，进程退出')
                return False
            devices = []
            preText = '正在等待'
            for line in Utils.run(self.getCommand() + ' devices').split('\n'):
                if (len(line) < 5 or line.find('List of devices attached') != -1):
                    continue
                dev = line.split('\t')
                devices.append((dev[0],dev[1].removesuffix('\n')))
            if len(devices) > 0:
                device = devices[0]
                if len(devices) > 1:
                    preText = '! 请不要连接多个设备'
                else:
                    if (device[1] != 'device'):
                        preText = '! 设备 %s 已连接，但设备状态不正确(%s)，请检查' % (device[0],device[1])
                    else:
                        if self.first_connected_device and device[0] != self.first_connected_device:
                            preText = '! 这是断线重连，请不要连接不同的设备'
                        else:
                            print('\n设备 %s 已连接' % device[0])
                            print('# 在安装程序运行过程中，请保持设备连接。')
                            self.first_connected_device = device[0]
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
            else:
                print(url)
                print('Wrong response code(%s)' % response.status_code)
                return False
            end = time.time()
            print('\nCompleted, time cost %.2f second(s).' % (end - start))
            return True
        except:
            print("Fail to download %s!" % url)
            return False

    @staticmethod
    def run(cmd: str) -> str:
        with os.popen(cmd) as res:
            buffer = res._stream.buffer.read()
        try:
            return buffer.decode().strip()
        except UnicodeDecodeError:
            return buffer.decode('gbk').strip()

adb         = None
mod_pack    = None
public_pack = None

def getSystemVersions() -> dict:
    ret = {}
    exec = adb.execute('shell cat /Version')
    if exec.find('No such file') != -1:
        return {}
    for i in exec.split('\n'):
        kv = i.split(':')
        if len(kv) >= 2: ret[kv[0]] = kv[1].strip('\r').removeprefix(' ')
    return ret

def getPcbaVersion() -> str:
    exec = adb.execute('shell get_pcba_version')
    return exec if exec.find('not found') == -1 else None

def getAppMd5() -> str:
    exec = adb.execute('shell md5sum -b /oem/YoudaoDictPen/output/YoudaoDictPen')
    return exec.split(' ')[0].lower() if exec.find('No such file') == -1 else None

def checkConnection() -> bool:
    return requests.get(PENMODS_SERVER_ADDR).status_code == 200

def isInstalled() -> bool:
    exec = adb.execute('shell cat /usr/bin/runDictPen')
    return exec.find('try_inject') == -1

def install_a(info: dict):
    assert Utils.download(info['download'],'temp/pack.zip')
    zipfile.ZipFile('temp/pack.zip').extractall('temp/pack')
    
    def ro_check():
        if adb.execute('shell touch /TEST_PART_RW').find('Read-only file system'):
            adb.execute('shell mount -o remount,rw /')
            time.sleep(1)
        adb.execute('shell rm -f /TEST_PART_RW')

    def upload_ex(path,to,setperm=False):
        ro_check()
        adb.execute('push "temp/pack/%s" "%s"' % (path,to))
        if setperm:
            adb.execute('shell chmod +x "%s"' % to)
    
    print('(1/4) 正在安装自动注入器...')
    upload_ex('dependents/injector','/userdisk/Loader/injector',True)
    upload_ex('script/try_inject','/usr/bin/try_inject',True)
    adb.execute("shell \"sed -i '1i try_inject &' /usr/bin/runDictPen\"")

    print('(2/4) 正在更新动态链接库...')
    upload_ex('dependents/libm.so.6','/lib/libm.so.6')
    upload_ex('dependents/libstdc++.so.6','/usr/lib/libstdc++.so.6')

    print('(3/4) 正在安装 PenMods...')
    upload_ex('libPenMods.so','/userdisk/Loader')
    upload_ex('external-icons/','/tmp/')
    adb.execute('shell mv -b /tmp/external-icons/settings/* /oem/YoudaoDictPen/output/images/settings/')
    

    # AudioRecorder required.
    upload_ex('dependents/lame','/userdisk/Loader/dependents/lame',True)
    upload_ex('dependents/libtinfo.so.6','/userdisk/Loader/dependents/libtinfo.so.6')

    print('(4/4) 安装完成，正在重启...')
    adb.execute('shell safe_powerdown')
    print('# 如果没有意外，PenMods 已成功安装到您的词典笔上。')
    print('# Enjoy it!')
    exit(0)

if __name__ == '__main__':
    printLogo()
    initDirs()

    assert sys.platform == 'win32', '安装程序暂只支持Windows系统。'

    # Initialization.
    adb = ADB()
    assert checkConnection(), '安装程序需要联网执行，请检查您的网络链接。'
    
    mod_pack = json.loads(requests.get(PENMODS_MOD_PACKS).content)
    public_pack = json.loads(requests.get(PENMODS_PUBLIC_PACKS).content)
    assert mod_pack['version'] and public_pack['version'], '无法获取在线 ModPacks.'
    assert mod_pack['version'] == MOD_PACK_VERSION, 'MOD列包表版本不匹配，请升级安装程序。'
    assert public_pack['version'] == PUBLIC_PACK_VERSION, '公共包列表版本不匹配，请升级安装程序。'

    mod_pack = mod_pack['packs']
    public_pack = public_pack['packs']
    
    # Preparing for the Adaptation Check.
    sys_version = getSystemVersions()['Version']
    sys_pcba    = getPcbaVersion()
    sys_app_md5 = getAppMd5()
    if not sys_version or not sys_pcba or not sys_app_md5:
        print('无法获取系统信息，连接的也许不是词典笔？')
        exit(-1)
    
    assert isInstalled(), '当前系统已安装PenMods，请先还原系统再执行安装。'

    # Match the appropriate pack.
    matched = None
    for pack in mod_pack:
        adapt  = pack['adaptation']
        if sys_version in adapt['version'] and sys_pcba in adapt['pcba'] and sys_app_md5 in adapt['app']:
            matched = pack
            break
    
    if not matched:
        print('无法为当前词典笔匹配合适的PenMods，可能其暂时不受支持。')
        print('Version: %s' % sys_version)
        print('Pcba:    %s' % sys_pcba)
        print('App:     %s' % sys_app_md5)
        exit(-1)
    ver = matched['version']
    print('已匹配到合适的PenMods (%s,V%s), 是否确认安装？' % (matched['name'],'.'.join(str(v) for v in matched['version'])))
    print('# 务必仔细阅读 github.com/PenUniverse/Installer 仓库中的注意事项')
    print('# 安装 PenMods 可能导致您失去有道官方保修')
    print('# 使用 PenMods 造成的一切后果均由您本人承担，与项目作者没有任何关系')
    print('# 特别注意: 不要为已修改过的系统执行安装，这是安装程序并非升级程序！！')

    if input('您是否已充分阅读、理解与接受以上告示，并决定开始安装？[y/N] ').lower() != 'y':
        exit(-1)
    
    if matched['install'] == 'a':
        install_a(matched)
    else:
        print('远端要求使用不受支持的安装方法，尝试更新安装程序？')