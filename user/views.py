from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import serializers
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from lerny.models import *
from lerny.serializers import LernySerializer, MicroLernySerializer


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
        print("Parameters")
        print(request.data['queryResult']['parameters'])
        print("OutputContexts")
        print(request.data['queryResult']['outputContexts']["parameters"])
        request = request.data['queryResult']['parameters']
        key = request['LERNY_INTENT']
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
        elif(key == "LIST_MICROLERNYS"):
            #lerny = request['LERNY_INTENT']
            serializers_class = MicroLernySerializer
            micro_lerny = MicroLerny.objects.all()
            data = MicroLernySerializer(micro_lerny, many=True).data
            i = 0
            temp = []
            # print(json.dumps(data))
            while(i < len(data)):
                temp.append({
                        "text": {
                            "text": [
                                str(data[i]['id'])+") "+data[i]['micro_lerny_title']
                            ]}},)

                i += 1

            data = {
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": [
                                "Lista de Microlernys"
                            ]
                        }
                    },
                ]
            }
            j=0
            while(j<len(temp)):
                data["fulfillmentMessages"].append(temp[j])
                j+=1
            
            data["fulfillmentMessages"].append(
                {
                    "payload": {
                        "facebook": {
                            "attachment": {
                                "type": "template",
                                "payload": {
                                    "template_type": "button",
                                    "text": "¿Deseas seleccionar un micro lerny?",
                                    "buttons": [
                                        {
                                            "type": "postback",
                                            "title": "Si",
                                            "payload": "CONTINUAR_SELECCION"
                                        },
                                        {
                                            "type": "postback",
                                            "title": "No",
                                            "payload": "lerny_farewell"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            )

        else:
            data = {}

        return Response(data, status=status.HTTP_201_CREATED)
