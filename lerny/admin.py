from django.contrib import admin
from .models import Lerny, MicroLerny, TreeMicroLerny, Resource, User_State, User_Resource, User_Lerny

# Register your models here

class UserLernyAdmin(admin.ModelAdmin):
    list_display = ("lerny_id","user_id")
    list_filter=("user_id","lerny_id")

class LernyAdmin(admin.ModelAdmin):
    list_display = ("lerny_name","description", "price")

class MicroLernyAdmin(admin.ModelAdmin):
    list_filter=("lerny",)
    list_display = ("micro_lerny_title","micro_lerny_subtitle","lerny")

class ResourceAdmin(admin.ModelAdmin):
    list_filter=("phase", "microlerny")
    list_display = ("title","phase", "microlerny")


class User_ResourceAdmin(admin.ModelAdmin):
    list_filter=("user_id",)
    list_display = ("user_id","resource_id")

admin.site.register(Lerny,LernyAdmin)
admin.site.register(MicroLerny,MicroLernyAdmin)
admin.site.register(TreeMicroLerny)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(User_State)
admin.site.register(User_Resource,User_ResourceAdmin)