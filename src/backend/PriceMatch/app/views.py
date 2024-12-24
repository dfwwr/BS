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
jd_map={}
sn_map={}
vph_map={}

def item_list(request):
    item_list = Goods.objects.all()
    paginator = Paginator(item_list, 10)  # 每页 10 个条目

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/item_list.html', {'page_obj': page_obj})

@csrf_exempt
def GoodsList(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        userid = body.get('user_id')
        good_ids=User_good.objects.filter(user_id=userid).values_list('good_id',flat=True)
        goods = Goods.objects.filter(good_id=good_ids)\
        .values('good_name','good_description',
          'good_scale','good_type','good_pic')
        goods_list=list(goods)
        return JsonResponse(goods_list,safe=False)

@csrf_exempt
def Signup(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
        email=body.get('email')
        phone=body.get('phone')
        if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)
        if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists.'}, status=400)
        if User.objects.filter(phone=phone).exists():
                return JsonResponse({'error': 'Phone already exists.'}, status=400)
        user = User(username=username, password=password,
                                 email=email,phone=phone)
        user.save()
        return JsonResponse({'message': 'User created successfully    Jump to login page after 1 seconds'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

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
def get_product_data_taobao(request):
    response = {}
    try:
        payload = {}

        response['payload'] = payload
        response['code'] = 0
        response['err'] = ""
    except Exception as e:
        response['code'] = 1
        response['err'] = str(e)
        print(e)
    
    return JsonResponse(response)

@csrf_exempt
def CheckLogin(request):
    response = {}
    req = json.loads(request.body)
    
    if request.method == 'POST':
        if req.get('method') == 'check':
            response['jd'] = 'true'
            response['vph'] = 'true'
            response['sn'] = 'true'
            
            try:
                jd_cookie = jdCookie.objects.get(user_id=req['user_id'])
                if timezone.now() - jd_cookie.created_at > timedelta(days=1):
                    jdCookie.objects.filter(user_id=req['user_id']).delete()
                    raise jdCookie.DoesNotExist
            except jdCookie.DoesNotExist:
                response['jd'] = 'false'
            
            try:
                vph_cookie = vphCookie.objects.get(user_id=req['user_id'])
                if timezone.now() - vph_cookie.created_at > timedelta(days=1):
                    vphCookie.objects.filter(user_id=req['user_id']).delete()
                    raise vphCookie.DoesNotExist
            except vphCookie.DoesNotExist:
                response['vph'] = 'false'
            
            try:
                sn_cookie = snCookie.objects.get(user_id=req['user_id'])
                if timezone.now() - sn_cookie.created_at > timedelta(days=1):
                    snCookie.objects.filter(user_id=req['user_id']).delete()
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
    if request.method == 'POST':
        if req['method'] == 'jd_login':
            
            if req['user_id'] not in jd_map:
                bro = avoid_check()
                bro.get('https://passport.jd.com/new/login.aspx')
                res = jd_login(bro)
            else:
                res = jd_login(jd_map[req['user_id']])
            
            if res[0] == 'success':
                jdCookie.objects.create(id=req['user_id'], cookie=json.dumps(res[1]))
                response['message'] = '扫码成功'
            elif res[0] == 'fail':
                jd_map[req['user_id']] = res[1]
                response['qrcode'] = res[2]
                response['message'] = '待扫码'
                
        elif req['method'] == 'vph_login':
            if req['user_id'] not in vph_map:
                bro = avoid_check()
                bro.get('https://category.vph.com/suggest.php?keyword=1')
                res = vph_login(bro)
            else:
                res = vph_login(vph_map[req['user_id']])
            if res[0] == 'success':
                vphCookie.objects.create(user_id=req['user_id'], cookie=json.dumps(res[1]))
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
                snCookie.objects.create(user_id=req['user_id'], cookie=json.dumps(res[1]))
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
    if request.method == 'POST':
        if req['method'] == 'jd_search':
            jd_cookie = jdCookie.objects.get(id=user_id)
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
        elif req['method'] == 'vip_search':
            vph_cookie = vphCookie.objects.get(id=user_id)
            cookies = json.loads(vph_cookie.cookie)
            if req['user_id'] not in vph_map:
                bro = avoid_check()
                bro.get('https://www.vip.com/')
                for cookie in cookies:
                    cookie['domain'] = '.vip.com'
                    bro.add_cookie(cookie)
                #sleep(3)
            else:
                bro = vph_map[user_id]
            response['products'], vph_map[user_id] =\
                vph_crawler(req['name'], bro)
            response['message'] = 'success'
        elif req['method'] == 'sn_search':
            sn_cookie = snCookie.objects.get(user_id=req['user_id'])
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

