from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'date_joined')
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'date_joined', 'is_staff',
         'is_active')}),
        ('Permissions', {'fields': ()}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('username', 'email', 'password1', 'password2', 'date_joined',
                        'is_staff', 'is_active')}
         ),
    )
    ordering = ('date_joined',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
