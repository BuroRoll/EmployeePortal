from django import forms
from .models import Account

from django.forms.widgets import FileInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from string import Template
from django.utils.safestring import mark_safe
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'name', 'phone', 'photo', 'info', 'position', 'is_new_employee')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'name', 'phone', 'photo', 'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<img height="300px" src="{value.url}"/><br>')
        return f'{img_html}{input_html}'


class UserChangeForm(forms.ModelForm):
    photo = forms.ImageField(label=('Фото'), required=False, error_messages={'invalid': ("Image files only")},
                             widget=ImagePreviewWidget)
    # phone = forms.

    class Meta:
        model = Account
        fields = ('email', 'name', 'phone', 'photo', 'info', 'slack_login', 'telegram_login')


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
