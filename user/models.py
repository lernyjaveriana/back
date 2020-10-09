from django.db import models
from lerny.models import Lerny, Resource, MicroLerny
#from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.


class User(models.Model):
    user_name = models.CharField('user name', max_length=50, null=False)
    user_surname = models.CharField('user surname', max_length=50, null=False)
    country = models.CharField('country', max_length=20, null=False)
    city = models.CharField('city', max_length=20, null=False)
    passw = models.CharField('passw', max_length=20, null=False)
    cellphone_number = models.CharField('cellphone number', max_length=20, null=False)
    mail = models.CharField('mail', max_length=20, null=True)
    notification = models.BooleanField(default=True)
    last_view_date = models.DateTimeField('last view date', null=True)
    points = models.FloatField('points', null=False)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)


class User_Lerny(models.Model):
    lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null = False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    lerny_points = models.FloatField('lerny points', null=False)
    opinion = models.CharField('opinion', max_length=300, null=True)
    opinion_points = models.FloatField('opinion points', null=False)
    valor = models.FloatField('valor', null=False)
    bill_state = models.BooleanField(default=False)
    reference = models.CharField('reference', max_length=20, null=False)
    pay_date = models.DateTimeField(null=True)
    last_view_date = models.DateTimeField('last view date', null=True)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)

class User_Resource(models.Model):
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE,null = False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    done = models.BooleanField(default=False)
    user_response = models.CharField('user response', max_length=300, null=True)
    response_date = models.DateTimeField('response date', null=True)
    last_view_date = models.DateTimeField('last view date', null=True)
    done_date = models.DateTimeField('done date', auto_now_add=True)


class User_Micro_Lerny(models.Model):
    lerny_id = models.ForeignKey(MicroLerny, on_delete=models.CASCADE, null = False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    user_microlerny_points = models.FloatField('user microlerny points', null=False)
    last_view_date = models.DateTimeField('last view date', null=True)
