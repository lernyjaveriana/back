from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, user_name, user_surname, country, city, mail,identifications):

        if not identifications:
            raise ValueError("debe ingresar numero de identificacion")
        user = self.model(
            user_name=user_name,
            mail=self.normalize_email(mail),
            user_surname=user_surname,
            country=country,
            city=city,
            identifications=identifications)
        user.set_password(identifications)
        user.save()
        return user
    def create_superuser(self,user_name,user_surname,country,city,password,mail,identifications):
        user=self.create_user(user_name=user_name,
            user_surname=user_surname,
            country=country,
            city=city,
            mail=mail,
            identifications=identifications)
        user.admin_user=True
        user.save()
        return user


class User(AbstractBaseUser):
    user_name = models.CharField('user name', max_length=50, null=False)
    user_surname = models.CharField('user surname', max_length=50, null=False)
    country = models.CharField('country', max_length=20, null=False)
    city = models.CharField('city', max_length=20, null=False)
    #passw = models.CharField('passw', max_length=20, null=False)
    mail = models.CharField('mail', max_length=100,unique=True,blank=True, null=True)
    notification = models.BooleanField(default=True)
    last_view_date = models.DateTimeField('last view date', null=True)
    points = models.FloatField('points', default=0.0, null=False)
    creation_date = models.DateTimeField('creation date', auto_now_add=True)
    active_user = models.BooleanField(default = True)
    admin_user= models.BooleanField(default = False)
    identifications = models.CharField('identifications',unique=True, max_length=20, default = "12345")
    objects=MyUserManager()

    USERNAME_FIELD = "identifications"
    REQUIRED_FIELDS =  ["user_name","user_surname","country","city","mail"]

    def __str__(self):
        return f'{self.user_name},{self.user_surname},{self.country},{self.city}'
    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.admin_user


