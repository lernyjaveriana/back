from django.contrib import admin
from .models import Lerny, MicroLerny, TreeMicroLerny, Resource, User_State, User_Resource

# Register your models here

class LernyAdmin(admin.ModelAdmin):
    list_display = ('lerny_name')

admin.site.register(Lerny,LernyAdmin)
admin.site.register(MicroLerny)
admin.site.register(TreeMicroLerny)
admin.site.register(Resource)
admin.site.register(User_State)
admin.site.register(User_Resource)