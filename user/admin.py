from django.contrib import admin
from .models import User
# Register your models here.

#admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ('pk', 'identification', 'mail', 'user_name', 'active_user', 'admin_user')
    #list_display_links = ('pk', 'user_name', 'mail',)

    search_fields = (
        'mail',
        'user_name',
        'first_name',
        'last_name',
    )

    list_filter = (
        'active_user',
        'admin_user',
        'identification',
    )

    #readonly_fields = ('date_joined', 'modified',)