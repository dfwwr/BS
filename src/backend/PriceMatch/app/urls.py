from django.urls import path
from .views import GoodsList,Signup,Signin
from .views import CheckLogin,Login,GoodSearch
from .views import StarProduct, UnstarProduct,PriceHistory,PriceHistoryTest
from .views import UserInfo,UserStats,UserEdit
from .views import TestEmail
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('star/Goods/', GoodsList, name='Goods-list'),
	path('user/sign_up/',Signup,name='sign_up'),
	path('user/sign_in/',Signin,name='sign_in'),
	path('search/checklogin/',CheckLogin,name='check_login'),
	path('search/login/',Login,name='login'),
	path('search/goodsearch/',GoodSearch,name='good_search'),
	path('good/star_product/',StarProduct,name='star_product'),
	path('good/unstar_product/', UnstarProduct, name='unstar_product'),
	path('good/price_history/',PriceHistory,name='price_history'),
	path('good/price_history_test/',PriceHistoryTest,name='price_history_test'),
	path('user/info/',UserInfo,name='user_info'),
	path('user/stats/',UserStats,name='user_stats'),
	path('user/edit/',UserEdit,name='user_edit'),
	path('user/testemail/',TestEmail,name='test_email'),
]