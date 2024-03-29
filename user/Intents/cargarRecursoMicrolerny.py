from ..models import User
from lerny.models import *
from lerny.serializers import *
from user.Intents.continueLerny import mediaResponseFormat,saveStateLogs,saveState,mediaResponseUrlList
from .TemplateUtilities.interfaceTemplates import *

def cargarRecursoMicrolerny(user_id,microlerny,user_id_obj,lerny_active,user_state):

    #the following code creates from scratch the user state, that means the user has never seen this lerny before
    if(user_state):
        user_state = user_state.first()
        lerny_id = user_state.lerny_id
        micro_lerny = MicroLerny.objects.filter(lerny=lerny_id,id=microlerny).first()
        resourse = Resource.objects.get(
            microlerny=micro_lerny, phase='1')

        user_state.resource_id = resourse
        user_state.micro_lerny_id = micro_lerny
        saveStateLogs(user_state.lerny_id, user_state.micro_lerny_id, user_state.user_id, user_state.resource_id)
        user_state.save()
        dataDB = ResourceSerializer(resourse).data
    
    else:
        lerny_id = lerny_active.lerny_id
        micro_lerny = MicroLerny.objects.filter(lerny=lerny_id,pk=microlerny).first()
        resourse = Resource.objects.get(
            microlerny=micro_lerny, phase='1')


        saveState(lerny_id,micro_lerny,user_id_obj,resourse)

        dataDB = ResourceSerializer(resourse).data
    print("Data, description: "+dataDB["description"])
    templates=mediaResponseFormat(resourse)
    return cargarRecursoMicrolernyTemplate ("fbMessenger",dataDB,templates,resourse)
