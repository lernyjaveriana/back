from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import *
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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

@login_required(login_url='/accounts/login/')
def UserStateResource(request):
	user = request.user
	company = user.company
	try:
		lernys = Lerny.objects.filter(lerny_company__company_id=company.pk)
	except:
		lernys = []
	context = {'lernys': lernys}
	#microlerny = MicroLerny.objects.filter(lerny__pk=lerny.pk)
	return render(request, 'lerny/tables.html', context)

@login_required(login_url='/accounts/login/')
def testData(request):
	user = request.user
	print(user)
	#user = User.objects.get(pk=2)
	list_data = []
	context = {}
	try:
		group = user.group.name
	except:
		group = None

	if (group=="Facilitadores"):
		company = user.company
		if company:
			#filtro todos los lernys que pertenecen a la empresa que se encuentra asignado el colaborador
			lernys = Lerny.objects.filter(lerny_company__company_id=company.pk).values_list("pk", flat=True)
			user_resources = User_Resource.objects.filter(resource_id__microlerny__lerny__in=lernys).order_by("resource_id__microlerny__lerny__lerny_name")
			for i in user_resources:
				data = {}
				data['pk'] = '<div align="center"><button type="button" class="btn btn-primary" data-dismiss="modal" onclick="editRow('+str(i.pk)+')">Editar</button></div>'
				data['lerny'] = i.resource_id.microlerny.lerny.lerny_name
				data['microlerny'] = i.resource_id.microlerny.micro_lerny_title
				data['user'] = i.user_id.user_name
				data['response'] = i.user_response
				data['done'] = i.done
				data['points'] = i.points
				list_data.append(data)
			context = list_data
			print(context)
			return JsonResponse({"data":context}, safe = False)
		else:
			return JsonResponse({"data":context}, safe = False)
	else:
		return JsonResponse({"data":context}, safe = False)

@csrf_exempt
def editStateResource(request):

	pk = request.POST.get('pk')

	points = request.POST.get('points')

	user_resource = User_Resource.objects.get(pk = pk)

	user_resource.points = points

	user_resource.save()

	return JsonResponse({"status": "success"})

#@login_required(login_url='/accounts/login/')
#def UserState(response):