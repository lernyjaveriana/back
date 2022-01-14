from ..models import User
from lerny.models import *
from lerny.serializers import *
from user.Intents.continueLerny import mediaResponseFormat,saveStateLogs,saveState,mediaResponseUrlList


def cargarRecursoMicrolerny(user_id,microlerny,user_id_obj,lerny_active,user_state):

    #the following code creates from scratch the user state, that means the user has never seen this lerny before
    if(user_state):
        user_state = user_state.first()
        lerny_id = user_state.lerny_id
        micro_lerny = MicroLerny.objects.filter(lerny=lerny_id,id=microlerny).first()
        resourse = Resource.objects.get(
            microlerny=micro_lerny, phase='1')

        user_state.resource_id = resourse
        user_state.micro_lerny_id = micro_lerny
        saveStateLogs(user_state.lerny_id, user_state.micro_lerny_id, user_state.user_id, user_state.resource_id)
        user_state.save()
        dataDB = ResourceSerializer(resourse).data
    
    else:
        lerny_id = lerny_active.lerny_id
        micro_lerny = MicroLerny.objects.filter(lerny=lerny_id,pk=microlerny).first()
        resourse = Resource.objects.get(
            microlerny=micro_lerny, phase='1')


        saveState(lerny_id,micro_lerny,user_id_obj,resourse)

        dataDB = ResourceSerializer(resourse).data
    print("Data, description: "+dataDB["description"])
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
