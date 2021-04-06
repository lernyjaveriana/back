from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_name", "user_surname", "identification")

admin.site.register(User, UserAdmin)
#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
#    """User admin."""

#    list_display = ('pk', 'username', 'email',)
#    list_display_links = ('pk', 'username', 'email',)

#    search_fields = (
#        'email',
#        'username',
#        'first_name',
#        'last_name',
#    )

#    list_filter = (
#        'is_active',
#        'is_staff',
#        'date_joined',
#        'modified',
#    )

#    readonly_fields = ('date_joined', 'modified',)