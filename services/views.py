import json

import requests
from django.http import JsonResponse
from django.views import View
from .models import Conversation, Messenger

TELEGRAM_URL = "https://api.telegram.org/bot"
BOT_TOKEN = '1758647032:AAGzI_bIdCfptgajV9GTrDM5G25LmCrhRWM'


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
            else:
                data = {
                    "chat_id": channel.conversation_id,
                    "text": msg_for_all,
                    "parse_mode": "Markdown",
                }
                requests.post(
                    f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", data=data)
