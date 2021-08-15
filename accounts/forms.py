from django import forms
from django.db.models import Q

from .models import Account, Candidate, Position


# Форма для регистрации обычных польщователей
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = None

    class Meta:
        model = Account
        fields = (
            'login', 'name', 'phone', 'photo', 'info', 'position', 'is_new_employee', 'slack_login', 'telegram_login')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Форма для регистрации пользователя через панель администратора
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('login', 'name', 'phone', 'photo', 'is_staff', 'is_superuser')

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


# Форма редактирования профиля для обычных пользователей
class UserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = None
        self.fields['position'].queryset = Position.objects.filter(~Q(access_to_candidates=True))
        self.fields['position'].queryset = Position.objects.filter(~Q(access_to_vacation_list=True))
        self.fields['position'].queryset = Position.objects.filter(~Q(change_events=True))

    class Meta:
        model = Account
        fields = ('name', 'photo', 'phone', 'slack_login', 'telegram_login', 'position', 'info')


# Форма редактирования профиля для пользователей с доступами к специальным разделам
class SpecialAccessEmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpecialAccessEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = None

    class Meta:
        model = Account
        fields = ('name', 'photo', 'phone', 'slack_login', 'telegram_login', 'position', 'info')


# Форма для редактирования пользователей через панель администратора
class AdminUserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = None

    class Meta:
        model = Account
        fields = ('name', 'photo', 'phone', 'slack_login', 'telegram_login', 'position', 'info')


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('name', 'position')
