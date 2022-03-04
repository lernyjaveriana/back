from lerny.models import *
from lerny.serializers import *
from user.Intents.continueLerny import mediaResponseUrlList

def bienvenidaLernyTemplate (interface,user_name=None):
    if interface == "fbMessenger":
        if user_name !=None:
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
                                                        "title": "Hola " + user_name + ", un gusto volver a verte!",
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

def cargarActividadFallbackTemplate (interface,micro_lernys,previous_text="A cual recurso deseas asociar el entregable que acabas de subir?"):
    temp = []
    if interface == "fbMessenger":
        for micro_lerny in micro_lernys:
            resources_microlerny = Resource.objects.filter(microlerny=micro_lerny,resource_type="practical")
            data = ResourceSerializer(resources_microlerny, many=True).data
            i = 0

            while(i < len(data)):
                print("IMPRESION LISTAR RECURSOS PRACTICOS: "+ str(data[i]['id'])+") " + data[i]['title'])
                temp.append(
                    {
                        "subtitle": data[i]['description'],
                        "image_url": data[i]['image_url'],
                        "title": data[i]['title'],
                        "buttons": [
                        {
                            "payload": "cargar actividad "+str(data[i]['id']),
                            "title": "Seleccionar",
                            "type": "postback"
                        }
                        ]
                    })
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
    return data 

def cargarRecursoMicrolernyTemplate (interface,dataDB,templates,resourse):

    if interface == "fbMessenger":
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
                {
                    "text": {
                        "text": [
                            "si tiene problemas cargando el contenido del recurso, puede visualizarlo en el siguien enlace: ",
                        ]

                    }
                },
            ]
        }
        for x in mediaResponseUrlList(resourse):
            data["fulfillmentMessages"].append(
                {
                    "text": {
                        "text": [
                            x,
                        ]

                    }
                },
            )
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
    return data

def listarLernysTemplate (interface,info):
    if interface == "fbMessenger":
        i = 0
        temp = []
        while(i < len(info)):
            print("IMPRESION LISTAR LERNY: "+ str(info[i]['id'])+") " + info[i]['lerny_name'])
            temp.append(
                {
                    "subtitle": info[i]['description'],
                    "image_url": info[i]['url_image'],
                    "title": info[i]['lerny_name'],
                    "buttons": [
                    {
                        "payload": "cargar lerny "+str(info[i]['id']),
                        "title": "Continuar Lerny",
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
    return data

def listarMicrolernysTemplate (interface,info):
    if interface == "fbMessenger":
        i = 0
        temp = []
        while(i < len(info)):
            print("IMPRESION LISTAR LERNY: "+ str(info[i]['id'])+") " + info[i]['micro_lerny_title'])
            temp.append(
                {
                    "subtitle": info[i]['micro_lerny_subtitle'],
                    "image_url": info[i]['microlerny_image_url'],
                    "title": info[i]['micro_lerny_title'],
                    "buttons": [
                    {
                        "payload": "cargar recurso "+str(info[i]['id']) ,
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
    return data

def pqrTemplate (interface):

    if interface == "fbMessenger":
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
                                            "title": "Tu inquietud ha sido guardada",
                                            "image_url": "https://lerny.co/wp-content/uploads/2020/12/marca_lerny.jpg",
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
    return data