import json

import requests

from .models import Conversation, Messenger


def post_message_to_slack(data, slack_user_name='Новый сотрудник', blocks=None):
    mess = Messenger.objects.get(messenger_name='Slack')
    channels = Conversation.objects.filter(messenger=mess)
    msg_for_hr = 'У нас новый сотрудник ' + data.cleaned_data['name'] + '\n' \
                 + 'На должности ' + str(data.cleaned_data['position']) + '\n' \
                 + 'Телефон ' + data.cleaned_data['phone'] + '\n' \
                 + 'Немного информации о нём ' + data.cleaned_data['info']

    msg_for_all = 'У нас новый сотрудник ' + data.cleaned_data['name'] + '\n' \
                  + 'На должности ' + str(data.cleaned_data['position'])
    for channel in channels:
        if channel.hr_conversation:
            requests.post('https://slack.com/api/chat.postMessage', {
                'token': channel.token,
                'channel': channel.conversation_id,
                'text': msg_for_hr,
                'username': slack_user_name,
                'blocks': json.dumps(blocks) if blocks else None
            }).json()
        elif channel.conversation_for_info:
            requests.post('https://slack.com/api/chat.postMessage', {
                'token': channel.token,
                'channel': channel.conversation_id,
                'text': msg_for_all,
                'username': slack_user_name,
                'blocks': json.dumps(blocks) if blocks else None
            }).json()


def send_msg_to_access(name, login, selected_conversations, conversation, blocks=None):
    if isinstance(selected_conversations, str):
        msg = 'Сотруднику ' + name + '(@' + login + ')' + '\n' \
              + 'Нужен доступ к ' + selected_conversations
    else:
        msg = 'Сотруднику ' + name + '(@' + login + ')' + '\n' \
              + 'Нужен доступ к ' + ', '.join(selected_conversations)
    requests.post('https://slack.com/api/chat.postMessage', {
        'token': conversation.token,
        'channel': conversation.conversation_id,
        'text': msg,
        'username': 'Доступ к системам',
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
