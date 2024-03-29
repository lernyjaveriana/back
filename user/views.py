from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import serializers
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import action
from .models import User
from lerny.models import *
from lerny.serializers import *
from user.Intents.bucketHelper import upload_to_s3
from user.Intents.bienvenidaLerny import bienvenidaLerny
from user.Intents.listarLernys import listarLernys
from user.Intents.continueLerny import continueLerny
from user.Intents.cargarRecursoMicrolerny import cargarRecursoMicrolerny
from user.Intents.listarMicrolernys import listarMicrolernys
from user.Intents.cargarActividadFallbackIntent import cargarActividadFallback
from user.Intents.pqr import pqr
from datetime import datetime

class UserManageGet(APIView):

	serializers_class = UserSerializer

	def get(self, request, user_id, format=None):
		user = User.objects.filter(id=user_id)
		data = UserSerializer(user, many=True).data
		return Response({'user': data})


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
# After upload an activitie, it should shows you a menu
cargarActividad={
					"fulfillmentMessages": [
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
													"title": "¿Deseas hacer algo más?",
													"image_url": "https://lerny.co/wp-content/uploads/2022/Menu_chatbot2.png",
													"subtitle": "Para continuar, por favor selecciona una opción.",
													"buttons":
													[
														{
															"type": "postback",
															"title": "Cargue su archivo",
															"payload": "CARGAR_ARCHIVO"
														},
														{
															"type": "postback",
															"title": "Continuar curso",
															"payload": "continuar_curso"
														},
														{
															"type": "postback",
															"title": "Ver módulos",
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

class ApiManager(APIView):
	
	def post(self, request):
		print("request")
		print(str(request))	
		print("request.data")
		print(request.data)	
		print("request.data.intent.displayname")
		print(request.data['queryResult'])	
		print("Parameters")
		print(request.data['queryResult']['parameters'])
		print("OutputContexts")
		print(request.data['queryResult']['outputContexts'])
		print("senderId")
		sender_id=request.data['originalDetectIntentRequest']['payload']['data']['sender']['id']
		text = request.data['queryResult'].get('queryText')
		print(sender_id)

		if(request.data['queryResult']['intent']['displayName']=="LernyDefaultFallback"):
			print('fallback')
			key = "LernyDefaultFallback"
			
			urlArg = []

			# need to verify every attachement file that was sent by the user and save the url generated by fb msn
			for attachment in request.data['originalDetectIntentRequest']["payload"]["data"]["message"]["attachments"]:
				urlArg.append(attachment.get("payload").get('url'))
			print('Sender_id fallback: '+str(sender_id))
			try:
				user_id_obj = User.objects.get(uid=str(sender_id))
				user_id=UserSerializer(user_id_obj).data['identification']
			except AssertionError as error:
				
				print("An error occurred obteniendo el user id obj: "+ error)
				user_id=None
			except:
				print("Something else went wrong")
				user_id=None
				

		else:
			print('not fallback')
			x = 0
			# Identifico el user_document_id independientemente de donde se encuentre en el json
			while(x < len(request.data['queryResult']['outputContexts'])):
				
				user_id = (request.data['queryResult']['outputContexts'][x].get(
					'parameters').get('user_document_id'))
				if((request.data['queryResult']['outputContexts'][x].get('parameters').get('user_document_id')) != None):
					break
				x += 1
			if(not(user_id is None)):
				user_id = (str(int(float(user_id))))
			else:
				try:
					user_id_obj = User.objects.get(uid=str(sender_id))
					user_id=UserSerializer(user_id_obj).data['identification']
				except AssertionError as error:
					
					print("An error occurred obteniendo el user id obj: "+ error)
					user_id=None
				except:
					print("Something else went wrong")
					user_id=None

			request = request.data['queryResult']['parameters']
			key = request['LERNY_INTENT']
		# LOGIN
		if (key == "LOGIN_USER"):
			serializer = UserLoginSerializer(data=request)
			serializer.is_valid(raise_exception=True)
			user, token = serializer.save()
			# se guarda el user id
			User.objects.filter(uid=sender_id).update(uid=1)
			User.objects.filter(identification=user_id).update(uid=sender_id)

			data = {
				"fulfillmentMessages": [
					{
						"text": {
							"text": [
								"Bienvenido a lerny tu asistente educativo"
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
														"title": "Hola " + UserSerializer(user).data["user_name"] + ", es un gusto verte hoy",
														"image_url": "https://lerny.co/wp-content/uploads/2022/Menu_chatbot1.png",
														"subtitle": "Para comenzar por favor selecciona una opción.",
														"buttons":
														[
															{
																"type": "postback",
																"title": "Mis cursos",
																"payload": "LISTAR_LERNYS"
															},
															{
																"type": "postback",
																"title": "Módulos actuales", 
																"payload": "LIST_MICROLERNYS"
															},
															{
																"type": "postback",
																"title": "Continuar curso",
																"payload": "CONTINUAR_CURSO"
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
		# LOGIN
		# LISTAR MICROLERNYS
		elif(key == "LIST_MICROLERNYS"):
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj,access=True).first()
				if(lerny_active):
					micro_lerny = MicroLerny.objects.filter(lerny=lerny_active.lerny_id).order_by('pk')
					data = listarMicrolernys(micro_lerny)
				else:
					data=listarLernys(user_id)
					data["fulfillmentMessages"].append({
						"text": {
							"text": [
								"Debes seleccionar un curso antes de continuar"
							]
						}
					})
		# CONTINUAR CURSO
		elif(key == "CONTINUAR_CURSO"):
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				user_id_obj = User.objects.get(identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj,access=True).first()
				if(lerny_active):
					user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active.lerny_id)
					user_state = user_state.first()
					if(user_state):
						support_resource_microlerny_lerny = Support_Resource_Microlerny_Lerny.objects.filter(
							lerny_id=user_state.lerny_id, Microlerny_id = user_state.micro_lerny_id).order_by('pk')
						support_resource_microlerny_lerny_count=support_resource_microlerny_lerny.count()
						scores = Score.objects.filter(
							User=user_state.user_id ).order_by('pk')
						scores_count=scores.count()

						print('count support_resource_microlerny_lerny_count: '+str(support_resource_microlerny_lerny_count))
						print('count scores_count: '+str(scores_count))
						## support feature
						if(support_resource_microlerny_lerny and scores_count<support_resource_microlerny_lerny_count):
							try:
								support_resource_show = support_resource_microlerny_lerny[scores_count]
							except IndexError:
								support_resource_show = None

							if(support_resource_show):
								support_resource=support_resource_show.Support_Resource_id
								dataDB = SupportResourceSerializer(support_resource).data["text"]
								data = {
									"followupEventInput": {
										"name": dataDB,
										"parameters": {
										},
										"languageCode":"en-US"
									}
								}
						else:
							data=continueLerny(lerny_active.lerny_id,user_id_obj,user_id)
					else:
						data=continueLerny(lerny_active.lerny_id,user_id_obj,user_id)
				else:
					data=listarLernys(user_id)
					data["fulfillmentMessages"].append({
						"text": {
							"text": [
								"Debes seleccionar un curso antes de continuar"
							]
						}
					})
		# CARGAR ARCHIVO
		elif(key == "CARGAR_ARCHIVO"):
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				response = request['file_url']
				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
				user_state = User_State.objects.filter(user_id=user_id_obj,lerny_id=lerny_active.lerny_id).first()
				u_resource = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
				
				# if (response.split(':')[0] == 'https'):
				# 	response=upload_to_s3(response)
				
				if(u_resource):
					data = UserResourceSerializer(u_resource).data
					User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).update(user_response=data['user_response']+';'+response)
				else:
					print("GUARDAR ARCHIVO")
					u_resource = User_Resource()
					u_resource.resource_id = user_state.resource_id
					u_resource.user_id = user_state.user_id
					u_resource.user_response = response
					u_resource.done = True
					u_resource.response_date = datetime.now()
					u_resource.last_view_date = datetime.now()
					u_resource.save()
					

				data = cargarActividad
		# LISTAR LERNYS
		elif(key == "LISTAR_LERNYS"):
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				print("listarLernys: "+user_id)
				data=listarLernys(user_id)
		# CARGAR_REQ_MICROLERNY
		elif(key == "CARGAR_REQ_MICROLERNY"):
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				microlerny = (int(request["microlerny_num"]))
				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj,access=True).first()
				if(lerny_active):
					user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active.lerny_id)
					data=cargarRecursoMicrolerny(user_id,microlerny,user_id_obj,lerny_active,user_state)
				else:
					data=listarLernys(user_id)
					data["fulfillmentMessages"].append({
						"text": {
							"text": [
								"Debes seleccionar un curso antes de continuar"
							]
						}
					})
		# CARGAR_CONTINUAR_LERNY
		elif(key == "CARGAR_CONTINUAR_LERNY"):

			print("CARGAR_CONTINUAR_LERNY")
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				lerny_pk = (int(request["lerny_num"]))
				user_id_obj = User.objects.get(
					identification=user_id)
				User_Lerny.objects.filter(active=True,user_id=user_id_obj).update(active=False)
				lerny_next = Lerny.objects.filter(pk=lerny_pk).first()
				User_Lerny.objects.filter(active=False,user_id=user_id_obj, lerny_id =lerny_next).update(active=True)

				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj,access=True).first()
				if(lerny_active):
					data=continueLerny(lerny_active.lerny_id,user_id_obj,user_id)
				else:
					data=listarLernys(user_id)
		# CARGAR_REQ_MICROLERNY\
		elif(key == "ACTIVIDAD_A_RECURSO"):

			print("ACTIVIDAD_A_RECURSO")
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				recurso_pk = (int(request["recurso_num"]))
				user_id_obj = User.objects.get(
					identification=user_id)

				objetive_resource = Resource.objects.filter(pk=recurso_pk).first()

				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
				user_state = User_State.objects.filter(user_id=user_id_obj,lerny_id=lerny_active.lerny_id).first()
				actual_resource_user = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
				datas=None
				objetive_resource_user = User_Resource.objects.filter(user_id=user_id_obj, resource_id=objetive_resource).first()
				
				if(objetive_resource_user):
					if(actual_resource_user):
						data = UserResourceSerializer(actual_resource_user).data
						data2 = UserResourceSerializer(objetive_resource_user).data
						User_Resource.objects.filter(user_id=user_id_obj, resource_id=objetive_resource).update(user_response=data['user_response']+' '+data2['user_response'])
						User_Resource.objects.get(user_id=user_id_obj, resource_id=actual_resource_user.resource_id).delete()
					else:
						previous_text="No hemos podido cargar tu actividad, intentalo de nuevo por favor"
						datas = {
							"fulfillmentMessages": [
								{
									"text": {
										"text": [
											previous_text
										]
									}
								},
							]
						}
						
				else:
					if(actual_resource_user):
						data = UserResourceSerializer(actual_resource_user).data
						print("RE CARGAR ARCHIVO")
						User_Resource.objects.filter(resource_id=actual_resource_user.resource_id).update(resource_id=objetive_resource)

					else:
						previous_text="No hemos podido cargar tu actividad, intentalo de nuevo por favor"
						datas = {
							"fulfillmentMessages": [
								{
									"text": {
										"text": [
											previous_text
										]
									}
								},
							]
						}
				if(datas):
					print("actividades re asignadas sin problema")
					data=datas
				else:
					previous_text="Tu archivo fue guardado en la actividad: "+str(objetive_resource.title)
					data = {
						"fulfillmentMessages": [
							{
								"text": {
									"text": [
										previous_text
									]
								}
							},
						]
					}

					data["fulfillmentMessages"].append({
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
												"title": "¿Deseas hacer algo más?",
												"image_url": "https://lerny.co/wp-content/uploads/2022/Menu_chatbot3.png",
												"subtitle": "Para continuar, por favor selecciona una opción.",
												"buttons":
												[
													{
														"type": "postback",
														"title": "Cargue su archivo",
														"payload": "CARGAR_ARCHIVO"
													},
													{
														"type": "postback",
														"title": "Continuar curso",
														"payload": "continuar_curso"
													},
													{
														"type": "postback",
														"title": "Ver módulos",
														"payload": "LIST_MICROLERNYS"
													},
												]
											}
										]
									}
								}
							}
						}})
		elif(key == "LernyDefaultFallback"):
			if(text):
				if(user_id is None):
					data=bienvenidaLerny(user_id)
				else:
					if(text[0:5] == "http:" or text[0:5] == "https"):
						
						user_id_obj = User.objects.get(
							identification=user_id)
						lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
						user_state = User_State.objects.filter(user_id=user_id_obj,lerny_id=lerny_active.lerny_id).first()
						u_resource = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
						response=text						
						
						if(u_resource):
							data = UserResourceSerializer(u_resource).data
							User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).update(user_response=data['user_response']+';'+response)
							u_resource = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
						else:
							print("GUARDAR ARCHIVO")
							u_resource = User_Resource()
							u_resource.resource_id = user_state.resource_id
							u_resource.user_id = user_state.user_id
							u_resource.user_response = response
							u_resource.done = True
							u_resource.response_date = datetime.now()
							u_resource.last_view_date = datetime.now()
							u_resource.save()
						data = cargarActividadFallback(user_id)
					else:
						data = {
							"fulfillmentMessages": [
								{
									"payload": {
										"facebook": {
											"attachment": {
												"type": "template",
												"payload": {
													"template_type": "button",
													"buttons": [
													{
														"type": "web_url",
														"title": "Enviar email",
														"url": "https://mail.google.com/mail/u/0/?fs=1&tf=cm&source=mailto&to=lernyjaveriana@gmail.com"
													},
													{
														"type": "postback",
														"payload": "hola lerny",
														"title": "Ver menú inicial"
													}
													],
													"text": "Hola, no hemos podido interpretar tu petición, si tienes una consulta importante, por favor escríbenos al correo: *lernyjaveriana@gmail.com*"
												}
											}
										}
									}
								}
							
							]
						}
			else:
				if(user_id is None):
					data=bienvenidaLerny(user_id)
				else:
					if(len(urlArg)>0):
						response = urlArg
						user_id_obj = User.objects.get(
							identification=user_id)
						lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
						user_state = User_State.objects.filter(user_id=user_id_obj,lerny_id=lerny_active.lerny_id).first()
						u_resource = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
						for url in urlArg:
							response=upload_to_s3(url)						
							if(u_resource):
								data = UserResourceSerializer(u_resource).data
								User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).update(user_response=data['user_response']+';'+response)
								u_resource = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
							else:
								print("GUARDAR ARCHIVO")
								u_resource = User_Resource()
								u_resource.resource_id = user_state.resource_id
								u_resource.user_id = user_state.user_id
								u_resource.user_response = response
								u_resource.done = True
								u_resource.response_date = datetime.now()
								u_resource.last_view_date = datetime.now()
								u_resource.save()
						data = cargarActividadFallback(user_id)
		# CARGAR_REQ_MICROLERNY
		elif(key == "PREGUNTA_GENERAL"):
			question = request['QUESTION']
			faq_id_obj = Faqs.objects.get(
				intent_name=question)
			data = FaqsSerializer(faq_id_obj).data
			response=data["response"]
			response_type=data["response_type"]
			if(response_type=="text"):
				data = {
					"fulfillmentMessages": [
						{
							"text": {
								"text": [
									response
								]
							}
						},
					]
				}
		# BIENVENIDO_LERNY
		elif(key == "BIENVENIDO_LERNY"):
			data=bienvenidaLerny(user_id)
		elif(key == "CARGAR_MULTIPLE"):
			print('CARGAR_MULTIPLE')
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:
				response = request["respuesta"]
				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
				user_state = User_State.objects.filter(user_id=user_id_obj,lerny_id=lerny_active.lerny_id).first()
				u_resource = User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).first()
				resource = Resource.objects.filter(id=user_state.resource_id.pk).first()
				u_quiz = User_quiz_logs.objects.filter(user_id=user_id_obj).first()
									
				points_wrong = resource.points_wrong_answer #puntos por respuesta incorrecta
				points_correct = resource.points_correct_answer #puntos por respuesta correcta
				response_correct = resource.response_answer_correct #respuesta correcta
				response_wrong = resource.response_wrong_answer #respuesta incorrecta
				points_user =User_quiz_logs.objects.filter(user_id=user_id_obj).count() #puntos acumulados del usuario
				points_true = points_correct + points_user #puntos acumulados respuesta correcta
				points_false = points_wrong + points_user #puntos acumulados respuesta incorrecta
				correct = 0

				retro = "Has seleccionado la respuesta" + str(response) + " y es incorrecta" + str(response_wrong) + " has obtenido: " + str(points_wrong) + " puntos 🎖️ en el quiz; tu suma total de puntos es "+ str(points_false)

				if(user_state.resource_id.first_button==response and resource.correct_answer_button==1):
					points_user = points_true
					retro = "Has seleccionado la respuesta" + str(response) + " y es correcta" + str(response_correct) + " has obtenido: " + str(points_correct) + " puntos 🎖️ en el quiz; tu suma total de puntos es "+ str(points_true) +" manifico 🤩"
					correct = 1
				if(user_state.resource_id.second_button==response and resource.correct_answer_button==2 ):
					points_user = points_true
					retro = "Has seleccionado la respuesta" + str(response) + " y es correcta" + str(response_correct) + " has obtenido: " + str(points_correct) + " puntos 🎖️ en el quiz; tu suma total de puntos es "+ str(points_true) +" manifico 🤩"
					correct = 1
				if(user_state.resource_id.third_button==response and resource.correct_answer_button==3):
					points_user = points_true
					retro = "Has seleccionado la respuesta" + str(response) + " y es correcta" + str(response_correct) + " has obtenido: " + str(points_correct) + " puntos 🎖️ en el quiz; tu suma total de puntos es "+ str(points_true) +" manifico 🤩"
					correct = 1

				if (resource.single_use):
					if (u_quiz):

						# Se realiza retro / tabnine()
						retro = "El quiz anterior, solo tiene habilitado un intento, tu respuesta no se puede guardar :/, continua aprendiendo con los siguientes recursos"
					else:
						quiz = User_quiz_logs()
						quiz.user_id = user_id_obj
						quiz.resource_id = resource
						quiz.points = points_user
						quiz.response = response
						if correct == 1:
							quiz.correct = True
						else:
							quiz.state_quiz = False
						#añadir recurso id
						quiz.save() #Guardamos la info del quiz
				else:
					if (u_quiz):
						User_quiz_logs.objects.filter( user_quiz_id=u_quiz.user_quiz_id).update(
							response=response,
							points = points_user,
						)
					else:
						quiz = User_quiz_logs()
						quiz.user_id = user_id_obj
						quiz.points = points_user
						quiz.response = response
						if correct == 1:
							quiz.correct = True
						else:
							quiz.state_quiz = False
						quiz.resource_id = resource.resource_id
						quiz.save() #Guardamos la info del quiz



				

				if(u_resource):
					data = UserResourceSerializer(u_resource).data
					User_Resource.objects.filter(user_id=user_id_obj, resource_id=user_state.resource_id).update(user_response=data['user_response']+'\n'+response)
				else:
					print("GUARDAR ARCHIVO")
					u_resource = User_Resource()
					u_resource.resource_id = user_state.resource_id
					u_resource.user_id = user_state.user_id
					u_resource.user_response = response
					u_resource.done = True
					u_resource.response_date = datetime.now()
					u_resource.last_view_date = datetime.now()
					u_resource.save()

				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
				data=continueLerny(lerny_active.lerny_id,user_id_obj,user_id)
				data_feedback =	{
					"text": {
						"text": [
							retro
						]
					}
				}

				print (data)
				data["fulfillmentMessages"].append(data_feedback)
		# NPS_METRIC1
		elif(key == "NPS_METRIC1"):			
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:

				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.get(active=True,user_id=user_id_obj)
				user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active.lerny_id)
				user_state = user_state.first()
				support_resource_microlerny_lerny = Support_Resource_Microlerny_Lerny.objects.filter(
				lerny_id=user_state.lerny_id, Microlerny_id = user_state.micro_lerny_id).order_by('pk')

				isText = SupportResourceSerializer(support_resource_microlerny_lerny.first().Support_Resource_id).data["Response_is_text"]
				score = Score()
				score.Support_Resource_Microlerny_Lerny = support_resource_microlerny_lerny.first()
				score.User = user_id_obj	
				if(isText):
					response=str(request["NPS1"])
					score.Response = response
					score.Response_Int = 0
				else:
					response=int(float(request["NPS1"]))
					score.Response = "N/A"
					score.Response_Int = response
				score.save()


				scores = Score.objects.filter(
				User=user_state.user_id ).order_by('pk')
				scores_count=scores.count()
				support_resource_microlerny_lerny_count=support_resource_microlerny_lerny.count()
				if(support_resource_microlerny_lerny and scores_count<support_resource_microlerny_lerny_count):
					try:
						support_resource_show = support_resource_microlerny_lerny[scores_count]
					except IndexError:
						support_resource_show = None
					support_resource=support_resource_show.Support_Resource_id
					dataDB = SupportResourceSerializer(support_resource).data["text"]
					
					data = {
							"followupEventInput": {
								"name": dataDB,
								"parameters": {
								},
								"languageCode":"en-US"
							}
						}
		# NPS_METRIC2
		elif(key == "NPS_METRIC2"):
						
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:

				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.get(active=True,user_id=user_id_obj)
				user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active.lerny_id)
				user_state = user_state.first()
				support_resource_microlerny_lerny = Support_Resource_Microlerny_Lerny.objects.filter(
				lerny_id=user_state.lerny_id, Microlerny_id = user_state.micro_lerny_id).order_by('pk')

				isText = SupportResourceSerializer(support_resource_microlerny_lerny[1].Support_Resource_id).data["Response_is_text"]
				score = Score()
				score.Support_Resource_Microlerny_Lerny = support_resource_microlerny_lerny[1]
				score.User = user_id_obj	
				if(isText):
					response=str(request["NPS2"])
					score.Response = response
					score.Response_Int = 0
				else:
					response=int(float(request["NPS2"]))
					score.Response = "N/A"
					score.Response_Int = response
				score.save()


				scores = Score.objects.filter(
				User=user_state.user_id ).order_by('pk')
				scores_count=scores.count()
				support_resource_microlerny_lerny_count=support_resource_microlerny_lerny.count()
				if(support_resource_microlerny_lerny and scores_count<support_resource_microlerny_lerny_count):
					try:
						support_resource_show = support_resource_microlerny_lerny[scores_count]
					except IndexError:
						support_resource_show = None
					support_resource=support_resource_show.Support_Resource_id
					dataDB = SupportResourceSerializer(support_resource).data["text"]
					
					data = {
							"followupEventInput": {
								"name": dataDB,
								"parameters": {
								},
								"languageCode":"en-US"
							}
					}
		# NPS_METRIC3
		elif(key == "NPS_METRIC3"):
			if(user_id is None):
				data=bienvenidaLerny(user_id)
			else:

				user_id_obj = User.objects.get(
					identification=user_id)
				lerny_active = User_Lerny.objects.get(active=True,user_id=user_id_obj)
				user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active.lerny_id)
				user_state = user_state.first()
				support_resource_microlerny_lerny = Support_Resource_Microlerny_Lerny.objects.filter(
				lerny_id=user_state.lerny_id, Microlerny_id = user_state.micro_lerny_id).order_by('pk')

				isText = SupportResourceSerializer(support_resource_show = support_resource_microlerny_lerny.first().Support_Resource_id).data["Response_is_text"]
				score = Score()
				score.Support_Resource_Microlerny_Lerny = support_resource_microlerny_lerny[1]
				score.User = user_id_obj	
				if(isText):
					response=str(request["NPS3"])
					score.Response = response
					score.Response_Int = 0
				else:
					response=int(float(request["NPS3"]))
					score.Response = "N/A"
					score.Response_Int = response
				score.save()
				data=continueLerny(lerny_active.lerny_id,user_id_obj,user_id)
		elif(key == "PQR"):
			if(user_id is None):

				data=bienvenidaLerny(user_id)
			else:
				user_id_obj = User.objects.get(identification=user_id)
				lerny_active = User_Lerny.objects.filter(active=True,user_id=user_id_obj,access=True).first()
				user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active.lerny_id).first()
				user_pqr = text
				print(user_pqr)
				data = pqr(user_id_obj,user_state,user_pqr)
		elif(key == "QUIZ_RESPONSE"):
			quiz_response = ""
		else:
			data = {}
		print(data)
		return Response(data, status=status.HTTP_201_CREATED)
		 
# class GetPayInformation(APIView):

#     def get(self, request, tipoDocumento, numeroDocumento, format=None):
# #        url = "http://replica.javerianacali.edu.co:8100/ServiciosSF/rs/consultarDeuda?tipoDocumento="+tipoDocumento+"&numeroDocumento="+numeroDocumento
# #        response = requests.get(url)
# #        information = response.json()

#         data = {}

#         information = {
#             "result":[
#                 {
#                     "nationalId":"1107073062",
#                     "commonId":"00008956081",
#                     "invoiceId":"PRE-EDU-00010176410000",
#                     "valorPagar":"970000",
#                     "valorPagado":"0",
#                     "accountTypeSF":"CEC"
#                 }
#             ]
#         }

#         try:
#             information["result"]
#             result = True
#         except:
#             result = False

#         if(result):
#             lerny = Lerny.objects.all().first()
#             user = User.objects.get(identification=numeroDocumento)
#             pay = False
#             for i in information["result"]:
#                 user_lerny = User_Lerny.objects.filter(lerny_id =lerny.id, user_id__identification=i["nationalId"])
#                 if(i["valorPagar"]==i["valorPagado"]):
#                     pay = True
#                 else:
#                     pay = False

#                 if(user_lerny):
#                     user_lerny = user_lerny.first()
#                     user_lerny.valor = i["valorPagado"]
#                     user_lerny.bill_state = pay
#                     user_lerny.reference = i["invoiceId"]
#                     user_lerny.pay_date = datetime.now()
#                     user_lerny.save()
#                     data = UserLernySerializer(user_lerny).data
                
#                 else:
#                     user_lerny = User_Lerny()
#                     user_lerny.lerny_id = lerny
#                     user_lerny.user_id = user
#                     user_lerny.valor = i["valorPagado"]
#                     user_lerny.bill_state = pay
#                     user_lerny.reference = i["invoiceId"]
#                     user_lerny.pay_date = datetime.now()
#                     user_lerny.lerny_points = 0
#                     user_lerny.opinion_points = 0
#                     user_lerny.save()
#                     data = UserLernySerializer(user_lerny).data
#         else:
#             information={
#                 "codError": "CE_CONSULTA_DEUDA",
#                 "exceptionMessage": "Error consultando las deudas de la persona"
#             }
#             data = information

#         return Response(data)
