from django.db import models

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