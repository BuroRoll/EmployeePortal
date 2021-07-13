from django import forms

from accounts.models import Account
from .models import Device


class CustomDeviceOwnerField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

    class Meta:
        model = Device


class DeviceForm(forms.ModelForm):
    owner = CustomDeviceOwnerField(queryset=Account.objects.all(), required=False)
