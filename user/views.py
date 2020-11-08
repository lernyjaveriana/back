from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import serializers
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User



class UserManageGet(APIView):

	serializers_class = UserSerializer

	def get(self, request, user_id, format=None):
		user = User.objects.filter(id = user_id)
		data = UserSerializer(user, many=True).data
		return Response ({'user': data})


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


class loginUser(APIView):

	def post(self, request):
		request= request.data['queryResult']['parameters']
		serializer = UserLoginSerializer(data=request)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()

		data = {
			"followupEventInput": {
				"name": "Login",
				"languageCode": "en-US",
				"parameters": {
					"user": UserSerializer(user).data,
					"access_token": token
					}
				}
			}		

		return Response(data, status=status.HTTP_201_CREATED)

