# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Goods,User,User_good,Log
from .models import jdCookie,snCookie,vphCookie
from .serializers import GoodsSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .tools import avoid_check
from .jd import jd_login,jd_crawler
from .vph import vph_login,vph_crawler
from .sn import sn_login,sn_crawler
import json
from time import sleep
from django.core.mail import send_mail
from django.conf import settings
import re
jd_map={}
sn_map={}
vph_map={}

def send_price_alert(user_email, good, current_price,prise):
    """发送价格提醒邮件"""
    subject = '商品价格提醒'
    message = f'''
    您关注的商品"{good.good_name}"价格发生变化！
    描述: {good.good_description}
    原价格: ¥{prise}
    现价格: ¥{current_price}
    变动幅度: {((current_price - prise) / prise * 100):.2f}%
    
    商品链接: {good.good_link}
    
    请及时查看！
    '''
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        return False


@csrf_exempt
def GoodsList(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        userid = body.get('user_id')
        good_ids=User_good.objects.filter(user_id=userid).values_list('good_id',flat=True)
        goods_list=[]
        for id in good_ids:
            good=Goods.objects.filter(good_id=id)\
            .values('good_id','good_name','good_description',
            'good_scale','good_type','good_pic','good_link','good_platform').first()
            good_dict=dict(good)
            latest_price=Log.objects.filter(good_id=id)\
                .order_by('-timestamp').values('prise','timestamp').first()
            
            if latest_price:
                good_dict['price']=latest_price['prise']
                good_dict['price_update_time']=latest_price['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            else:
                good_dict['price']=None
                good_dict['price_update_time']=None
            goods_list.append(good_dict)
        return JsonResponse(goods_list,safe=False)

@csrf_exempt
def Signup(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        email = body.get('email')
        phone = body.get('phone')
        
        # 验证用户名长度
        if len(username) < 6:
            return JsonResponse({'error': '用户名长度必须大于6个字符'}, status=400)
            
        # 验证密码长度
        if len(password) < 6:
            return JsonResponse({'error': '密码长度必须大于6个字符'}, status=400)
            
        # 验证邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return JsonResponse({'error': '请输入正确的邮箱地址'}, status=400)
            
        # 验证手机号格式（如果提供）
        if phone:
            phone_pattern = r'^1[3-9]\d{9}$'
            if not re.match(phone_pattern, phone):
                return JsonResponse({'error': '请输入正确的手机号码'}, status=400)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=400)
            
        # 检查邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': '邮箱已被使用'}, status=400)
            
        # 创建新用户
        user = User(
            username=username,
            password=password,
            email=email,
            phone=phone
        )
        user.save()
        
        return JsonResponse({
            'message': 'User created successfully. Jump to login page after 1 seconds'
        })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def Signin(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        if not User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User does not exist.'}, status=400)
        
        user = User.objects.get(username=username)
        if user.password != password:
            return JsonResponse({'error': 'Incorrect password.'}, status=400)
        
        return JsonResponse({'message': 'Login successful','user_id':user.user_id})
    else:
        return JsonResponse({'message': 'Invalid request method'})
    
@csrf_exempt
def CheckLogin(request):
    response = {}
    req = json.loads(request.body)
    
    if request.method == 'POST':
        if req.get('method') == 'check':
            response['jd'] = 'true'
            response['vph'] = 'true'
            response['sn'] = 'true'
            user=User.objects.get(user_id=req['user_id'])
            print(user)
            try:
                jd_cookie = jdCookie.objects.get(user_id=user)
                print(jd_cookie)
                if timezone.now() - jd_cookie.created_at > timedelta(days=1):
                    jdCookie.objects.filter(user_id=user).delete()
                    raise jdCookie.DoesNotExist
            except jdCookie.DoesNotExist:
                response['jd'] = 'false'
            
            try:
                vph_cookie = vphCookie.objects.get(user_id=user)
                if timezone.now() - vph_cookie.created_at > timedelta(days=1):
                    vphCookie.objects.filter(user_id=user).delete()
                    raise vphCookie.DoesNotExist
            except vphCookie.DoesNotExist:
                response['vph'] = 'false'
            
            try:
                sn_cookie = snCookie.objects.get(user_id=user)
                if timezone.now() - sn_cookie.created_at > timedelta(days=1):
                    snCookie.objects.filter(user_id=user).delete()
                    raise snCookie.DoesNotExist
            except snCookie.DoesNotExist:
                response['sn'] = 'false'
            
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'Invalid request method'})
    
@csrf_exempt
def Login(request):
    response={}
    req = json.loads(request.body)
    user = User.objects.get(user_id=req['user_id'])
    if request.method == 'POST':
        if req['method'] == 'jd_login':
            if req['user_id'] not in jd_map:
                bro = avoid_check()
                bro.get('https://passport.jd.com/new/login.aspx')
                res = jd_login(bro)
            else:
                res = jd_login(jd_map[req['user_id']])
            
            if res[0] == 'success':
                jdCookie.objects.create(
                    user_id=user,
                    cookie=json.dumps(res[1]))
                response['message'] = '扫码成功'
            elif res[0] == 'fail':
                jd_map[req['user_id']] = res[1]
                response['qrcode'] = res[2]
                response['message'] = '待扫码'
                
        elif req['method'] == 'vph_login':
            if req['user_id'] not in vph_map:
                bro = avoid_check()
                bro.get('https://category.vip.com/suggest.php?keyword=1')
                res = vph_login(bro)
            else:
                res = vph_login(vph_map[req['user_id']])
            if res[0] == 'success':
                vphCookie.objects.create(
                    user_id=user,
                    cookie=json.dumps(res[1]))
                response['message'] = '扫码成功'
            elif res[0] == 'fail':
                vph_map[req['user_id']] = res[1]
                response['qrcode'] = res[2]
                response['message'] = '待扫码'

        elif req['method'] == 'sn_login':
            if req['user_id'] not in sn_map:
                bro = avoid_check()
                bro.get('https://passport.suning.com/ids/login?service=https%3A%2F%2Floginst.suning.com%2F%2Fauth%3FtargetUrl%3Dhttps%253A%252F%252Fwww.suning.com%252F&method=GET&loginTheme=b2c')
                res = sn_login(bro)
            else:
                res = sn_login(sn_map[req['user_id']])
            if res[0] == 'success':
                snCookie.objects.create(
                    user_id=user,
                    cookie=json.dumps(res[1]))
                response['message'] = '扫码成功'
            elif res[0] == 'fail':
                sn_map[req['user_id']] = res[1]
                response['qrcode'] = res[2]
                response['message'] = '待扫码'

        return JsonResponse(response)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def GoodSearch(request):
    response={}
    req = json.loads(request.body)
    user_id = req['user_id']
    user=User.objects.get(user_id=user_id)
    if request.method == 'POST':
        if req['method'] == 'jd_search':
            jd_cookie = jdCookie.objects.get(user_id=user)
            cookies = json.loads(jd_cookie.cookie)
            if req['user_id'] not in jd_map:
                bro = avoid_check()
                bro.get('https://www.jd.com/')
                for cookie in cookies:
                    bro.add_cookie(cookie)
            else:
                bro = jd_map[user_id]

            response['products'], jd_map[user_id] = \
                jd_crawler(req['name'], bro)
            response['message'] = 'success'
        elif req['method'] == 'vph_search':
            vph_cookie = vphCookie.objects.get(user_id=user)
            cookies = json.loads(vph_cookie.cookie)
            if req['user_id'] not in vph_map:
                bro = avoid_check()
                bro.get('https://www.vip.com/')
                for cookie in cookies:
                    cookie['domain'] = '.vip.com'
                    bro.add_cookie(cookie)
                sleep(3)
            else:
                bro = vph_map[user_id]
            response['products'], vph_map[user_id] =\
                vph_crawler(req['name'], bro)
            response['message'] = 'success'
        elif req['method'] == 'sn_search':
            sn_cookie = snCookie.objects.get(user_id=user)
            cookies = json.loads(sn_cookie.cookie)
            if req['user_id'] not in sn_map:
                bro = avoid_check()
                bro.get('https://www.suning.com/')
                for cookie in cookies:
                    bro.add_cookie(cookie)
            else:
                bro = sn_map[user_id]
            response['products'], sn_map[user_id] =\
                sn_crawler(req['name'], bro)
            response['message'] = 'success'
        return JsonResponse(response)

@csrf_exempt
def StarProduct(request):
    response={}
    req = json.loads(request.body)
    user_id = req['user_id']
    product = req['product']
    productName=req['productname']
    try:
        user=User.objects.get(user_id=user_id)
        exists=Goods.objects.filter(good_link=product['link']).exists()
        if exists:
            good=Goods.objects.get(good_link=product['link'])
        else:
            good=Goods.objects.create(
                good_name=productName,
                good_description=product['title'],
                good_pic=product['img'],
                good_link=product['link'],
                good_platform=product['platform']
            )
            good.save()
        user_good=User_good.objects.create(
            user_id=user,
            good_id=good
        )
        user_good.save()
        log=Log.objects.create(
            good_id=good,
            timestamp=timezone.now(),
            prise=product['price']
        )
        log.save()
        response['message'] = 'success'

    except Exception as e:
        response['message'] = 'fail'
        response['error'] = str(e)
    return JsonResponse(response)

@csrf_exempt
def UnstarProduct(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('user_id')
        good_id = body.get('good_id')
        print(good_id)
        try:
            user = User.objects.get(user_id=user_id)
            good = Goods.objects.get(good_id=good_id)
            record = User_good.objects.filter(
                user_id=user,
                good_id=good
            ).first()
            if record:
                record.delete()
                exists=User_good.objects.filter(good_id=good_id).exists()
                if not exists:
                    good.delete()
                return JsonResponse({'message': 'success'})
            else:
                return JsonResponse({'error': 'Record not found'}, status=404)
                
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Goods.DoesNotExist:
            return JsonResponse({'error': 'Good not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def PriceHistory(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        good_id = body.get('good_id')
        good=Goods.objects.get(good_id=good_id)
        logs = Log.objects.filter(good_id=good).order_by('timestamp').values('timestamp', 'prise')
        return JsonResponse({'logs': list(logs)})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def UserInfo(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('user_id')
        user=User.objects.get(user_id=user_id)
        return JsonResponse({'user_id':user.user_id,'username':user.username,'email':user.email,'phone':user.phone})
    else:
        return JsonResponse({'error': 'Unknown error'}, status=400)
    
@csrf_exempt
def UserStats(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('user_id')
        user=User.objects.get(user_id=user_id)
        goods=User_good.objects.filter(user_id=user).values_list('good_id',flat=True)
        good_count=len(goods)
        jd_count=0
        vph_count=0
        sn_count=0
        for good_id in goods:
            good=Goods.objects.get(good_id=good_id)
            if(good.good_platform=='京东'):
                jd_count+=1
            elif(good.good_platform =='唯品会'):
                vph_count+=1
            elif(good.good_platform =='苏宁'):
                sn_count+=1
        return JsonResponse({'totalGoods':good_count,'jdGoods':jd_count,'vphGoods':vph_count,'snGoods':sn_count})
    else:
        return JsonResponse({'error': 'Unknown error'}, status=400)

@csrf_exempt
def UserEdit(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('user_id')
        user = User.objects.get(user_id=user_id)
        
        username = body.get('username')
        email = body.get('email')
        phone = body.get('phone')
        new_password = body.get('newPassword')
        
        if(username!=user.username):
            if User.objects.filter(username=username).exclude(user_id=user_id).exists():
                return JsonResponse({'error': '用户名已存在'}, status=400)
            else: 
                user.username = username
        if(email!=user.email):
            if User.objects.filter(email=email).exclude(user_id=user_id).exists():
                return JsonResponse({'error': '邮箱已被使用'}, status=400)
            else:
                user.email = email
                
        if(phone!=user.phone):
            user.phone = phone
        
        if new_password:
            user.password = new_password
            
        user.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'error': 'Unknown error'}, status=400)

@csrf_exempt
def TestEmail(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body.get('user_id')
        user=User.objects.get(user_id=user_id)
        subject='测试邮件'
        message='测试邮件'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'success'})

@csrf_exempt
def PriceHistoryTest(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        good_id = body.get('good_id')
        good=Goods.objects.get(good_id=good_id)
        latest_log=Log.objects.filter(good_id=good).order_by('-timestamp').first()
        latest_timestamp=latest_log.timestamp
        latest_prise=latest_log.prise
        for i in range(3):
            latest_timestamp=latest_timestamp-timedelta(hours=8)
            latest_prise=latest_prise-10
            log=Log.objects.create(
                good_id=good,
                timestamp=latest_timestamp,
                prise=latest_prise
            )
            log.save()

        logs = Log.objects.filter(good_id=good).order_by('timestamp').values('timestamp', 'prise')
        return JsonResponse({'logs': list(logs)})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

