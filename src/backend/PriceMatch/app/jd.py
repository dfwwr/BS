import json

from lxml import etree
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .tools import draw_num

from .tools import avoid_check, draw_num

def jd_login(web):
    try:
        # 等待用户扫描并登录，检查“退出登录”是否出现
        web.find_element('xpath', '//*[@id="J_user"]/div/div[1]/div/p[2]/span/a[2]')
        cookies = web.get_cookies()
        web.quit()
        return 'success', cookies
    except NoSuchElementException:
        try:
            qrcode_btn = web.find_element('xpath', '//*[@id="kbCoagent"]/ul/li[2]/a')
            qrcode_btn.click()
        except NoSuchElementException:
            print('已在二维码页面')
        web.refresh()
        try:
            qrcode_img = web.find_element('xpath', "//*[@id='tpl_for_page']/span[1]/div[1]/div[4]/div[1]/img").get_attribute('src')
            return 'fail', web, qrcode_img
        except NoSuchElementException:
            return 'fail', web, ''

def jd_fatch(key, web):
    items_data = []

    search_input = web.find_element('id', value='key')
    search_input.clear()
    search_input.send_keys(key)
    
    # 点击搜索
    search_btn = web.find_element('class name', value='button')
    search_btn.click()
    
    # 页面滚动加载
    sleep(1.5)
    web.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(1)

    # 解析页面数据
    page_content = etree.HTML(web.page_source)
    items = page_content.xpath('//div[@id="J_goodsList"]/ul/li')
    
    # 提取商品信息
    count = 0
    for item in items:
        count += 1
        if count > 20:
            break
            
        # 获取商品图片
        item_img = item.xpath('.//div[@class="p-img"]/a/img/@src')
        if not item_img:
            item_img = item.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img')
        item_img = 'https:' + item_img[0]
        
        # 获取商品标题
        item_title = ''.join(item.xpath('.//div[@class="p-name p-name-type-2"]/a/em//text()'))
        
        # 获取商品价格
        item_price = item.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
        if draw_num(item_price) == '':
            continue
            
        # 获取销量信息
        item_sales = item.xpath('.//div[@class="p-commit"]/strong/a/text()')
        if not item_sales:
            item_sales.append('未知')
        item_sales = item_sales[0].strip()
        
        # 获取店铺信息
        item_shop = item.xpath('.//div[@class="p-shop"]/span/a/@title')
        if not item_shop:
            item_shop.append('未知')
        item_shop = item_shop[0]
        
        # 获取商品链接
        item_link = 'https:' + ''.join(item.xpath('.//div[@class="p-name p-name-type-2"]/a/@href'))
        
        # 组装商品数据
        items_data.append({
            'img': item_img,
            'title': item_title,
            'price': float(item_price),
            'sales': item_sales,
            'shop': item_shop,
            'platform': '京东商城',
            'link': item_link,
            'grab_time': time.strftime('%Y-%m-%d %H:%M', time.localtime())
        })
        
    return items_data, web
