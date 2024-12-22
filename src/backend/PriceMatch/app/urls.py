from django.urls import path
from .views import GoodsList
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('api/Goods/', GoodsList, name='Goods-list'),
]