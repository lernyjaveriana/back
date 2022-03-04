from ..models import User
from lerny.models import *
from lerny.serializers import *
from TemplateUtilities.interfaceTemplates import *


def listarMicrolernys(micro_lerny):

    data = MicroLernySerializer(micro_lerny, many=True).data
    
    return listarMicrolernysTemplate("fbMessenger",data)