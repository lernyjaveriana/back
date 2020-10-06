from django.contrib import admin
from .models import Lerny, MicroLerny, TreeMicroLerny, Resource

# Register your models here.


admin.site.register(Lerny)
admin.site.register(MicroLerny)
admin.site.register(TreeMicroLerny)
admin.site.register(Resource)