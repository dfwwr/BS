from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from .models import Goods, Log, User_good,User
from datetime import datetime
from .jd import jd_fatch
from .vph import vph_fatch
from .sn import sn_fatch
from .tools import avoid_check
import json
from .views import send_price_alert

def check_price_changes():
    """检查所有商品的价格变化"""
    try:
        # 获取所有商品
        goods = Goods.objects.all()
        
        for good in goods:
            # 获取最新价格记录
            latest_log = Log.objects.filter(good_id=good).order_by('-timestamp').first()
            if not latest_log:
                continue
            bro = avoid_check()
            if good.good_platform == '京东':
                bro.get('https://www.jd.com/')
                products, _ = jd_fatch(good.good_name, bro)
            elif good.good_platform == '唯品会':
                bro.get('https://www.vip.com/')
                products, _ = vph_fatch(good.good_name, bro)
            elif good.good_platform == '苏宁':
                bro.get('https://www.suning.com/')
                products, _ = sn_fatch(good.good_name, bro)
            else:
                continue
                
            bro.quit()
            
            current_price = None
            for product in products:
                if product['link'] == good.good_link:
                    current_price = product['price']
                    break
                    
            if current_price is None:
                continue
                
            # 如果价格发生变化，记录并通知
            if current_price != latest_log.prise:
                # 记录新价格
                Log.objects.create(
                    good_id=good,
                    prise=current_price
                )
                
                # 获取关注该商品的所有用户
                user_goods = User_good.objects.filter(good_id=good)
                for user_good in user_goods:
                    user = User.objects.get(user_id=user_good.user_id.user_id)
                    # 发送邮件通知
                    send_price_alert(user.email, good, current_price,latest_log.prise)
                        
    except Exception as e:
        print(f"价格检查任务失败: {str(e)}") 