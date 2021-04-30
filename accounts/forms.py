from django import forms

from .models import Account, Candidate


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

    # def clean_login(self):
    #     login = self.cleaned_data.get('login')
    #     if Account.objects.filter(login=login).exists():
    #         print('Login error!!!')
    #         raise forms.ValidationError({"some_field": "raise an error",})


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


# class ImagePreviewWidget(forms.widgets.FileInput):
#     def render(self, name, value, attrs=None, **kwargs):
#         input_html = super().render(name, value, attrs=None, **kwargs)
#         img_html = mark_safe(f'<img height="300px" src="{value.url}"/><br>')
#         return f'{img_html}{input_html}'


class UserChangeForm(forms.ModelForm):
    # photo = forms.ImageField(label=('Фото'), required=False, error_messages={'invalid': ("Image files only")},
    #                          widget=ImagePreviewWidget)
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = None
        # self.fields['position'].queryset = Position.objects.filter(~Q(position_name='HR'))

    class Meta:
        model = Account
        fields = ('name', 'photo', 'phone', 'slack_login', 'telegram_login', 'position')


class HrChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HrChangeForm, self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = None

    class Meta:
        model = Account
        fields = ('name', 'photo', 'phone', 'slack_login', 'telegram_login', 'position')


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('name', 'position')
