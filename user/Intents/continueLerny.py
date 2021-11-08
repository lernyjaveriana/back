from rest_framework.decorators import action
from ..models import User
from lerny.models import *
from lerny.serializers import *
from user.Intents.bucketHelper import upload_to_s3
from user.Intents.cargarActividadFallbackIntent import cargarActividadFallbackIntent
from datetime import datetime

def mediaResponseFormat(resourse):
	medias = Media.objects.filter(resource_id=resourse).order_by('position')
	template=[]
	for file in medias:
		content = MediaSerializer(file).data
		template.append({
			"payload": {
				"facebook": {
					"attachment": {
						"type": content["content_type"],
						"payload": {
							"url":content["content_url"]
						}
					}
				}
			}
		})
	return template


def saveStateLogs(lerny_id,micro_lerny,user_id_obj,resourse):
	logsUserResource =  User_State_Logs.objects.filter(micro_lerny_id=micro_lerny,resource_id=resourse, lerny_id=lerny_id,user_id=user_id_obj)
	if(logsUserResource.count() ==0):	
		user_state_logs = User_State_Logs()
		user_state_logs.lerny_id = lerny_id
		user_state_logs.micro_lerny_id = micro_lerny
		user_state_logs.user_id = user_id_obj
		user_state_logs.resource_id = resourse
		user_state_logs.save()

def saveState(lerny_id,micro_lerny,user_id_obj,resourse):

	saveStateLogs(lerny_id, micro_lerny, user_id_obj, resourse)

	user_state = User_State()
	user_state.lerny_id = lerny_id
	user_state.micro_lerny_id = micro_lerny
	user_state.user_id = user_id_obj
	user_state.resource_id = resourse
	user_state.save()


def continueLerny(lerny_active,user_id_obj,user_id):
	user_state = User_State.objects.filter(user_id=user_id_obj, lerny_id =lerny_active)
	is_last = False
	#The user is found in the db
	if(user_state):
		user_state = user_state.first()
		phase = user_state.resource_id.phase
		resourses = Resource.objects.filter(
				microlerny=user_state.micro_lerny_id)

		#verifies if the user is still consumming the resources of the actual microlerny
		if(resourses.count() > int(phase)):
			resourse = Resource.objects.filter(
				microlerny=user_state.micro_lerny_id, phase=str(int(phase)+1)).first()
			user_state.resource_id = resourse

			saveStateLogs(user_state.lerny_id, user_state.micro_lerny_id, user_state.user_id, user_state.resource_id)
			user_state.save()
			dataDB = ResourceSerializer(resourse).data
		#verifies if the user completed all the microlerny's resources, then, should search the next microlerny
		elif(resourses.count() == int(phase)):
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
					microlerny=micro_lerny_son_obj, phase='1')

				user_state.resource_id = resourse
				user_state.micro_lerny_id = microlerny_son

				saveStateLogs(user_state.lerny_id, user_state.micro_lerny_id, user_state.user_id, user_state.resource_id)
				user_state.save()
				dataDB = ResourceSerializer(resourse).data
			else:
				#variable que indica que es o no el ultimo microlerny del curso
				is_last = True
		else:
			data = None
	else:
		
		lerny_id = lerny_active

		micro_lerny = MicroLerny.objects.filter(lerny=lerny_id).order_by('pk').first()
		resourse = Resource.objects.get(
			microlerny=micro_lerny.id, phase='1')

		user_id_obj = User.objects.get(
			identification=user_id)

		saveState(lerny_id,micro_lerny,user_id_obj,resourse)

		dataDB = ResourceSerializer(resourse).data
	if(is_last):

		user_id_obj = User.objects.get(identification=user_id)
		user_lernys = User_Lerny.objects.filter(user_id=user_id_obj)

		lernys_ids = user_lernys.values_list('lerny_id', flat=True)
		lernys = Lerny.objects.filter(
			pk__in=lernys_ids)

		data = LernySerializer(lernys, many=True).data
		i = 0
		temp = []
		previous_text = "Has terminado los microlernys asociados al lerny!"
		while(i < len(data)):
			print("IMPRESION LISTAR LERNY: "+ str(data[i]['id'])+") " + data[i]['lerny_name'])
			temp.append(
				{
					"subtitle": data[i]['description'],
					"image_url": data[i]['url_image'],
					"title": data[i]['lerny_name'],
					"buttons": [
					{
						"payload": "cargar lerny "+str(data[i]['id']),
						"title": "Continuar Lerny",
						"type": "postback"
					}
					]
				},)
			i += 1

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

	elif(dataDB["resource_type"] == "consumable" and not is_last):
		templates=mediaResponseFormat(resourse)
		previous_text = dataDB["previous_text"]
		if(previous_text==None or previous_text==''):
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
			]
		}
		for x in templates:
			data["fulfillmentMessages"].append(x)
		data["fulfillmentMessages"].append({
			"payload": {
				"facebook": {
					"attachment": {
						"type": "template",
						"payload": {
							"template_type": "generic",
							"elements": [
								{
									"title": dataDB["title"],
									"image_url": dataDB["image_url"],
									"subtitle": dataDB["description"],
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
		})

	elif(dataDB["resource_type"] == "practical" and not is_last):
		templates=mediaResponseFormat(resourse)
		previous_text = dataDB["previous_text"]
		if(previous_text==None or previous_text==''):
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
			]
		}
		for x in templates:
			data["fulfillmentMessages"].append(x)
		
		data["fulfillmentMessages"].append({
			"payload": {
				"facebook": {
					"attachment": {
						"type": "template",
						"payload": {
							"template_type": "generic",
							"elements": [
								{
									"title": dataDB["title"],
									"image_url": dataDB["image_url"],
									"subtitle": dataDB["description"],
									"buttons": [
										{
											"type": "postback",
											"title": "Siguiente recurso",
											"payload": "CONTINUAR_CURSO"
										},
										{
											"payload": "CARGAR_ARCHIVO" ,
											"title": "Cargar actividad",
											"type": "postback"
										}
										
									]
								}
							]
						}
					}
				}
			}
		})

	elif(dataDB["resource_type"] == "multiple" and not is_last):
		print("Data, description: "+dataDB["description"])
		temp=[]
		previous_text = dataDB["previous_text"]
		if(previous_text==''):
			previous_text="Responde la siguiente pregunta por favor"

		if(dataDB["first_button"]):
			temp.append(
				{
					"type": "postback",
					"title": dataDB["first_button"],
					"payload": "CARGAR_MULTIPLE "+dataDB["first_button"]
				},
			)
		
		if(dataDB["second_button"]):
			temp.append(
				{
					"type": "postback",
					"title": dataDB["second_button"],
					"payload": "CARGAR_MULTIPLE "+ dataDB["second_button"]
				},
			)
		
		if(dataDB["third_button"]):
			temp.append(
				{
					"type": "postback",
					"title": dataDB["third_button"],
					"payload": "CARGAR_MULTIPLE "+dataDB["third_button"]
				}
			)
		
		
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
											"title": dataDB["title"],
											"image_url": dataDB["image_url"],
											"subtitle": dataDB["description"],
											"buttons": temp	
										}
									]
								}
							}
						}
					}
				}
			]
		}
	return data
