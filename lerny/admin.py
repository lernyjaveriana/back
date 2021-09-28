from django.contrib import admin
from .models import Faqs, Faqs_Lerny, Lerny, MicroLerny, TreeMicroLerny, Resource, User_State, User_Resource, User_Lerny, Company, Lerny_Company, User_Micro_Lerny, Media, User_State_Logs, Group, User_Group

# Register your models here

class UserLernyAdmin(admin.ModelAdmin):
    list_display = ("lerny_id","user_id")
    list_filter=("user_id","lerny_id")

class MediaAdmin(admin.ModelAdmin):
    list_filter=("resource_id",)
    list_display = ("resource_id","content_type")


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
    list_display = ("user_id","resource_id", "done")

class Faqs_Lerny_ResourceAdmin(admin.ModelAdmin):
    list_filter=("lerny_id",)
    list_display = ("lerny_id","intent_name")

class CompanyAdmin(admin.ModelAdmin):
    list_filter=("nit",)
    list_display = ("nit","name", "country", "creation_date")

class Group_ResourceAdmin(admin.ModelAdmin):
    list_filter=("lerny_id",)
    list_display = ("Group_name","lerny_id")

class User_Group_ResourceAdmin(admin.ModelAdmin):
    list_filter=("User_id",)
    list_display = ("Group_id","User_id")



admin.site.register(Group,Group_ResourceAdmin)
admin.site.register(User_Group,User_Group_ResourceAdmin)
admin.site.register(Lerny,LernyAdmin)
admin.site.register(User_Lerny,UserLernyAdmin)
admin.site.register(MicroLerny,MicroLernyAdmin)
admin.site.register(TreeMicroLerny)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(User_State)
admin.site.register(User_State_Logs)
admin.site.register(User_Resource,User_ResourceAdmin)
admin.site.register(Faqs)
admin.site.register(Faqs_Lerny,Faqs_Lerny_ResourceAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Lerny_Company)
admin.site.register(User_Micro_Lerny)
admin.site.register(Media,MediaAdmin)