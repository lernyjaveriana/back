from rest_framework import serializers
from .models import *

class LernySerializer(serializers.ModelSerializer):
	class Meta:
		model = Lerny
		fields = '__all__'

class MicroLernySerializer(serializers.ModelSerializer):
	class Meta:
		model = MicroLerny
		fields = ['micro_lerny_title','id']


class ResourceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Resource
		fields = '__all__'

class UserResourceSerializer(serializers.ModelSerializer):
	class Meta:
		model = User_Resource
		fields = '__all__'