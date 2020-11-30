from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import serializers
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from lerny.models import *
from lerny.serializers import *
from datetime import datetime

class UserManageGet(APIView):

	serializers_class = UserSerializer

	def get(self, request, user_id, format=None):
		user = User.objects.filter(id = user_id)
		data = UserSerializer(user, many=True).data
		return Response ({'user': data})


class UserManagePost(APIView):
	
	def post(self, request):
		
		serializers = UserSerializer(data=request.data)

		if serializers.is_valid():
			serializers.save()
			return Response({'user': serializers.data})
		else:
			return Response(
				serializers.errors, status=status.HTTP_400_BAD_REQUEST	
			)

class ApiManager(APIView):

	def post(self, request):
		print(request.data['queryResult']['parameters'])
		request= request.data['queryResult']['parameters']
		key = request['LERNY_INTENT']
		#key = "send_task"

		if (key=="LOGIN_USER"):
			serializer = UserLoginSerializer(data=request)
			serializer.is_valid(raise_exception=True)
			user, token = serializer.save()

			data = {
				"fulfillmentMessages": [
					{
						"text": {
							"text": [
								"Bienvenido a lerny"
							]
						}
					},
					{
						"payload": {
							"facebook": {
								"attachment": {
									"type": "template",
									"payload": 
									{
										"template_type": "generic",
										"elements": 
										[
											{
												"title":"Hola "+ UserSerializer(user).data["user_name"] + ", un gusto volver a verte!",
												"image_url": "https://www.dropbox.com/s/ha2re0473e67eqo/LOGO%20LERNY%20NUEVO%20_Mesa%20de%20trabajo%201%20copia%207.png",
												"subtitle": "Para comenzar por favor selecciona una opción.",
												"buttons": 
												[
													{
														"type": "postback",
														"title": "Continuar lerny",
														"payload": "continuar_curso"
													},
													{
														"type": "postback",
														"title": "ver microlernys",
														"payload": "LIST_MICROLERNYS"
													},
												]
											}
										]
									}
								}
							}
						}
					}
				]
			}

			# data = {
			# 	"followupEventInput": {
			# 		"name": "Login",
			# 		"languageCode": "en-US",
			# 		"parameters": {
			# 			"user": UserSerializer(user).data,
			# 			"access_token": token
			# 			}
			# 		}
			# 	}
		elif(key=="LIST_MICROLERNYS"):
			#lerny = request['LERNY_INTENT']
			serializers_class = MicroLernySerializer
			micro_lerny = MicroLerny.objects.all()
			data = MicroLernySerializer(micro_lerny, many=True).data
			i=0
			temp=[]
			#print(json.dumps(data))
			while(i<len(data)):
				temp.append({
						"type": "postback",
						"title": data[i]['micro_lerny_title'],
						"payload": data[i]['id']
					},)
				
				i+=1

			data = {
				"fulfillmentMessages": [
					{
						"text": {
							"text": [
								"Lista de Microlernys"
							]
						}
					},
					{
						"payload": {
							"facebook": {
								"attachment": {
									"type": "template",
									"payload": 
									{
										"template_type": "generic",
										"elements": 
										[
											{
												"title":"Microlernys disponibles",
												"image_url": "https://www.dropbox.com/s/ha2re0473e67eqo/LOGO%20LERNY%20NUEVO%20_Mesa%20de%20trabajo%201%20copia%207.png",
												"subtitle": "Para comenzar por favor selecciona una opción.",
												"buttons": 
												temp
											}
										]
									}
								}
							}
						}
					}
				]
			}
		
		elif(key=="api3"):
			user_id = 1
			serializers_class = ResourceSerializer
			user_state = User_State.objects.filter(user_id=user_id)
			if(user_state):
				user_state = user_state.first()
				phase = user_state.resource_id.phase
				if(phase == 'pre'):
					resourse = Resource.objects.get(microlerny = user_state.micro_lerny_id, phase='dur')
					user_state.resource_id = resourse
					user_state.save()
					data = ResourceSerializer(resourse).data
				elif(phase == 'dur'):
					resourse = Resource.objects.get(microlerny = user_state.micro_lerny_id, phase='pos')
					user_state.resource_id = resourse
					user_state.save()
					data = ResourceSerializer(resourse).data
				elif(phase == 'pos'):
					try:
						son = TreeMicroLerny.objects.filter(dady_micro_lerny__pk=user_state.micro_lerny_id).values_list('son_micro_lerny_id', flat=True)
						microlerny_son = MicroLerny.objects.filter(pk__in = son).first()
						resourse = Resource.objects.get(microlerny = microlerny_son.id, phase='pre')
						user_state.resource_id = resourse.id
						user_state.micro_lerny_id = microlerny_son.id
						user_state.save()
						data = ResourceSerializer(resourse).data
					except:
						data = None
				else:
					data = None
			else:
				lerny_id = 1
				micro_lerny = MicroLerny.objects.filter(lerny__pk=lerny_id).order_by('pk').first()
				resourse = Resourse.objects.get(micro_lerny_id = micro_lerny.id, phase='pre')
				user_state = User_State()
				user_state.lerny_id = lerny_id
				user_state.micro_lerny_id = micro_lerny
				user_state.user_id = user_id
				user_state.resource_id = resourse
				user_state.save()
				data = ResourceSerializer(resourse).data

		elif(key=="send_task"):
			lerny_id = 1
			url_task = "https://drive.google.com/file/d/0B-kjlg3hzpzYdnUzYllyTGxjVDFjZFhOUDh1QnJEdTk2b2g0/view?usp=sharing"
			user_id = 1
			user_state = User_State.objects.filter(user_id=user_id)
			serializers_class = UserResourceSerializer
			if(user_state):
				user_state = user_state.first()
				u_resource = User_Resource()
				u_resource.resource_id = user_state.resource_id
				u_resource.user_id = user_state.user_id
				u_resource.user_response = url_task
				u_resource.response_date = datetime.now()
				u_resource.last_view_date = datetime.now()
				u_resource.save()
				data = UserResourceSerializer(u_resource).data
			else:
				data = {"message": "el usuario no tiene tareas pendientes"} 
		else:
			data = {

			}

		return Response(data, status=status.HTTP_201_CREATED)

