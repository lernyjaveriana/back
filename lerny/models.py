from django.db import models
from user.models import User
# Create your models here.

class Lerny(models.Model):
	lerny_name = models.CharField('lerny name', max_length = 100, null=False)
	description = models.CharField('description', max_length = 300, null=False)
	url_image = models.CharField('url image', max_length = 300)
	category = models.CharField('category', max_length = 100)
	price = models.FloatField('price', null = False)
	creation_date = models.DateTimeField('creation date', auto_now_add = True)
class MicroLerny(models.Model):
	micro_lerny_title = models.CharField('microlerny title', max_length = 200, null=False)
	micro_lerny_subtitle = models.CharField('microlerny subtitle', max_length = 300, null=False)
	update_date = models.DateTimeField('update date', auto_now = True)
	creation_date = models.DateTimeField('creation date', auto_now_add = True)
	lerny = models.ForeignKey(Lerny, on_delete=models.CASCADE, null = False)

class TreeMicroLerny(models.Model):
	dady_micro_lerny = models.ForeignKey(MicroLerny, on_delete=models.CASCADE, related_name='dady_micro_lerny')
	son_micro_lerny = models.ForeignKey(MicroLerny, on_delete=models.CASCADE, related_name='son_micro_lerny')

class Resource(models.Model):
	title = models.CharField('title', max_length = 100)
	description = models.CharField('description', max_length = 300)
	content_url = models.CharField('content_url', max_length = 100, null=False)
	content_type = models.CharField('microlerny title', max_length = 200, null=False)
	phase = models.CharField('phase', max_length = 3, null=False)
	creation_date = models.DateTimeField('creation date', auto_now_add = True)
	points = models.FloatField('points', null=False)
	microlerny = models.ForeignKey(MicroLerny, on_delete=models.CASCADE, null = False)

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
    micro_lerny_id = models.ForeignKey(MicroLerny, on_delete=models.CASCADE, null = False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    user_microlerny_points = models.FloatField('user microlerny points', null=False)
    last_view_date = models.DateTimeField('last view date', null=True)

class User_State(models.Model):
    lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null = False)
    micro_lerny_id = models.ForeignKey(MicroLerny, on_delete=models.CASCADE, null = False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    resource_id = models.ForeignKey(Resource, on_delete=models.CASCADE,null = False)
    last_view_date = models.DateTimeField('last view date', null=True)