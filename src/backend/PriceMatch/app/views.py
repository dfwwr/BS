# views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Goods,User,User_good,Log
from .serializers import GoodsSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def item_list(request):
    item_list = Goods.objects.all()
    paginator = Paginator(item_list, 10)  # 每页 10 个条目

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/item_list.html', {'page_obj': page_obj})

@csrf_exempt
def GoodsList(request):
    if request.method == 'GET':
        Goods = Goods.objects.all()
        serializer = GoodsSerializer(Goods, many=True)
        return JsonResponse(serializer.data)