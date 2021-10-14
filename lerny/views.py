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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Avg

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


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
	context = {'have_company': True if lernys != [] else False, 'username': user.user_name}

	return render(request, 'lerny/tables.html', context)

@login_required(login_url='/accounts/login/')
def ApiStateResource(request):
	user = request.user
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
				try:
					group_id=UserGroupSerializer(User_Group.objects.get(User_id=i.user_id)).data["Group_id"]
					data['Grupo'] = GroupSerializer(Group.objects.get(pk=group_id,lerny_id=i.resource_id.microlerny.lerny.pk)).data["Group_name"]
				except:
					data['Grupo'] = ""
				
				data['pk'] = '<div align="center"><button type="button" class="btn btn-primary" data-dismiss="modal" onclick="editRow('+str(i.pk)+')">Calificar</button></div>'
				data['lerny'] = i.resource_id.microlerny.lerny.lerny_name
				data['microlerny'] = i.resource_id.microlerny.micro_lerny_title
				data['resource'] = i.resource_id.title
				data['user'] = i.user_id.user_name
				data['identification'] = i.user_id.identification
				data['response'] = i.user_response
				data['points'] = i.points
				print("ENTREGABLES",data['response'])
				list_data.append(data)
			context = list_data
			print(context)
			return JsonResponse({"data":context}, safe = False)
		else:
			return JsonResponse({"data":context}, safe = False)
	else:
		return JsonResponse({"data":context}, safe = False)

@login_required(login_url='/accounts/login/')
def charts(request):
	user = request.user
	try:
		company = user.company.pk
	except:
		company = None
	context = {"username": user.user_name, 'have_company': True if company != None else False}
	print('GRAFICAS',context)
	return render(request, 'lerny/charts.html', context);

@csrf_exempt
def editStateResource(request):

	try:
		pk = request.POST.get('pk')
		points = request.POST.get('points')
		user_resource = User_Resource.objects.get(pk = pk)
		user_resource.points = points
		user_resource.save()
		return JsonResponse({"status": "success"})
	except Exception as ex:
		return JsonResponse({"status": ex})


class lernyDetail(APIView):

	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

	def get(self, request, format=None):
		user = request.user
		lerny_id = int(request.GET["lerny_id"])
		microlerny_id = int(request.GET["microlerny_id"])
		list_data = []
		list_info_micro = []
		list_name_micro = []
		list_cont_micro = []
		list_progress_micro = []
		list_average_micro = []

		context = {}
		approved = 0

		try:
			group = user.group.name
		except:
			group = None
		try:
			company = user.company.pk
		except:
			company = None
		
		if group == "Facilitadores":
			if company:
				
				if lerny_id != -1:
					#filtro por el lerny
					lerny = Lerny.objects.get(pk=lerny_id)
				else:
					#Muestro el primer lerny asociado a la compañia
					lerny = Lerny.objects.filter(lerny_company__company_id=company).first()

				#selecciono todos los usuarios inscritos en el lerny
				user_lerny = User_Lerny.objects.filter(lerny_id=lerny.pk)
				#selecciono todos los recursos del lerny
				resource_lerny = Resource.objects.filter(microlerny__lerny__pk=lerny.pk)
				if microlerny_id != -1:
					#Filtro por microlerny
					resource_lerny = resource_lerny.filter(microlerny__pk=microlerny_id)
				#cuento la cantidad de recursos obligatorios que se requieren para aprobar el lerny
				cont_resource_lerny = resource_lerny.count()
				print("cont_resource_lerny="+str(cont_resource_lerny))
				#selecciono todos los registros de recursos obligatorios aprobados por usuarios
				user_resource = User_State_Logs.objects.filter(micro_lerny_id__lerny__pk=lerny.pk)
				for i in user_lerny:
					data = {}
					data['user'] = i.user_id.user_name
					data['identification'] = i.user_id.identification
					cont = user_resource.filter(user_id__pk=i.user_id.pk).count()
					if cont_resource_lerny != 0:
						if cont == cont_resource_lerny:
							data['done'] = "Aprobado"
							data['progress'] = 100
							approved = approved + 1
						elif cont == 0:
							data['done'] = "No aprobado"
							data['progress'] = 0
						else:
							data['done'] = "No aprobado"
							data['progress'] = round(((cont*100)/cont_resource_lerny), 2)
					else:
						data['done'] = "Aprobado"
						#resource_lerny = Resource.objects.filter(microlerny__lerny__pk=lerny.pk)
						data['progress'] = round(((cont*100)/cont_resource_lerny), 2)
						approved = approved + 1
					list_data.append(data)
					cont = 0
				if user_lerny.count() != 0:
					data_approved = [round(((approved*100)/user_lerny.count()), 2), round((((user_lerny.count()-approved)*100)/user_lerny.count()), 2)]
				else:
					data_approved = [0, 0]

				microlernys = MicroLerny.objects.filter(lerny__pk=lerny.pk).order_by('pk')
				
				for i in microlernys:
					data = {}
					cant = user_resource.filter(micro_lerny_id__pk=i.pk).order_by('user_id').distinct('user_id').count()
					data['microlerny'] = i.micro_lerny_subtitle
					data['cant'] = cant
					print('CUENTA DE RECURSOS VISTOS ',cant)
					print('CUENTA RECURSOS ',user_lerny.count())
					if user_lerny.count()!= 0:
						data['progress'] = round(((cant*100)/user_lerny.count()), 2)
					else:
						data['progress'] = 0
					user_resources = User_Resource.objects.filter(resource_id__microlerny__lerny__pk=lerny.pk, done=True)
					avg = user_resources.filter(resource_id__microlerny__pk=i.pk).aggregate(average=Avg('points'))
					data['average'] = avg['average']
					list_info_micro.append(data)
					list_name_micro.append(data['microlerny'])
					list_cont_micro.append(data['cant'])
					list_progress_micro.append(data['progress'])
					list_average_micro.append(data['average'])

				context = {	'data': list_data,
							'approved': data_approved,
							'info_micro':list_info_micro, 
							'name_micro':list_name_micro, 
							'cont_micro':list_cont_micro,
							'progress_micro': list_progress_micro,
							'average_micro': list_average_micro,
						}
				return Response (context)
		
				context = {'data': "No tiene una compañia asignada"}
				return Response ({'data': context})
		else:
			context = {'data': "No tiene permisos para ingresar"}
			return Response ({'data': context})


def getLernyList(request):

	user = request.user
	json = []

	try:
		company = user.company.pk
	except:
		company = None
	
	if company:
		lernys = Lerny.objects.filter(lerny_company__company_id=company)

		for lerny in lernys:
			json.append({'pk': lerny.pk, 'name': lerny.lerny_name})
	else:
		json = [{'pk': None, 'name': 'No tiene asignada una compañia'}]

	return JsonResponse(json, safe=False)

@csrf_exempt
def getMicrolernyList(request):
	id_lerny = request.POST.get('pk')
	microlernys = MicroLerny.objects.filter(lerny__pk = id_lerny)
	json = []

	for microlerny in microlernys:
		json.append({'pk': microlerny.pk, 'name': microlerny.micro_lerny_title})

	return JsonResponse(json, safe=False)