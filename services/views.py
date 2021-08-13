from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import slackBot
from .models import Conversation, Messenger, System
from .serializers import SystemsSerializer, ConversationsSerializer
from .telegramBot import TelegramBot


@permission_classes([IsAuthenticated])
class SystemsList(generics.ListAPIView):
    queryset = System.objects.all()
    serializer_class = SystemsSerializer


@permission_classes([IsAuthenticated])
class ConversationsList(generics.ListAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationsSerializer


@login_required
def get_system_access(request):
    return render(request, 'systems/systems.html')


@api_view(['GET'])
def get_systems(request):
    systems = System.objects.all()
    systems = SystemsSerializer(systems, many=True).data
    return Response({'systems': systems})


@api_view(['POST'])
@login_required
def send_request_for_access(request):
    if request.data['type'] == 'System':
        selected = System.objects.get(id=request.data['id']).system_name
    elif request.data['type'] == 'Conversation':
        selected = Conversation.objects.get(id=request.data['id']).conversation_name
    username = request.user.name
    telegram_login = request.user.telegram_login
    slack_login = request.user.slack_login
    telegram_messenger_id = Messenger.objects.filter(messenger_name='Telegram')[0].id
    slack_messenger_id = Messenger.objects.filter(messenger_name='Slack')[0].id
    for conversations_for_accesses in Conversation.objects.filter(conversation_for_accesses=True):
        if conversations_for_accesses.messenger_id == telegram_messenger_id:
            TelegramBot.send_to_access(username,
                                       telegram_login,
                                       selected, conversations_for_accesses)
        elif conversations_for_accesses.messenger_id == slack_messenger_id:
            slackBot.send_msg_to_access(username,
                                        slack_login,
                                        selected, conversations_for_accesses)

    return Response({'success': 'ok'})
