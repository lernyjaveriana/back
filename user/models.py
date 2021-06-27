from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
#from lerny.models import Company

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import Group

# Create your models here.


class MyUserManager(BaseUserManager):

    def create_user(self, user_name, user_surname, country, city, mail, identification, password):

        if not identification:
            raise ValueError("debe ingresar numero de identificacion")

        password = make_password(password)
        user = self.model(
            user_name=user_name,
            mail=self.normalize_email(mail),
            user_surname=user_surname,
            country=country,
            city=city,
            identification=identification, password = password)
        user.save(using = self._db)
        return user

    def create_superuser(self, user_name, user_surname, country, city, mail, identification, password):
        user=self.create_user(user_name=user_name,
            user_surname=user_surname,
            country=country,
            city=city,
            mail=mail,
            identification=identification, password=password)
        user.admin_user=True
        user.is_staff = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField('user name', max_length=50, null=False)
    user_surname = models.CharField('user surname', max_length=50, null=False)
    country = models.CharField('country', max_length=20, null=False)
    city = models.CharField('city', max_length=20, null=False)
    uid = models.CharField('uid', max_length=100, default="", null=True)
    #passw = models.CharField('passw', max_length=20, null=False)
    mail = models.CharField('mail', max_length=100,unique=True,blank=True, null=True)
    notification = models.BooleanField(default=True)
    last_view_date = models.DateTimeField('last view date', null=True)
    points = models.FloatField('points', default=0.0, null=False)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    active_user = models.BooleanField(default = True)
    admin_user= models.BooleanField(default = False)
    identification = models.CharField('identification',unique=True, max_length=20, default = "12345")
    company = models.ForeignKey('lerny.Company', on_delete=models.CASCADE, null=True, related_name='company')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null = True, related_name='group')
    objects=MyUserManager()

    USERNAME_FIELD = "identification"
    REQUIRED_FIELDS =  ["user_name","user_surname","country","city","mail"]

    def __str__(self):
        return f'{self.user_name},{self.user_surname},{self.identification}'
    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.admin_user




    