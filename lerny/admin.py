from django.contrib import admin
from .models import *

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

# Support tables 
class Support_Resource_ResourceAdmin(admin.ModelAdmin):
    list_filter=("name",)
    list_display = ("name","text")
class Support_Resource_Microlerny_Lerny_ResourceAdmin(admin.ModelAdmin):
    list_filter=("Support_Resource_id",)
    list_display = ("Support_Resource_id",)
class Score_ResourceAdmin(admin.ModelAdmin):
    list_filter=("Support_Resource_Microlerny_Lerny",)
    list_display = ("Support_Resource_Microlerny_Lerny","User")

class pqr_ResourceAdmin(admin.ModelAdmin):
    list_filter=("user_id",)
    list_display = ("user_state","user_id","pqr","type","priority","ticket","state")

class User_quiz_logsAdmin(admin.ModelAdmin):
    list_filter=("user_id",)
    list_display = ("user_id","user_quiz_id","response","points","state_quiz")

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
admin.site.register(Support_Resource,Support_Resource_ResourceAdmin)
admin.site.register(Support_Resource_Microlerny_Lerny,Support_Resource_Microlerny_Lerny_ResourceAdmin)
admin.site.register(Score,Score_ResourceAdmin)
admin.site.register(PQR,pqr_ResourceAdmin)
admin.site.register(User_quiz_logs,User_quiz_logsAdmin)