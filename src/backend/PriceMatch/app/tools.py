from msedge.selenium_tools import EdgeOptions, Edge
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os



# 提取字符串中的连续数字
def draw_num(str_data):
    """
    :param str_data: 字符串类型
    :return: 只含数字的字符串
    """
    num_filter = filter(str.isdigit, str_data)
    num_list = list(num_filter)
    num_str = "".join(num_list)
    return num_str


# 无头浏览与规避检测
def avoid_check():
    """
    :return: 浏览器窗口
    """
    option = EdgeOptions()
    option.use_chromium = True
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    # 添加请求头
    option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
    option.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    option.add_argument('accept-encoding=gzip, deflate, br')
    option.add_argument('accept-language=zh-CN,zh;q=0.9')
    
    # 添加其他选项
    option.add_argument('--ignore-certificate-errors')
    option.add_argument('--ignore-ssl-errors')
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    
    # 使用绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_dir, 'msedgedriver.exe')
    
    bro = Edge(
        executable_path=driver_path,
        options=option
    )
    return bro

