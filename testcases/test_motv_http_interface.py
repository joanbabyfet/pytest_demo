import logging
import allure
import pytest
from utils.http_utils import HttpUtils
from utils.read_jsonfile_utils import ReadJsonFileUtils
from config.global_config import MOTV_HTTP_HOST

'''
这里放get用例
'''
@pytest.mark.httptest # pytest.ini文件中要添加markers = httptest，不然会有warning，说这个Mark有问题
@allure.feature("获取手机号国码get请求测试")
class TestHttpInterface:
    # 获取文件绝对路径
    data_file_path = ReadJsonFileUtils.get_data_path("resources", "test_motv_http_data.json")
    # 获取api接口数据
    param_data = ReadJsonFileUtils(data_file_path)
    data_item = param_data.get_value('dataItem')
    # 自定义用例名称
    ids = []
    for v in data_item:
        ids.append(v['name'])

    '''
    @pytest.mark.parametrize是数据驱动;
    data_item列表中有几个字典，就运行几次case
    ids是用于自定义用例的名称
    '''
    @pytest.mark.parametrize("args", data_item, ids=ids)
    def test_motv(self, args, login):
        # 打印用例ID和名称到报告中显示
        print(f"用例ID:{args['id']}")
        print(f"用例名称:{args['name']}")
        #print(f"测试conftest传值：{login}")
        logging.info("测试开始~~~~~~~")
        args['headers']['Authorization'] = f'Bearer {login}'
        if args['method'] == 'get':
            res = HttpUtils.http_get(args['headers'], MOTV_HTTP_HOST + args['url'], args['parameters'])
        elif args['method'] == 'post':
            res = HttpUtils.http_post(args['headers'], MOTV_HTTP_HOST + args['url'], args['parameters'])
        # assert断言，判断接口是否返回期望的结果数据
        assert str(res.get('code')) == str(args['expectdata']['code']), "接口返回code值不等于预期"