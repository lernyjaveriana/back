from django.contrib import admin
from .models import Lerny, MicroLerny, TreeMicroLerny, Resource, User_State, User_Resource

# Register your models here.


admin.site.register(Lerny)
admin.site.register(MicroLerny)
admin.site.register(TreeMicroLerny)
admin.site.register(Resource)
admin.site.register(User_State)
admin.site.register(User_Resource)