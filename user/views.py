from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import serializers
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User



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
		if (key=="LOGIN_USER"):
			serializer = UserLoginSerializer(data=request)
			serializer.is_valid(raise_exception=True)
			user, token = serializer.save()

			data = {
				"fulfillmentMessages": [
					{
						"text": {
							"text": [
								"Bienvenido a lerny back"
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
												"title":"Hola "+ UserSerializer(user).data["user_surname"] + ", un gusto volver a verte!",
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
														"payload": "ver_microlernys"
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
		elif(key=="api2"):
			data = {
				{
					"fulfillmentMessages": [
						{
							"text": {
								"text": [
									"Bienvenido a lerny back"
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
													"title": "Lista de microlernys",
													"image_url": "https://www.dropbox.com/s/ha2re0473e67eqo/LOGO%20LERNY%20NUEVO%20_Mesa%20de%20trabajo%201%20copia%207.png",
													"subtitle": "Elige el microlerny que deseas estudiar",
													"buttons": 
													[
														{
															"type": "postback",
															"title": "Comprar c",
															"payload": "cargar_curso"
														},
														{
															"type": "postback",
															"title": "Iniciar sesión",
															"payload": "iniciar_sesion"
														},
														{
															"type": "postback",
															"title": "Información de contacto",
															"payload": "info_contacto"
														}
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
			}
		else:
			data = {}

		return Response(data, status=status.HTTP_201_CREATED)

