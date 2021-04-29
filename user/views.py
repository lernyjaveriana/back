from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import serializers
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import action
from .models import User
from lerny.models import *
from lerny.serializers import *
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


class ApiManager(APIView):

	def post(self, request):
		media = "video"
		print("request.data")
		print(request)	
		print("request.data.intent.displayname")
		print(request.data['queryResult'])	
		print("Parameters")
		print(request.data['queryResult']['parameters'])
		print("OutputContexts")
		print(request.data['queryResult']['outputContexts'])
		x = 0
		# Identifico el user_document_id independientemente de donde se encuentre en el json
		OutputContexts = ''
		while((x < len(request.data['queryResult']['outputContexts']))):
			user_id = (request.data['queryResult']['outputContexts'][x].get(
				'parameters').get('user_document_id'))
			if((request.data['queryResult']['outputContexts'][x].get('parameters').get('user_document_id')) != None):
				break
			x += 1
		if(not(user_id is None)):
			user_id = (str(int(float(user_id))))
			print("USER_ID "+user_id)
		
		if(request.data['queryResult']['intent']['displayName']=="LernyDefaultFallback"):
			key = "LernyDefaultFallback"
		else:
			request = request.data['queryResult']['parameters']
			key = request['LERNY_INTENT']
		# LOGIN
		if (key == "LOGIN_USER"):
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
														"title": "Hola " + UserSerializer(user).data["user_name"] + ", un gusto volver a verte!",
														"image_url": "https://lerny.co/wp-content/uploads/2020/12/titulo_curso.jpg",
														"subtitle": "Para comenzar por favor selecciona una opción.",
														"buttons":
														[
															{
																"type": "postback",
																"title": "Continuar Lerny",
																"payload": "CONTINUAR_CURSO"
															},
															{
																"type": "postback",
																"title": "ver Micro Lernys",
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
		# LOGIN

		# LISTAR MICROLERNYS
		elif(key == "LIST_MICROLERNYS"):
			# lerny = request['LERNY_INTENT']
			serializers_class = MicroLernySerializer
			micro_lerny = MicroLerny.objects.all()
			data = MicroLernySerializer(micro_lerny, many=True).data
			i = 0
			temp = []
			while(i < len(data)):
				print("IMPRESION LISTAR LERNY: "+ str(data[i]['id'])+") " + data[i]['micro_lerny_title'])
				temp.append(
					{
						"subtitle": data[i]['micro_lerny_subtitle'],
						"image_url": data[i]['microlerny_image_url'],
						"title": data[i]['micro_lerny_title'],
						"buttons": [
						{
							"payload": "cargar recurso "+str(data[i]['id'])+") " ,
							"title": "Seleccionar",
							"type": "postback"
						}
						]
					},)
				i += 1

			data = {
				"fulfillmentMessages": [
				{
					"payload": {
						"facebook": {
							"attachment": {
								"type": "template",
								"payload": {
									"template_type": "generic",
									"elements": temp
								}
							}
						}
					}
				}]
			}
		# CONTINUAR CURSO
		elif(key == "CONTINUAR_CURSO"):
			is_last = False
			serializers_class = ResourceSerializer
			user_id_obj = User.objects.get(
				identification=user_id)
			user_state = User_State.objects.filter(user_id=user_id_obj)

			if(user_state):
				user_state = user_state.first()
				phase = user_state.resource_id.phase
				if(phase == 'pre'):
					resourse = Resource.objects.get(
						microlerny=user_state.micro_lerny_id, phase='dur')
					user_state.resource_id = resourse
					user_state.save()
					data = ResourceSerializer(resourse).data
					
				elif(phase == 'dur'):
					resourse = Resource.objects.filter(
						microlerny=user_state.micro_lerny_id, phase='pt2')
					if(resourse):
						print("recurso pt2 ")
					else:
						print("recurso pos ")
						resourse = Resource.objects.filter(
							microlerny=user_state.micro_lerny_id, phase='pos')
					
					user_state.resource_id = resourse.first()
					user_state.save()
					data = ResourceSerializer(resourse.first()).data

				elif(phase == 'pt2'):
					resourse = Resource.objects.filter(
						microlerny=user_state.micro_lerny_id, phase='pos')
					user_state.resource_id = resourse.first()
					user_state.save()
					data = ResourceSerializer(resourse.first()).data

				elif(phase == 'pos'):
					micro_lerny_id_obj = MicroLerny.objects.get(
						id=user_state.micro_lerny_id.id)
					son = TreeMicroLerny.objects.filter(
						dady_micro_lerny=micro_lerny_id_obj)

					if(son.count() > 0):
						s = son.values_list('son_micro_lerny_id', flat=True)

						microlerny_son = MicroLerny.objects.filter(
							pk__in=s).first()

						micro_lerny_son_obj = MicroLerny.objects.get(
							id=microlerny_son.id)

						resourse = Resource.objects.get(
							microlerny=micro_lerny_son_obj, phase='pre')

						user_state.resource_id = resourse
						user_state.micro_lerny_id = microlerny_son
						user_state.save()
						data = ResourceSerializer(resourse).data
					else:
						#variable que indica que es o no el ultimo microlerny dle curso
						is_last = True
				else:
					data = None
			else:
				lerny_id = Lerny.objects.all().first()

				micro_lerny = MicroLerny.objects.all().order_by('pk').first()
				resourse = Resource.objects.get(
					microlerny=micro_lerny.id, phase='pre')

				user_id_obj = User.objects.get(
					identification=user_id)

				user_state = User_State()
				user_state.lerny_id = lerny_id
				user_state.micro_lerny_id = micro_lerny
				user_state.user_id = user_id_obj
				user_state.resource_id = resourse
				user_state.save()
				data = ResourceSerializer(resourse).data
			if(is_last):

				data = {
					"fulfillmentMessages": [
						{
							"payload": {
								"facebook": {
									"attachment": {
										"type": "template",
										"payload": {
											"template_type": "generic",
											"elements": [
												{
													"title": "Has terminado los microlernys asociados al lerny!",
													"image_url": "https://lerny.co/wp-content/uploads/2020/12/ruta_curso1.jpg",
													"subtitle": "selecciona una opcion para continuar",
													"buttons": [
														{
															"type": "postback",
															"title": "Listar Microlernys",
															"payload": "LIST_MICROLERNYS"
														},
														{
															"type": "postback",
															"title": "Salir",
															"payload": "lerny_farewell"
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
			elif(data["phase"] != "pos" and not is_last):
				# print("Data, description: "+data["description"])
				if(data["description"]=="Infografía"):
					media = "image"
				elif(data["description"]=="Práctica"):
					media = "file"
				previous_text = data["previous_text"]
				if(previous_text==None):
					previous_text="Estamos cargando tu contenido, esto puede tardar un par de minutos, por favor espera. :)"
				data = {
					"fulfillmentMessages": [
						{
							"text": {
								"text": [
									previous_text
								]
							}
						},
						{
							"payload": {
								"facebook": {
									"attachment": {
										"type": media,
										"payload": {
											"url":data["content_url"]
										}
									}
								}
							}
						},
						{
							"payload": {
								"facebook": {
									"attachment": {
										"type": "template",
										"payload": {
											"template_type": "generic",
											"elements": [
												{
													"title": data["title"],
													"image_url": data["image_url"],
													"subtitle": data["description"],
													"buttons": [
														{
															"type": "postback",
															"title": "Siguiente recurso",
															"payload": "CONTINUAR_CURSO"
														},
														{
															"type": "postback",
															"title": "Salir",
															"payload": "lerny_farewell"
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

			elif(data["phase"] == "pos" and not is_last):
				print("Data, description: "+data["description"])
				if(data["description"]=="Infografía"):
					media = "image"
				elif(data["description"]=="Práctica"):
					media = "file"
				previous_text = data["previous_text"]
				if(previous_text==None):
					previous_text="Estamos cargando tu contenido, esto puede tardar un par de minutos, por favor espera. :)"
				data = {
					"fulfillmentMessages": [
						{
							"text": {
								"text": [
									previous_text
								]
							}
						},
						{
							"payload": {
								"facebook": {
									"attachment": {
										"type": media,
										"payload": {
											"url":data["content_url"]
										}
									}
								}
							}
						},
						{
							"payload": {
								"facebook": {
									"attachment": {
										"type": "template",
										"payload": {
											"template_type": "generic",
											"elements": [
												{
													"title": data["title"],
													"image_url": data["image_url"],
													"subtitle": data["description"],
													"buttons": [
														{
															"type": "postback",
															"title": "Siguiente recurso",
															"payload": "CONTINUAR_CURSO"
														},
														{
															"type": "postback",
															"title": "Cargar url de la actividad",
															"payload": "CARGAR_ARCHIVO"
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

		# CARGAR ARCHIVO
		elif(key == "CARGAR_ARCHIVO"):
			file_url = request["file_url"]
			url_task = file_url
			user_id_obj = User.objects.get(
				identification=user_id)
			user_state = User_State.objects.filter(user_id=user_id_obj)
			serializers_class = UserResourceSerializer
			if(user_state):
				print("GUARDAR ARCHIVO")
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
			data = {
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
												"title": "Tu archivo ha sido cargado exitosamente! Deseas hacer algo más?",
												"image_url": "https://lerny.co/wp-content/uploads/2020/12/ruta_curso1.jpg",
												"subtitle": "Para continuar, por favor selecciona una opción.",
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
		# CARGAR_REQ_MICROLERNY
		elif(key == "CARGAR_REQ_MICROLERNY"):
			microlerny = (int(request["microlerny_num"]))
			serializers_class = ResourceSerializer
			user_id_obj = User.objects.get(
				identification=user_id)
			user_state = User_State.objects.filter(user_id=user_id_obj)
			if(user_state):
				user_state = user_state.first()
				lerny_id = Lerny.objects.all().first()
				micro_lerny = MicroLerny.objects.all().order_by('pk')[microlerny-1]
				resourse = Resource.objects.get(
					microlerny=micro_lerny.id, phase='pre')

				user_state.resource_id = resourse
				user_state.micro_lerny_id = micro_lerny
				user_state.save()
				data = ResourceSerializer(resourse).data

			else:
				lerny_id = Lerny.objects.all().first()
				micro_lerny = MicroLerny.objects.all().order_by('pk')[microlerny-1]
				resourse = Resource.objects.get(
					microlerny=micro_lerny.id, phase='pre')

				user_state = User_State()
				user_state.lerny_id = lerny_id
				user_state.micro_lerny_id = micro_lerny
				user_state.user_id = user_id_obj
				user_state.resource_id = resourse
				user_state.save()
				data = ResourceSerializer(resourse).data
			print("Data, description: "+data["description"])
			if(data["description"]=="Infografía"):
				media = "image"
			elif(data["description"]=="Práctica"):
				media = "file"
			previous_text = data["previous_text"]
			if(previous_text==None):
				previous_text="Estamos cargando tu contenido, esto puede tardar un par de minutos, por favor espera. :)"
			data = {
				"fulfillmentMessages": [
					{
						"text": {
							"text": [
								previous_text
							]
						}
					},
					{
						"payload": {
							"facebook": {
								"attachment": {
									"type": media,
									"payload": {
										"url":data["content_url"]
									}
								}
							}
						}
					},
					{
						"payload": {
							"facebook": {
								"attachment": {
									"type": "template",
									"payload": {
										"template_type": "generic",
										"elements": [
											{
												"title": data["title"],
												"image_url": data["image_url"],
												"subtitle": data["description"],
												"buttons": [
													{
														"type": "postback",
														"title": "Siguiente recurso",
														"payload": "CONTINUAR_CURSO"
													},
													{
														"type": "postback",
														"title": "Salir",
														"payload": "lerny_farewell"
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
		elif(key == "LernyDefaultFallback"):
			text = request.data['queryResult'].get('queryText')
			if(text):
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
												"payload": "menu_inicial",
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
				data = {}

		else:
			data = {}
		print(data)
		return Response(data, status=status.HTTP_201_CREATED)
		
class GetPayInformation(APIView):

    def get(self, request, tipoDocumento, numeroDocumento, format=None):
#        url = "http://replica.javerianacali.edu.co:8100/ServiciosSF/rs/consultarDeuda?tipoDocumento="+tipoDocumento+"&numeroDocumento="+numeroDocumento
#        response = requests.get(url)
#        information = response.json()
        serializers_class = UserLernySerializer
        data = {}

        information = {
            "result":[
                {
                    "nationalId":"1107073062",
                    "commonId":"00008956081",
                    "invoiceId":"PRE-EDU-00010176410000",
                    "valorPagar":"970000",
                    "valorPagado":"0",
                    "accountTypeSF":"CEC"
                }
            ]
        }

        try:
            information["result"]
            result = True
        except:
            result = False

        if(result):
            lerny = Lerny.objects.all().first()
            user = User.objects.get(identification=numeroDocumento)
            pay = False
            for i in information["result"]:
                user_lerny = User_Lerny.objects.filter(lerny_id =lerny.id, user_id__identification=i["nationalId"])
                if(i["valorPagar"]==i["valorPagado"]):
                    pay = True
                else:
                    pay = False

                if(user_lerny):
                    user_lerny = user_lerny.first()
                    user_lerny.valor = i["valorPagado"]
                    user_lerny.bill_state = pay
                    user_lerny.reference = i["invoiceId"]
                    user_lerny.pay_date = datetime.now()
                    user_lerny.save()
                    data = UserLernySerializer(user_lerny).data
                
                else:
                    user_lerny = User_Lerny()
                    user_lerny.lerny_id = lerny
                    user_lerny.user_id = user
                    user_lerny.valor = i["valorPagado"]
                    user_lerny.bill_state = pay
                    user_lerny.reference = i["invoiceId"]
                    user_lerny.pay_date = datetime.now()
                    user_lerny.lerny_points = 0
                    user_lerny.opinion_points = 0
                    user_lerny.save()
                    data = UserLernySerializer(user_lerny).data
        else:
            information={
                "codError": "CE_CONSULTA_DEUDA",
                "exceptionMessage": "Error consultando las deudas de la persona"
            }
            data = information

        return Response(data)
