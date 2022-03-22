
from ..serializers import UserSerializer
from rest_framework.decorators import action
from ..models import User
from lerny.models import *
from lerny.serializers import *
from user.Intents.TemplateUtilities.interfaceTemplates import *

def bienvenidaLerny(user_id,interface="fbMessenger"):
	if(user_id):
		user = User.objects.get(
		identification=user_id)
		user_name = UserSerializer(user).data["user_name"]
		data = bienvenidaLernyTemplate(interface,user_name)
	else:
		data = bienvenidaLernyTemplate("fbMessenger")
	return data

