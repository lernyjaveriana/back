from ..models import User
from lerny.models import *
from lerny.serializers import *


def pqr(user_id_obj,user_state,user_pqr):
    print("GUARDAR PQR")
    new_pqr = PQR()
    new_pqr.user_id = user_id_obj
    new_pqr.user_state = user_state
    new_pqr.pqr = user_pqr
    new_pqr.save()
    return user_pqr