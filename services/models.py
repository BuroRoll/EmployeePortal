from django.db import models


class Messenger(models.Model):
    messenger_name = models.CharField(max_length=100)

    def __str__(self):
        return self.messenger_name


class Conversation(models.Model):
    conversation_name = models.CharField(max_length=150)
    conversation_id = models.CharField(max_length=150, blank=True)
    token = models.CharField(max_length=150, blank=True)
    messenger = models.ForeignKey(Messenger, on_delete=models.CASCADE, blank=True)
    admin = models.CharField(max_length=150, blank=True)
    hr_conversation = models.BooleanField(default=False)
    conversation_for_accesses = models.BooleanField(default=False)

    def __str__(self):
        return self.conversation_name
