import json
from lxml import etree
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def draw_num(str_data):
    """
    :param str_data: 字符串类型
    :return: 只含数字的字符串
    """
    num_filter = filter(str.isdigit, str_data)
    num_list = list(num_filter)
    num_str = "".join(num_list)
    return num_str

def jd_login(web):
    try:
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
    search_btn = web.find_element('class name', value='button')
    search_btn.click()
    sleep(1.5)
    web.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(1)
    page_content = etree.HTML(web.page_source)
    items = page_content.xpath('//div[@id="J_goodsList"]/ul/li')
    count = 0
    for item in items:
        count += 1
        if count > 20:
            break
        item_img = item.xpath('.//div[@class="p-img"]/a/img/@src')
        if not item_img:
            item_img = item.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img')
        item_img = 'https:' + item_img[0]
        item_title = ''.join(item.xpath('.//div[@class="p-name p-name-type-2"]/a/em//text()'))
        item_price = item.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
        if draw_num(item_price) == '':
            continue
        item_sales = item.xpath('.//div[@class="p-commit"]/strong/a/text()')
        if not item_sales:
            item_sales.append('未知')
        item_sales = item_sales[0].strip()
        item_shop = item.xpath('.//div[@class="p-shop"]/span/a/@title')
        if not item_shop:
            item_shop.append('未知')
        item_shop = item_shop[0]
        item_link = 'https:' + ''.join(item.xpath('.//div[@class="p-name p-name-type-2"]/a/@href'))
        items_data.append({
            'img': item_img,
            'title': item_title,
            'price': float(item_price),
            'sales': item_sales,
            'shop': item_shop,
            'platform': '京东',
            'link': item_link,
            'grab_time': time.strftime('%Y-%m-%d %H:%M', time.localtime())
        })
    return items_data, web
