from DrissionPage import ChromiumPage, ChromiumOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import json

def get_product(keyword):
    co = ChromiumOptions().headless()
 
    cp = ChromiumPage(co)

    # cp.get('https://login.taobao.com/member/login.jhtml')
    cp.get('https://www.taobao.com/')

    # cp.ele('css:#fm-login-id').input("")
    # cp.ele('css:#fm-login-password').input("")
    # cp.ele('css:.fm-button.fm-submit.password-login').click()

    cp.ele('css:#q').input(keyword)
    cp.ele('css:.btn-search.tb-bg').click()
    cp.listen.start('h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0')

    bodys = []

    data_packets = cp.listen.wait(count=2)
    for data_packet in data_packets:
        bodys.append(str(data_packet.response.body))

    matching_bodys = [body for body in bodys if body.startswith(' mtopjsonp')]

    for matching_body in matching_bodys:
        string = re.findall(r' mtopjsonp\d+\((.*)\)', matching_body)[0]
        mtop_data = json.loads(string)

        items_array = mtop_data['data']['itemsArray']
        print(items_array)

    cp.quit()
if __name__ == '__main__':
    get_product('鼠标')