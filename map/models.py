from django.db import models
from accounts.models import Account


class Marker(models.Model):
    x_coordinate = models.CharField(max_length=100)
    y_coordinate = models.CharField(max_length=100)
    place = models.CharField(max_length=350)
    href = models.CharField(max_length=1000)
    date = models.CharField(max_length=20)
    description = models.TextField()
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.place
