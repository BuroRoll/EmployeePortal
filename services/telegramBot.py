import os
import json

import requests
from django.http import JsonResponse
from django.views import View

from .models import Conversation, Messenger

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = os.getenv('BOT_TOKEN')


# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/telegram/
class TelegramBot(View):
    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        if 'my_chat_member' not in t_data:
            t_message = t_data["message"]
            t_chat = t_message["chat"]
            try:
                text = t_message["text"].strip().lower()
            except Exception as _:
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
        }
        requests.post(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)

    @staticmethod
    def send_to_all(data):
        mess = Messenger.objects.get(messenger_name='Telegram')
        channels = Conversation.objects.filter(messenger=mess)
        name = data.cleaned_data['name']
        position = str(data.cleaned_data['position'])
        phone = data.cleaned_data['phone']
        info = data.cleaned_data['info']
        msg_for_hr = f'У нас новый сотрудник {name}  \n' \
                     f'На должности {position} \n' \
                     f'Телефон: {phone} \n' \
                     f'Немного информации о нём: {info}'
        msg_for_all = f'У нас новый сотрудник {name} \n' \
                      f'На должности {position}'
        for channel in channels:
            if channel.hr_conversation:
                data = {
                    "chat_id": channel.conversation_id,
                    "text": msg_for_hr,
                }
                requests.post(
                    f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)
            elif channel.conversation_for_info:
                data = {
                    "chat_id": channel.conversation_id,
                    "text": msg_for_all,
                }
                requests.post(
                    f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)

    @staticmethod
    def send_to_access(name, login, selected_conversations, conversation):
        if isinstance(selected_conversations, str):
            msg = 'Сотруднику ' + name + '(@' + login + ')' + '\n' \
                  + 'Нужен доступ к ' + selected_conversations
        else:
            msg = 'Сотруднику ' + name + '(@' + login + ')' + '\n' \
                  + 'Нужен доступ к ' + ', '.join(selected_conversations)

        data = {
            "chat_id": conversation.conversation_id,
            "text": msg,
        }
        requests.post(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)
