from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
"""
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_name", "user_surname", "identification", "company", "group")
    search_fields =("identification",)
admin.site.register(User, UserAdmin)
"""
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

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('identification',)
    list_filter = ('identification',)
    fieldsets = (
        (None, {'fields': ('user_name', 'user_surname', 'country', 'city', 'uid', 'mail', 'notification', 'last_view_date', 'active_user', 'admin_user', 'identification', 'company', 'group', 'password')}),
        ('Permissions', {'fields': ()}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'user_surname', 'country', 'city', 'uid', 'mail', 'notification', 'last_view_date', 'active_user', 'admin_user', 'identification', 'company', 'group', 'password1', 'password2')}
        ),
    )
    search_fields = ('identification',)
    ordering = ('identification',)

admin.site.register(User, CustomUserAdmin)

