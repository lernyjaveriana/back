from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import UserSerializer
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
