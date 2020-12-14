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
    user_document_id = serializers.CharField(min_length=4, max_length=64)
    #user_document_id.original = serializers.CharField(min_length=8, max_length=64)
    

    # Primero validamos los datos
    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        #user = authenticate(username=int(float(data['user_document_id'])), password=int(float(data['user_document_id'])))
        user = authenticate(username=data['user_document_id'], password=data['user_document_id'])
        if not user:
            try:
                user = User.objects.get(identification=data['user_document_id'])
                if user.identification == user.password:
                    self.context['user'] = user
                else:
                    print("prueba con el dato identificacion: "+data['user_document_id'])
                    raise serializers.ValidationError('Las credenciales no son válidas')
            except:
                print("prueba con el dato identificacion: "+data['user_document_id'])
                raise serializers.ValidationError('El usuario no existe')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key