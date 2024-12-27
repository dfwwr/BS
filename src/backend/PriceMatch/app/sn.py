import json

from lxml import etree
from time import sleep

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .tools import draw_num

from .tools import avoid_check, draw_num


def sn_login(web):
    try:
        # 检查登录状态
        web.find_element('xpath', '//*[@id="sn-logout"]')
        cookies = web.get_cookies()
        web.quit()
        return 'success', cookies
    except NoSuchElementException:
        try:
            # 切换到扫码登录
            scan_tab = web.find_element('xpath', '//*[@id="tab-scan"]')
            scan_tab.click()
        except NoSuchElementException:
            print('当前已在扫码页面')
        
        web.refresh()
        try:
            qr_img = web.find_element('xpath', '//*[@id="login-scan"]/div[1]/img').get_attribute('src')
            return 'fail', web, qr_img
        except NoSuchElementException:
            return 'fail', web, ''

def sn_fatch(key, web):
    """获取苏宁商品数据"""
    items_data = []
    
    # 执行搜索
    search_box = web.find_element('id', 'searchKeywords')
    search_box.clear()
    search_box.send_keys(key)
    
    search_btn = web.find_element('id', 'searchSubmit')
    search_btn.click()
    
    # 等待加载并滚动
    sleep(1)
    web.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    sleep(1)
    
    # 解析页面
    page = etree.HTML(web.page_source)
    product_items = page.xpath('//div[@class="item-bg"]')
    
    # 提取数据
    item_count = 0
    for item in product_items:
        item_count += 1
        if item_count > 20:
            break
            
        try:
            # 获取图片
            item_img = item.xpath('.//div[@class="img-block"]/a/img/@src')[0]
            if not item_img.startswith('http'):
                item_img = 'https:' + item_img
                
            # 获取标题
            item_title = ''.join(item.xpath('.//div[@class="title-selling-point"]/a/text()'))
            
            # 获取价格
            item_price = item.xpath('.//span[@class="price-box"]/span/text()')[0]
            if draw_num(item_price) == '':
                continue
                
            # 获取店铺
            try:
                item_shop = item.xpath('.//div[@class="store-stock"]//a/text()')[0].strip()
            except:
                item_shop = '苏宁自营'
                
            # 获取链接
            item_link = item.xpath('.//div[@class="title-selling-point"]/a/@href')[0]
            if not item_link.startswith('http'):
                item_link = 'https:' + item_link
                
            # 获取销量
            try:
                item_sales = item.xpath('.//div[@class="sale-num"]/text()')[0]
            except:
                item_sales = '暂无销量'
                
            # 组装数据
            items_data.append({
                'img': item_img,
                'title': item_title,
                'price': float(item_price),
                'sales': item_sales,
                'shop': item_shop,
                'platform': '苏宁易购',
                'link': item_link,
                'grab_time': time.strftime('%Y-%m-%d %H:%M', time.localtime())
            })
            
        except Exception as e:
            print(f'处理商品数据出错: {str(e)}')
            continue
            
    return items_data, web