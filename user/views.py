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


#class UserViewLogin(viewsets.GenericViewSet):

#    queryset = User.objects.filter(active_user=True)
#    serializer_class = UserSerializer

    # Detail define si es una petición de detalle o no, en methods añadimos el método permitido, en nuestro caso solo vamos a permitir post
#    @action(detail=False, methods=['post'])
#    def login(self, request):
#        """User sign in."""

#        serializer = UserLoginSerializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        user, token = serializer.save()
#        data = {
#            'user': UserSerializer(user).data,
#            'access_token': token
#        }
#        return Response(data, status=status.HTTP_201_CREATED)


class loginUser(APIView):

	def post(self, request):
		data= request.data['queryResult']['parameters']
		#data= request.data
		print(data)
		serializer = UserLoginSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		user, token = serializer.save()
		data = {
			'user': UserSerializer(user).data,
			'access_token': token
			}
		return Response(data, status=status.HTTP_201_CREATED)

