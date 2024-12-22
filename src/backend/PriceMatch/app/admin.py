from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Goods,User,User_good,Log

admin.site.register(Goods)
admin.site.register(User)
admin.site.register(User_good)
admin.site.register(Log)