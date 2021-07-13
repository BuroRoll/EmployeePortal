from datetime import datetime

from django.db import models
from django.utils import timezone

from accounts.models import Account


class TypeOfDevice(models.Model):
    device_type = models.CharField(max_length=200)

    def __str__(self):
        return self.device_type


class Device(models.Model):
    name = models.CharField(max_length=250)
    device_type = models.ForeignKey(TypeOfDevice, on_delete=models.CASCADE, default=1)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    time_of_taking = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def set_owner(self, owner):
        self.owner = owner
        self.time_of_taking = datetime.now(tz=timezone.utc)
        self.save()

    def unset_owner(self):
        self.owner = None
        self.time_of_taking = None
        self.save()
