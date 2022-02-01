from ..models import User
from lerny.models import *
from lerny.serializers import *


def pqr(user_id_obj, user_state, user_pqr):
    print("GUARDAR PQR")
    new_pqr = PQR()
    new_pqr.user_id = user_id_obj
    new_pqr.user_state = user_state
    new_pqr.pqr = user_pqr
    new_pqr.save()
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
                                        "title": "Tu pregunta/inquietud ha sido guardada, deseas hacer algo más?",
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
