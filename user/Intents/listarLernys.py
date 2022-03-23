from ..models import User
from lerny.models import *
from lerny.serializers import *
from .TemplateUtilities.interfaceTemplates import *


def listarLernys(user_id):
    user_id_obj = User.objects.get(identification=user_id)
    user_lernys = User_Lerny.objects.filter(user_id=user_id_obj,access=True)

    lernys_ids = user_lernys.values_list('lerny_id', flat=True)
    lernys = Lerny.objects.filter(
        pk__in=lernys_ids)

    data = LernySerializer(lernys, many=True).data
    data = listarLernysTemplate("fbMessenger",data)
    return data