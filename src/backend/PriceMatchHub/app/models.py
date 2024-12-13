from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255,null=False,unique=True)
    password = models.CharField(max_length=255,null=False)
    email = models.CharField(max_length=255,null=False,unique=True)
    phone=models.CharField(max_length=15,null=True)
    
    def __str__(self):
        return self.username

class Goods(models.Model):
    good_id=models.AutoField(primary_key=True)
    good_name=models.CharField(max_length=255,null=False)
    good_description=models.TextField(null=True)
    good_scale=models.CharField(max_length=255,null=False)
    good_type=models.CharField(max_length=255,null=False)
    good_pic=models.ImageField(upload_to='./images/',null=True)
    def __str__(self):
        return self.good_name

class Log(models.Model):
    log_id=models.AutoField(primary_key=True)
    good_id=models.ForeignKey(Goods,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    prise=models.FloatField(null=False)
    def __str__(self):
        return self.good_id.good_name

class User_good(models.Model):
    message_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    good_id=models.ForeignKey(Goods,on_delete=models.CASCADE)
    def __str__(self):
        return self.user_id.username