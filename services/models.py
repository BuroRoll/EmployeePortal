from django.db import models


class Messenger(models.Model):
    messenger_name = models.CharField(max_length=100)

    def __str__(self):
        return self.messenger_name


class Conversation(models.Model):
    conversation_name = models.CharField(max_length=150)
    conversation_id = models.CharField(max_length=150, unique=True)
    token = models.CharField(max_length=150)
    messenger = models.ForeignKey(Messenger, on_delete=models.CASCADE)
    admin = models.CharField(max_length=150)
    hr_conversation = models.BooleanField(default=False)
    conversation_for_accesses = models.BooleanField(default=False)

    def __str__(self):
        return self.conversation_name
