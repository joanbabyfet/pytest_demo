
import requests
import json
import urllib3

'''
http请求工具类
'''
class HttpUtils:
    @staticmethod
    def http_post(headers, url, parameters):
        urllib3.disable_warnings() # 关闭ssl警告

        print('接口请求url：' + url)
        print("接口请求method：post")
        print('接口请求headers：' + json.dumps(headers))
        print('接口请求parameters：' + json.dumps(parameters))
        res = requests.post(url, data=parameters, headers=headers, verify=False)
        print('接口返回结果：' + res.text)
        if res.status_code != 200:
            raise Exception(u'请求异常')
        result = json.loads(res.text)
        return result
    
    @staticmethod
    def http_get(headers, url, parameters):
        urllib3.disable_warnings() # 关闭ssl警告

        req_headers = json.dumps(headers) # 字典转json格式字符串
        print("接口请求url：" + url)
        print("接口请求method：get")
        print("接口请求headers：" + req_headers)
        print('接口请求parameters：' + json.dumps(parameters))
        res = requests.get(url, params=parameters, headers=headers, verify=False)
        print("接口返回结果：" + res.text)
        if res.status_code != 200:
            raise Exception(u"请求异常")
        result = json.loads(res.text) # json格式字符串转字典
        return result