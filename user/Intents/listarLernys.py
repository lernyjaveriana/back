from .serializers import UserSerializer, UserLoginSerializer
from .models import User
from lerny.models import *
from lerny.serializers import *


def listarLernys(user_id):
    user_id_obj = User.objects.get(identification=user_id)
    user_lernys = User_Lerny.objects.filter(user_id=user_id_obj,access=True)

    lernys_ids = user_lernys.values_list('lerny_id', flat=True)
    lernys = Lerny.objects.filter(
        pk__in=lernys_ids)

    data = LernySerializer(lernys, many=True).data
    i = 0
    temp = []
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