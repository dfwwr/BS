from rest_framework import serializers
from .models import Goods,User,User_good,Log

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'