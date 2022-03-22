from lerny.models import *
from lerny.serializers import *
from datetime import datetime
from .TemplateUtilities.interfaceTemplates import *

# After upload activities trggered into fallback intent, it should shows you a menu
def cargarActividadFallbackIntent(user_id):

	user_id_obj = User.objects.get(identification=user_id)
	user_lerny = User_Lerny.objects.filter(active=True,user_id=user_id_obj).first()
	lerny_active=user_lerny.lerny_id
	micro_lernys = MicroLerny.objects.filter(lerny=lerny_active).order_by('pk')
	return cargarActividadFallbackTemplate("fbMessenger",micro_lernys)