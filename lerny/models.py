from django.db import models
from user.models import User
# Create your models here.


class Lerny(models.Model):
	lerny_name = models.CharField('lerny name', max_length=100, null=False)
	description = models.CharField('description', max_length=300, null=False)
	url_image = models.CharField('url image', max_length=300)
	category = models.CharField('category', max_length=100)
	price = models.FloatField('price', null=False)
	creation_date = models.DateTimeField('creation date', auto_now_add=True)
	REQUIRED_FIELDS = ["lerny_name"]

	def __str__(self):
		return f'{self.lerny_name}'


class MicroLerny(models.Model):
	micro_lerny_title = models.CharField(
		'microlerny title', max_length=200, null=False)
	micro_lerny_subtitle = models.CharField(
		'microlerny subtitle', max_length=300, null=False)
	microlerny_image_url = models.CharField(
		'microlerny image url', max_length=300, null=True)
	update_date = models.DateTimeField('update date', auto_now=True)
	creation_date = models.DateTimeField('creation date', auto_now_add=True)
	lerny = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return f'{self.micro_lerny_subtitle},{self.micro_lerny_title}'


class TreeMicroLerny(models.Model):
	dady_micro_lerny = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, related_name='dady_micro_lerny')
	son_micro_lerny = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, related_name='son_micro_lerny')

	def __str__(self):
		return f'{self.dady_micro_lerny},{self.son_micro_lerny}'


class Resource(models.Model):
	title = models.CharField('title', max_length=100)
	description = models.CharField('description', max_length=300)
	content_type = models.CharField(
		'microlerny title', max_length=200, null=False)
	previous_text = models.CharField('previous text', max_length=600, blank=True)
	phase = models.CharField('phase', max_length=3, null=False)
	creation_date = models.DateTimeField('creation date', auto_now_add=True)
	points = models.FloatField('points', default=1, blank=True)
	microlerny = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, null=False)
	image_url = models.CharField('image url', max_length=200, null=False)
	resource_type = models.CharField('resource type', max_length=200, null=False)
	first_button = models.CharField('first button', max_length=200, blank=True)
	second_button = models.CharField('second button', max_length=200, blank=True)
	third_button = models.CharField('third button', max_length=200, blank=True)
	correct_answer = models.CharField(
		'Correct answer', max_length=200, blank=True)
	wrong_answer = models.CharField('Wrong answer', max_length=200, blank=True)
	correct_answer_button = models.IntegerField(
		'Correct answer button', default=1, blank=True)

	def __str__(self):
		return f'{self.title,self.phase,self.microlerny}'


class Media(models.Model):
	resource_id = models.ForeignKey(
		'resource', on_delete=models.CASCADE, null=False)
	content_url = models.CharField('content_url', max_length=100, null=False)
	content_type = models.CharField('content type', max_length=200, null=False)
	position = models.FloatField('position', null=False)

	def __str__(self):
		return f'{self.resource_id,self.content_type}'


class User_Lerny(models.Model):
	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	access = models.BooleanField('is accessible?',default=True)
	active = models.BooleanField('current status', default=False)

	def __str__(self):
		return f'{self.user_id},{self.lerny_id}'


class User_Resource(models.Model):
	resource_id = models.ForeignKey(
		Resource, on_delete=models.CASCADE, null=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	done = models.BooleanField(default=False)
	user_response = models.TextField('user response', null=True)
	response_date = models.DateTimeField('response date', null=True)
	last_view_date = models.DateTimeField('last view date', null=True)
	done_date = models.DateTimeField('done date', auto_now_add=True)
	points = models.FloatField('points', null=True)

	def __str__(self):
		return f'{self.resource_id},{self.user_id}'


class User_Micro_Lerny(models.Model):
	micro_lerny_id = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, null=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	user_microlerny_points = models.FloatField(
		'user microlerny points', null=False)
	last_view_date = models.DateTimeField('last view date', null=True)

	def __str__(self):
		return f'{self.user_id},{self.micro_lerny_id}'


class User_State(models.Model):
	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)
	micro_lerny_id = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, null=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	resource_id = models.ForeignKey(
		Resource, on_delete=models.CASCADE, null=False)
	last_view_date = models.DateTimeField('last view date', null=True)

	def __str__(self):
		return f'{self.user_id},{self.resource_id}'


class User_State_Logs(models.Model):

	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)
	micro_lerny_id = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, null=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	resource_id = models.ForeignKey(
		Resource, on_delete=models.CASCADE, null=False)
	last_view_date = models.DateTimeField('last view date', null=True)

	def __str__(self):
		return f'{self.lerny_id},{self.micro_lerny_id},{self.user_id},{self.resource_id}'


class PQR(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	user_state = models.ForeignKey(User_State,on_delete=models.CASCADE, null=True)
	pqr = models.TextField('user response', null=False)
	type = models.TextField('type', null=True)
	def __str__(self):
		return f'{self.user_id},{self.pqr}'


class Faqs_Lerny(models.Model):
	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)
	intent_name = models.CharField('intent_name', max_length=50, null=False)
	response = models.CharField('response ', max_length=300, null=False)
	url = models.CharField('url', max_length=300, null=True)
	response_type = models.CharField('response_type', max_length=30, null=True)
	title = models.CharField('title', max_length=50, blank=True)
	subtitle = models.CharField('subtitle', max_length=100, blank=True)
	but_name = models.CharField('but_name', max_length=30, blank=True)

	def __str__(self):
		return f'{self.intent_name},{self.lerny_id}'


class Faqs(models.Model):
	intent_name = models.CharField('intent_name', max_length=50, null=False)
	response = models.CharField('response ', max_length=600, null=False)
	response_type = models.CharField('response_type', max_length=30, blank=True)

	def __str__(self):
		return f'{self.intent_name}'


class Company(models.Model):
	nit = models.CharField('nit', max_length=50, null=False)
	name = models.CharField('name', max_length=50, null=False)
	country = models.CharField('country', max_length=50, null=True)
	region = models.CharField('region', max_length=50, null=True)
	city = models.CharField('city', max_length=50, null=True)
	direction = models.CharField('direction', max_length=100, null=True)
	phone = models.CharField('phone', max_length=50, null=True)
	email = models.CharField('email', max_length=50, null=True)
	web = models.CharField('web', max_length=50, null=True)
	creation_date = models.DateTimeField('creation date', auto_now_add=True)

	def __str__(self):
		return f'{self.nit},{self.name}'


class Lerny_Company(models.Model):
	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)
	company_id = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
	date = models.DateTimeField('date', auto_now_add=True)

	def __str__(self):
		return f'{self.lerny_id},{self.company_id}'


class Group(models.Model):
	Group_name = models.CharField('group name', max_length=50, null=False)
	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return f'{self.Group_name},{self.lerny_id}'


class User_Group(models.Model):
	Group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)
	User_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return f'{self.Group_id},{self.User_id}'


class Support_Resource(models.Model):
	name = models.CharField('name', max_length=50, null=False)
	text = models.CharField('text ', max_length=300, null=False)
	Response_is_text = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name}'


class Support_Resource_Microlerny_Lerny(models.Model):
	Support_Resource_id = models.ForeignKey(
		Support_Resource, on_delete=models.CASCADE, null=False)
	lerny_id = models.ForeignKey(Lerny, on_delete=models.CASCADE, null=False)
	Microlerny_id = models.ForeignKey(
		MicroLerny, on_delete=models.CASCADE, related_name='micro_lerny_id')

	def __str__(self):
		return f'{self.Support_Resource_id,self.Microlerny_id}'


class Score(models.Model):
	Support_Resource_Microlerny_Lerny = models.ForeignKey(
		Support_Resource_Microlerny_Lerny, on_delete=models.CASCADE, null=False)
	User = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	Response = models.CharField('response ', max_length=300, null=False)
	Response_Int = models.FloatField('points', null=True)

	def __str__(self):
		return f'{self.Support_Resource_Microlerny_Lerny,self.Response}'
