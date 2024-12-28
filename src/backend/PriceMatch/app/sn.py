import json
from lxml import etree
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from .jd import draw_num

def sn_login(web):
    try:
        web.find_element('xpath', '//*[@id="searchSubmit"]')
        cookies = web.get_cookies()
        web.quit()
        return 'success', cookies
    except NoSuchElementException:
        try:
            scan_tab = web.find_element('xpath', '/html/body/div[2]/div[1]/div/div[5]/div[1]/a[2]')
            scan_tab.click()
        except NoSuchElementException:
            print('当前已在扫码页面')
        web.refresh()
        try:
            qr_img = web.find_element('xpath', "//*[@id='tpl_for_page']/span[1]/div[1]/div[4]/div[1]/img").get_attribute('src')
            return 'fail', web, qr_img
        except NoSuchElementException:
            return 'fail', web, ''

def sn_fatch(key, web):
    items_data = []
    search_box = web.find_element('id', value='searchKeywords')
    search_box.clear()
    search_box.send_keys(key)
    search_box.send_keys(Keys.ENTER)
    sleep(1)
    web.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    sleep(1)
    page = etree.HTML(web.page_source)
    product_items = page.xpath('//div[@id="product-list"]/ul/li')
    item_count = 0
    for item in product_items:
        item_count += 1
        if item_count > 20:
            break
        try:
            item_img = item.xpath('.//div[@class="img-block"]/a/img/@src')[0]
            if not item_img.startswith('http'):
                item_img = 'https:' + item_img
            item_title = ''.join(item.xpath('.//div[@class="title-selling-point"]/a/text()')).replace('\n', '')[0:127]
            item_price = ''.join(item.xpath('.//div[@class="price-box"]/span/text()')).replace('\n', '') + \
                        ''.join(item.xpath('.//div[@class="price-box"]/span/i[2]/text()')).replace('\n', '')
            if draw_num(item_price) == '':
                continue
            try:
                item_shop = item.xpath('.//div[@class="store-stock"]//a/text()')[0]
            except:
                item_shop = '苏宁自营'
            item_link = item.xpath('.//div[@class="title-selling-point"]/a/@sa-data')[0]
            link_list = item_link.split(',')
            link_shop_id = draw_num(link_list[2])
            link_prd_id = draw_num(link_list[1])
            item_link = 'https://product.suning.com/' + link_shop_id + '/' + link_prd_id + '.html'
            try:
                item_sales = item.xpath('.//div[@class="info-evaluate"]/a/i/text()')[0]
            except:
                item_sales = '暂无销量'
            items_data.append({
                'img': item_img,
                'title': item_title,
                'price': float(item_price),
                'sales': item_sales,
                'shop': item_shop,
                'platform': '苏宁',
                'link': item_link,
                'grab_time': time.strftime('%Y-%m-%d %H:%M', time.localtime())
            })
        except Exception as e:
            print(f'处理商品数据出错: {str(e)}')
            continue
    return items_data, web