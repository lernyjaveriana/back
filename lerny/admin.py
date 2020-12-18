from django.contrib import admin
from .models import *

# Register your models here.


#admin.site.register(Lerny)
@admin.register(Lerny)
class LernyAdmin(admin.ModelAdmin):
	list_display = ("pk", "lerny_name", "description", "url_image", "category", "price", "creation_date")

@admin.register(MicroLerny)
class MicroLernyAdmin(admin.ModelAdmin):
	list_display = ("pk", "micro_lerny_title", "micro_lerny_subtitle", "update_date", "creation_date", "get_lerny")

	def get_lerny(self, obj):
		return obj.lerny.lerny_name

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
	list_display = ("pk", "title", "description", "content_url", "content_type", "phase", "creation_date", "points", "get_microlerny")

	def get_microlerny(self, obj):
		return obj.microlerny.micro_lerny_title

@admin.register(TreeMicroLerny)
class TreeMicroLernyAdmin(admin.ModelAdmin):
	list_display = ("pk", "get_dady_microlerny", "get_son_microlerny")

	def get_dady_microlerny(self, obj):
		return obj.dady_micro_lerny.micro_lerny_title
	
	def get_son_microlerny(self, obj):
		return obj.son_micro_lerny.micro_lerny_title


@admin.register(User_State)
class UserStateAdmin(admin.ModelAdmin):
	list_display = ("pk", "get_lerny", "get_microlerny","get_user", "get_resource", "last_view_date")

	def get_lerny(self, obj):
		return obj.lerny_id.lerny_name
	
	def get_microlerny(self, obj):
		return obj.micro_lerny_id.micro_lerny_title

	def get_user(self, obj):
		return obj.user_id.identification

	def get_resource(self, obj):
		return obj.resource_id.title


@admin.register(User_Lerny)
class UserLernyAdmin(admin.ModelAdmin):
	list_display = ("pk", "get_lerny", "get_microlerny","get_user", "get_resource", "last_view_date")

	def get_lerny(self, obj):
		return obj.lerny_id.lerny_name
	
	def get_microlerny(self, obj):
		return obj.micro_lerny_id.micro_lerny_title

	def get_user(self, obj):
		return obj.user_id.identification

	def get_resource(self, obj):
		return obj.resource_id.title

@admin.register(User_Resource)
class UserLernyAdmin(admin.ModelAdmin):
	list_display = ("pk", "get_resource", "user_id","done", "user_response", "response_date", "last_view_date", "done_date")

	def get_resource(self, obj):
		return obj.resource_id.title
	
	def get_user(self, obj):
		return obj.user_id.identification
