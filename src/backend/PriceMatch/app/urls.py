from django.urls import path
from .views import GoodsList,Signup,Signin
from .views import CheckLogin,Login,GoodSearch
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('api/Goods/', GoodsList, name='Goods-list'),
	path('user/sign_up/',Signup,name='sign_up'),
	path('user/sign_in/',Signin,name='sign_in'),
	path('search/checklogin/',CheckLogin,name='check_login'),
	path('search/login/',Login,name='login'),
	path('search/goodsearch/',GoodSearch,name='good_search'),
]