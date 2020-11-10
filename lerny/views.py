from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import *
from .models import *


class LernyManageGet(APIView):

	serializers_class = LernySerializer

	def get(self, request, cellphone_number, format=None):
		try:
			user_lerny = User_Lerny.objects.filter(user_id__cellphone_number = cellphone_number).order_by('last_view_date').first()
			lerny = Lerny.objects.filter(pk=user_lerny.lerny_id)
			data = LernySerializer(lerny, many=True).data
		except:
			data = None
		
		return Response ({'lerny': data})


class MicroLernyDadAndSon(APIView):
	
	serializers_class = MicroLernySerializer

	def get(self, request, microlerny_id, format=None):

		dad = TreeMicroLerny.objects.filter(son_micro_lerny__pk=microlerny_id).values_list('dady_micro_lerny_id', flat=True)
		son = TreeMicroLerny.objects.filter(dady_micro_lerny__pk=microlerny_id).values_list('son_micro_lerny_id', flat=True)
		print(dad)
		print(son)
		
		try:
			microlerny_dad = MicroLerny.objects.filter(pk__in = dad)
			dad_data = MicroLernySerializer(microlerny_dad, many=True).data
		except:
			dad_data = None
		
		try:
			microlerny_son = MicroLerny.objects.filter(pk__in = son)
			son_data = MicroLernySerializer(microlerny_son, many=True).data
		except:
			son_data = None
		
		return Response ({'dad': dad_data, 'son': son_data })

		

