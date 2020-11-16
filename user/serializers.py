#from rest_framework import serializers
#from .models import *

#class UserSerializer(serializers.ModelSerializer):
#	class Meta:
#		model = User
#		fields = '__all__'
#------------------------------------------------------


# Django
from django.contrib.auth import password_validation, authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from .models import *


#class UserModelSerializer(serializers.ModelSerializer):

#    class Meta:

#        model = User
#        fields = (
#            'username',
#            'first_name',
#            'last_name',
#            'email',
#        )


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'



class UserLoginSerializer(serializers.Serializer):

    # Campos que vamos a requerir
    identification = serializers.CharField(min_length=6, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['identification'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key