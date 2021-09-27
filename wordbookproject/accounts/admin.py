from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('login_id', 'date_joined')

    list_filter = ()

    fieldsets = (
        (None, {'fields': ('login_id', 'password')}),
        ('Permissions', {'fields': ()}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login_id', 'password1', 'password2')}
        ),
    )
    ordering = ('login_id',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)