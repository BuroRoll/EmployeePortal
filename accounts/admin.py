from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserRegisterForm, UserChangeForm
from .models import *


class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserRegisterForm

    list_display = ('login', 'name', 'position')

    fieldsets = (
        (None, {'fields': ('login', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'photo', 'position')}),
    )
    add_fieldsets = (
        (None, {'fields': ('login', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'phone')}),
    )

    search_fields = ('name',)
    list_filter = ('position', )
    ordering = ('login',)
    filter_horizontal = ()


class CandidatesAdmin(admin.ModelAdmin):
    model = Candidate
    list_display = ('name', 'position')


admin.site.register(Account, AccountAdmin)
admin.site.register(Position)
admin.site.register(Candidate, CandidatesAdmin)
admin.site.unregister(Group)
