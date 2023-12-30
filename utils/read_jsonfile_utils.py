
import json
import os

'''
读取json接口数据工具类
'''
class ReadJsonFileUtils:
    # 构造函数
    def __init__(self, file_name):
        self.file_name  = file_name
        self.data       = self.get_data()
    
    # 获取json数据
    def get_data(self):
        f = open(self.file_name, encoding='utf-8')
        data = json.load(f)
        f.close()
        return data
    
    # 静态方法
    def get_value(self, id):
        return self.data[id]
    
    @staticmethod
    def get_data_path(folder, filename):
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_file_path = os.path.join(BASE_PATH, folder, filename)
        return data_file_path

if __name__ == '__main__':
    opr = ReadJsonFileUtils('resources/test_http_post_data.json')
    data_item = opr.get_value('dataItem')
    print(data_item)