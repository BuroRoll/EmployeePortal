import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from accounts.models import Account, Position
from . import slackBot

from .models import Conversation, Messenger, System

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = '1758647032:AAFDLU2mbQ7TS3o2Ywbq65xIv9KJALNj2uE'


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/telegram/
class TGBotView(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        if 'my_chat_member' not in t_data:
            t_message = t_data["message"]
            t_chat = t_message["chat"]
            try:
                text = t_message["text"].strip().lower()
            except Exception as e:
                return JsonResponse({"ok": "POST request processed"})
            text = text.lstrip("/")
            if text == 'add_chat':
                if not Conversation.objects.filter(conversation_id=t_chat['id']).exists():
                    tg = Messenger.objects.get(messenger_name='Telegram')
                    Conversation(conversation_name=t_chat['title'], conversation_id=t_chat['id'], token=BOT_TOKEN,
                                 admin='admin', messenger=tg).save()
                    self.send_message('Чат успешно добавлен', t_chat['id'])
                else:
                    self.send_message('Данный чат уже добавлен', t_chat['id'])
        return JsonResponse({"ok": "POST request processed"})

    @staticmethod
    def send_message(message, chat_id):
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        requests.post(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)

    @staticmethod
    def send_to_all(data):
        mess = Messenger.objects.get(messenger_name='Telegram')
        channels = Conversation.objects.filter(messenger=mess)
        msg_for_hr = 'У нас новый сотрудник ' + data.cleaned_data['name'] + '\n' \
                     + 'На должности ' + str(data.cleaned_data['position']) + '\n' \
                     + 'Телефон ' + data.cleaned_data['phone'] + '\n' \
                     + 'Немного информации о нём ' + data.cleaned_data['info']

        msg_for_all = 'У нас новый сотрудник ' + data.cleaned_data['name'] + '\n' \
                      + 'На должности ' + str(data.cleaned_data['position'])
        for channel in channels:
            if channel.hr_conversation:
                data = {
                    "chat_id": channel.conversation_id,
                    "text": msg_for_hr,
                    "parse_mode": "Markdown",
                }
                requests.post(
                    f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)
            elif not channel.conversation_for_accesses:
                data = {
                    "chat_id": channel.conversation_id,
                    "text": msg_for_all,
                    "parse_mode": "Markdown",
                }
                requests.post(
                    f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)

    @staticmethod
    def send_to_access(name, login, selected_conversations, conversation):
        msg = 'Сотруднику ' + name + '(@' + login + ')' + '\n' \
              + 'Нужен доступ к ' + ', '.join(selected_conversations)

        data = {
            "chat_id": conversation.conversation_id,
            "text": msg,
            "parse_mode": "Markdown",
        }
        requests.post(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)


@login_required
def get_system_access(request):
    if request.method == 'POST':
        selected_system = request.POST.getlist('system')
        print(type(request.user.position))
        username = request.user.name
        telegram_login = request.user.telegram_login
        slack_login = request.user.slack_login
        telegram_messenger_id = Messenger.objects.filter(messenger_name='Telegram')[0].id
        slack_messenger_id = Messenger.objects.filter(messenger_name='Slack')[0].id
        for conversations_for_accesses in Conversation.objects.filter(conversation_for_accesses=True):
            if conversations_for_accesses.messenger_id == telegram_messenger_id:
                TGBotView.send_to_access(username,
                                         telegram_login,
                                         selected_system, conversations_for_accesses)
            elif conversations_for_accesses.messenger_id == slack_messenger_id:
                slackBot.send_msg_to_access(username,
                                            slack_login,
                                            selected_system, conversations_for_accesses)
    conversations = Conversation.objects.all()
    systems = System.objects.all()

    return render(request,
                  'systems/systems.html', {'conversations': conversations, 'systems': systems})
