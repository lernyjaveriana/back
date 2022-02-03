
from ..serializers import UserSerializer
from rest_framework.decorators import action
from ..models import User
from lerny.models import *
from lerny.serializers import *




def bienvenidaLerny(user_id):
	if(user_id):
		user = User.objects.get(
		identification=user_id)
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
													"image_url": "https://lerny.co/wp-content/uploads/2020/12/marca_lerny.jpg",
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
														{
															"type": "postback",
															"title": "Listar Lernys",
															"payload": "LISTAR_LERNYS"
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
	else:
		data = {
			"fulfillmentMessages": [
				{
					"text": {
						"text": [
							"Hola!, te damos la bienvenida a Lerny, una plataforma de educación en facebook messenger, pensada para quienes construimos futuro trabajando."
						]
					}
				},
				{
					"payload":{
						"facebook": 
						{
							"attachment": 
							{
							"type": "template",
							"payload": {
								"template_type": "generic",
								"elements": [
								{
									"image_url": "https://lerny.co/wp-content/uploads/2020/12/marca_lerny.jpg",
									"buttons": [
									{
										"title": "Comprar curso",
										"payload": "comprar_curso",
										"type": "postback"
									},
									{
										"payload": "iniciar_sesion",
										"title": "Iniciar sesión",
										"type": "postback"
									},
									{
										"payload": "info_contacto",
										"title": "Más información",
										"type": "postback"
									}
									],
									"title": "Menú Principal",
									"subtitle": "Para comenzar por favor selecciona una opción."
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

