## About
通过pytest框架实现接口自动化测试, 并导出html／allure报告

## Usage
```
# 进入testcases目录下
pytest test_motv_http_interface.py 或
pytest -m httptest

# 导出pytest-html报告
pytest test_motv_http_interface.py --html=../testoutput/report.html

# 导出allure报告
pytest --alluredir=../testoutput/result
allure generate ../testoutput/result/ -o ../testoutput/report/ --clean

# 显示allure报告, 进入testoutput目录下
allure open report/
```

## Maintainers
Alan

## LICENSE
[MIT License](https://github.com/joanbabyfet/pytest_demo/blob/master/LICENSE)
