from ..models import User
from lerny.models import *
from lerny.serializers import *


def listarMicrolernys(micro_lerny):

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
                    "payload": "cargar recurso "+str(data[i]['id']) ,
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