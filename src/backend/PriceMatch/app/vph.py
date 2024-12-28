import json
from lxml import etree
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .jd import draw_num

def vph_login(web):
    try:
        web.find_element('xpath', '//*[@id="J-search"]/div[1]/a')
        cookies = web.get_cookies()
        web.quit()
        return 'success', cookies
    except NoSuchElementException:
        try:
            qrcode_url = web.find_element('xpath', '/html/body/div[2]/div/div[1]/div[2]/div/div[1]/div/a').get_attribute('href')
            web.get(qrcode_url)
        except NoSuchElementException:
            print('当前已在扫码页面')
        web.refresh()
        try:
            qr_img = web.find_element('xpath', "//*[@id='tpl_for_page']/span[1]/div[1]/div[4]/div[1]/img").get_attribute('src')
            return 'fail', web, qr_img
        except NoSuchElementException:
            return 'fail', web, ''

def vph_fatch(name, web):
    items_data = []
    search_input = web.find_element('xpath', '//*[@id="J-search"]/div[1]/input')
    search_input.clear()
    search_input.send_keys(name)
    search_input.send_keys(Keys.ENTER)
    sleep(1)
    page_height = web.execute_script("return document.body.scrollHeight")
    viewport_height = web.execute_script("return window.innerHeight")
    current_position = 0
    while current_position < page_height * 0.2:
        web.execute_script(f"window.scrollTo(0, {current_position + viewport_height});")
        current_position += viewport_height
        sleep(2)
    page = etree.HTML(web.page_source)
    product_items = (page.xpath('//*[@id="J_searchCatList"]/div[@class="c-goods-item  J-goods-item c-goods-item--auto-width"]'))
    i = 0
    for item in product_items:
        i += 1
        if i > 20:
            break
        item_img = item.xpath('.//a/div[1]/div[1]/img/@src')
        if not item_img:
            item_img = item.xpath('.//a/div[1]/div[1]/img/@data-original')
        item_img = 'https:' + item_img[0]
        item_title = ''.join(item.xpath('.//a/div[2]/div[2]//text()'))
        item_price = item.xpath('.//a/div[2]/div[1]/div[1]/div[2]/text()')[0]
        if draw_num(item_price) == '':
            item_price = '暂无报价'
        item_shop = '唯品会官方旗舰店'
        item_link = 'https:' + ''.join(item.xpath('.//a/@href'))
        item_platform = '唯品会'
        items_data.append({
            'img': item_img,
            'title': item_title,
            'price': item_price,
            'sales': '',
            'shop': item_shop,
            'platform': item_platform,
            'link': item_link,
            'grab_time': time.strftime('%Y-%m-%d %H:%M', time.localtime())
        })
    return items_data, web