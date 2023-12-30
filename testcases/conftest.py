import logging
import traceback
import pytest
import requests
from config.global_config import MOTV_HTTP_HOST
import json
import urllib3

'''
如果用例执行前需要先登录获取token值，就要用到conftest.py文件了
作用：conftest.py 配置里可以实现数据共享，不需要import导入 conftest.py，pytest用例会自动查找
scope参数为session，那么所有的测试文件执行前执行一次
scope参数为module，那么每一个测试文件执行前都会执行一次conftest文件中的fixture
scope参数为class，那么每一个测试文件中的测试类执行前都会执行一次conftest文件中的fixture
scope参数为function，那么所有文件的测试用例执行前都会执行一次conftest文件中的fixture
'''
@pytest.fixture(scope="session")
def login():
    urllib3.disable_warnings() # 关闭ssl警告

    header = {
        "language":"cn",
        "Accept":"application/json"
    }
    params = {
        'params': '{"did":"7cab640329f00d1c","device_info":{"host": "abfarm-00953", "tags": "dev-keys", "type": "userdebug", "board": "unknown", "brand": "google", "model": "Android SDK built for x86", "device": "generic_x86", "display": "sdk_gphone_x86-userdebug 8.0.0 OSR1.180418.026 6741039 dev-keys", "product": "sdk_gphone_x86", "hardware": "ranchu", "androidId": "OSR1.180418.026", "bootloader": "unknown", "fingerprint": "google/sdk_gphone_x86/generic_x86:8.0.0/OSR1.180418.026/6741039:userdebug/dev-keys", "manufacturer": "Google", "supportedAbis": ["x86"], "systemFeatures": ["android.hardware.sensor.proximity", "android.hardware.sensor.accelerometer", "android.hardware.faketouch", "android.hardware.usb.accessory", "android.software.backup", "android.hardware.touchscreen", "android.hardware.touchscreen.multitouch", "android.software.print", "android.software.voice_recognizers", "android.software.picture_in_picture", "android.hardware.fingerprint", "android.hardware.sensor.gyroscope", "android.hardware.sensor.relative_humidity", "com.google.android.feature.GOOGLE_BUILD", "android.hardware.telephony.gsm", "android.hardware.audio.output", "android.hardware.screen.portrait", "android.hardware.sensor.ambient_temperature", "android.software.home_screen", "android.hardware.microphone", "android.software.autofill", "android.hardware.sensor.compass", "android.hardware.touchscreen.multitouch.jazzhand", "android.hardware.sensor.barometer", "android.software.app_widgets", "android.software.input_methods", "android.hardware.sensor.light", "android.software.device_admin", "android.hardware.camera", "android.hardware.screen.landscape", "android.software.managed_users", "android.software.webview", "android.hardware.camera.any", "android.software.connectionservice", "android.hardware.touchscreen.multitouch.distinct", "android.hardware.location.network", "android.software.cts", "com.google.android.apps.dialer.SUPPORTED", "android.software.live_wallpaper", "com.google.android.feature.GOOGLE_EXPERIENCE", "com.google.android.feature.EXCHANGE_6_2", "android.hardware.location.gps", "android.software.midi", "android.hardware.wifi", "android.hardware.location", "android.hardware.telephony", null], "version.baseOS": "", "version.sdkInt": 26, "version.release": "8.0.0", "isPhysicalDevice": false, "version.codename": "REL", "supported32BitAbis": ["x86"], "supported64BitAbis": [], "version.incremental": "6741039", "version.previewSdkInt": 0, "version.securityPatch": "2018-04-05"}, "app_info": {"version": 1},"channel":"Snwn1Zi28","test":false}',
    }
    url = MOTV_HTTP_HOST + '/login'
    logging.info(f'开始调用登录接口:{url}')
    res = requests.post(url, data=params, headers=header, verify=False)  # verify：忽略https的认证
    try:
        data = json.loads(res.text)
        token = data['data']['token']
    except Exception as ex:
        logging.error(f'登录失败！接口返回：{res.text}')
        traceback.print_tb(ex)
    logging.info(f'登录成功，token值为：{token}')
    return token

#测试一下conftest.py文件和fixture的作用
@pytest.fixture(scope="session")
def login_test():
    print("运行用例前先登录！")

    # 使用yield关键字实现后置操作，如果上面的前置操作要返回值，在yield后面加上要返回的值
    # 也就是yield既可以实现后置，又可以起到return返回值的作用
    yield "runBeforeTestCase"
    print("运行用例后退出登录！")

# 解决终端显示中文
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')