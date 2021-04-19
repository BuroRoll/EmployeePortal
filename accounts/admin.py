from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *
from .forms import UserRegisterForm, UserChangeForm


class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserRegisterForm

    list_display = ('email', 'name', 'position')

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'photo', 'position')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'phone')}),
    )

    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
admin.site.register(Position)
admin.site.unregister(Group)



