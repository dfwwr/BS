import json

from lxml import etree
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from .tools import avoid_check, draw_num

def vph_login(web):
    try:
        # 检查登录状态
        web.find_element('xpath', '//*[@id="J_user_logout"]')
        cookies = web.get_cookies()
        web.quit()
        return 'success', cookies
    except NoSuchElementException:
        try:
            # 切换到扫码登录
            scan_tab = web.find_element('xpath', '//*[@id="J_qr_code_tab"]')
            scan_tab.click()
        except NoSuchElementException:
            print('当前已在扫码页面')
            
        web.refresh()
        try:
            qr_img = web.find_element('xpath', '//*[@id="J_qr_code_img"]').get_attribute('src')
            return 'fail', web, qr_img
        except NoSuchElementException:
            return 'fail', web, ''

def vph_fatch(name, web):
    items_data = []
    search_input = web.find_element('xpath', '//*[@id="J-search"]/div[1]/input')
    # 搜索关键词
    search_input.clear()
    search_input.send_keys(name)
    # 回车以搜索
    search_input.send_keys(Keys.ENTER)
    sleep(1)
    # 获取页面高度和视口高度
    page_height = web.execute_script("return document.body.scrollHeight")
    viewport_height = web.execute_script("return window.innerHeight")
    # 初始化当前滚动位置
    current_position = 0
    # 执行一组js程序滚动页面置底
    while current_position < page_height * 0.2:
        web.execute_script(f"window.scrollTo(0, {current_position + viewport_height});")
        current_position += viewport_height
        # 等待图片加载
        sleep(2)
    # 数据解析
    page = etree.HTML(web.page_source)
    product_items = (page.xpath('//*[@id="J_searchCatList"]/div[@class="c-goods-item  J-goods-item c-goods-item--auto-width"]'))
    i = 0
    for item in product_items:
        i += 1
        if i > 20:
            break
        # 图片
        item_img = item.xpath('.//a/div[1]/div[1]/img/@src')
        if not item_img:
            item_img = item.xpath('.//a/div[1]/div[1]/img/@data-original')
        item_img = 'https:' + item_img[0]
        # 商品标题
        item_title = ''.join(item.xpath('.//a/div[2]/div[2]//text()'))
        # 商品价格
        item_price = item.xpath('.//a/div[2]/div[1]/div[1]/div[2]/text()')[0]
        if draw_num(item_price) == '':
            continue
        # 店铺名
        item_shop = '唯品会官方旗舰店'
        # 商品链接
        item_link = 'https:' + ''.join(item.xpath('.//a/@href'))
        # 平台
        item_platform = '唯品会'
        items_data.append({
            'img': item_img,
            'title': item_title,
            'price': float(item_price),
            'sales': '',
            'shop': item_shop,
            'platform': item_platform,
            'link': item_link,
            'grab_time': time.strftime('%Y-%m-%d %H:%M', time.localtime())
        })
    # # 存储cookie
    # cookies = bro.get_cookies()
    # # 关闭无头浏览器
    # bro.quit()
    return items_data, web