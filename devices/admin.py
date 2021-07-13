from django.contrib import admin

from .forms import DeviceForm
from .models import Device, TypeOfDevice

admin.site.register(TypeOfDevice)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'owner_fio', 'time_of_taking')
    form = DeviceForm

    @staticmethod
    def owner_fio(obj):
        if obj.owner:
            return obj.owner.name
        else:
            return 'Устройство свободно'
