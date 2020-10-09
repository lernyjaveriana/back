from django.contrib import admin
from .models import User, User_Lerny, User_Micro_Lerny, User_Resource
# Register your models here.

admin.site.register(User)
admin.site.register(User_Lerny)
admin.site.register(User_Micro_Lerny)
admin.site.register(User_Resource)