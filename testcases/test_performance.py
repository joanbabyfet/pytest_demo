import requests 
import time 
import threading
import psutil
import pytest 
import logging
import allure
import urllib3

# 定义测试用例
@pytest.mark.performance # pytest.ini文件中要添加markers = performance，不然会有warning，说这个Mark有问题
def test_performance():
    urllib3.disable_warnings() # 关闭ssl警告

    # 设置测试参数
    url = 'https://www.google.com.tw'
    num_thread  = 20        # 线程数(模拟几个用户)
    num_request = 200       # 每个线程的请求次数
    timeout     = 5         # 超时时间

    # 初始化测试结果
    response_times = []     # 响应时间列表
    success     = 0         # 成功次数
    error       = 0         # 失败次数

    def test_func():
        nonlocal error, success # 只在闭包里面生效
        for _ in range(num_request):
            try:
                start_time = time.time() # 开始时间
                res = requests.get(url, timeout=timeout, verify=False)
                end_time = time.time() # 结束时间
                responsea_time = end_time - start_time # 执行时间
                response_times.append(responsea_time) # 执行时间列表
                success += 1
            except requests.exceptions.RequestException:
                error += 1
        
    # 创建测试线程
    threads = []
    for _ in range(num_thread):
        t = threading.Thread(target=test_func)
        threads.append(t)

    # 启动测试线程
    for t in threads:
        t.start()

    # 等待测试线程结束
    for t in threads:
        t.join()

    # 计算测试结束
    total_request = num_thread * num_request
    throughput = success / (sum(response_times) or 1)
    concurrency = num_thread
    error_rate = error /(total_request or 1)
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    # 将测试结果显示在终端
    logging.info(f'总请求数: {total_request}')
    logging.info(f'总时间: {sum(response_times):.2f} 秒')
    logging.info(f'吞吐量: {throughput:.2f} 次请求/秒')
    logging.info(f'并发数: {concurrency}')
    logging.info(f'错误率: {error_rate:.2%}')
    logging.info(f'CPU利用率: {cpu_usage:.2f}%')
    logging.info(f'内存利用率: {memory_usage:.2f}%')

    # 将测试结果显示在html报告里
    print(f'总请求数: {total_request}')
    print(f'总时间: {sum(response_times):.2f} 秒')
    print(f'吞吐量: {throughput:.2f} 次请求/秒')
    print(f'并发数: {concurrency}')
    print(f'错误率: {error_rate:.2%}')
    print(f'CPU利用率: {cpu_usage:.2f}%')
    print(f'内存利用率: {memory_usage:.2f}%')

    # 将测试结果写入txt文件
    # with open('performance_result.txt', 'w', encoding="utf-8") as f:
    #     f.write(f'总请求数: {total_request}\n')
    #     f.write(f'总时间: {sum(response_times):.2f} 秒\n')
    #     f.write(f'吞吐量: {throughput:.2f} 次请求/秒\n')
    #     f.write(f'并发数: {concurrency}\n')
    #     f.write(f'错误率: {error_rate:.2%}\n')
    #     f.write(f'CPU利用率: {cpu_usage:.2f}%\n')
    #     f.write(f'内存利用率: {memory_usage:.2f}%\n')