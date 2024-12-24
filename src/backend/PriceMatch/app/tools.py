from msedge.selenium_tools import EdgeOptions, Edge
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
    
    # 添加忽略证书错误的选项
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