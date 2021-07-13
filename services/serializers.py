from rest_framework import serializers

from .models import Conversation, System


class SystemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ['id', 'system_name']


class ConversationsSerializer(serializers.ModelSerializer):
    messenger_name = serializers.CharField(source='messenger', read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'conversation_name', 'messenger_name']
