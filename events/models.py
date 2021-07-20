from django.db import models

from accounts.models import Account


class Event(models.Model):
    title = models.CharField(max_length=300)
    picture = models.ImageField(upload_to='events/%Y/%m/%d', blank=True, default='events/default_event_pic.png')
    event_date = models.CharField(max_length=300)
    event_time = models.CharField(max_length=300)
    event_place = models.CharField(max_length=300)
    description = models.TextField(max_length=600)
    show_members = models.BooleanField(default=False)
    show_members_count = models.BooleanField(default=False)
    members_count = models.IntegerField(null=True)
    members = models.ManyToManyField(Account, related_name='member')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='creator')

    def __str__(self):
        return self.title
