from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserRegisterForm, AdminUserChangeForm
from .models import *


class AccountAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = UserRegisterForm

    list_display = ('login', 'name', 'position')

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'vacation', 'position', 'vacation_days', )}),
    )
    add_fieldsets = (
        (None, {'fields': ('login', 'password1', 'password2')}),
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
