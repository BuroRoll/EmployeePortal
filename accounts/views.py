from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.serializers import serialize
from django.shortcuts import render, redirect


from services import slackBot
from services.models import Conversation
from services.views import TGBotView
from .forms import *
from .forms import RegistrationForm
from .models import Account
from .models import Position


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.errors['Неверный логин или пароль'] = form.error_class(['Ошибка'])
            cd = form.cleaned_data
            user = authenticate(login=cd['login'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print('logined')
                    return redirect('/')

    else:
        form = LoginForm()
    return render(request, 'accounts/login1.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == 'POST':
        user_form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            print(user_form)
            user_form.save()
        return redirect('/')
    else:
        if Account.objects.filter(login=request.user)[0].position == 'HR' or Account.objects.filter(login=request.user)[0].position == 'hr':
            user_form = HrChangeForm(instance=request.user)
        else:
            user_form = UserChangeForm(instance=request.user)
        return render(request,
                      'accounts/account1.html',
                      {'user_form': user_form})
    # return render(request, 'accounts/account1.html', {'section': 'dashboard'})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            selected_conversations = request.POST.getlist('select')
            if user_form.cleaned_data['is_new_employee']:
                slackBot.post_message_to_slack(user_form)
                TGBotView.send_to_all(user_form)
            if len(selected_conversations) > 0:
                for conversations_for_accesses in Conversation.objects.filter(conversation_for_accesses=True):
                    if conversations_for_accesses.messenger.messenger_name == 'Telegram':
                        TGBotView.send_to_access(user_form.cleaned_data['name'],
                                                 user_form.cleaned_data['telegram_login'],
                                                 selected_conversations, conversations_for_accesses)
                    if conversations_for_accesses.messenger.messenger_name == 'Slack':
                        slackBot.send_msg_to_access(user_form.cleaned_data['name'],
                                                    user_form.cleaned_data['slack_login'],
                                                    selected_conversations, conversations_for_accesses)
            return redirect('/')
    # else:
    user_form = RegistrationForm()
    conversations = Conversation.objects.all()
    return render(request, 'accounts/register1.html', {'user_form': user_form, 'conversations': conversations})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            print(user_form)
            user_form.save()
        return redirect('/')
    else:
        user_form = UserChangeForm(instance=request.user)
        return render(request,
                      'accounts/edit.html',
                      {'user_form': user_form})


@login_required
def get_all_employees(request):
    employee = Account.objects.filter(is_superuser=False)
    positions = Position.objects.all()
    employee = serialize('json', employee, fields=['name', 'position'])
    positions = serialize('json', positions, fields=['position_name'])
    return render(request, 'accounts/table-test.html', {'employees': employee, 'positions': positions})



# let employees = JSON.parse('{{ employees | safe }}');
#     let positions = JSON.parse('{{ positions | safe }}');
#
#     for (let i = 0; i < employees.length; i++) {
#         let fio = employees[i].fields.name.split(' ');
#         let tr = document.createElement('tr');
#         tr.classList.add('candidate-list-block');
#         let td1 = tr.appendChild(document.createElement('td'));
#         td1.innerHTML = fio[0]
#         let td2 = tr.appendChild(document.createElement('td'))
#         td2.innerHTML = fio[1]
#         let td3 = tr.appendChild(document.createElement('td'))
#         td3.innerHTML = fio[2]
#         let td4 = tr.appendChild(document.createElement('td'))
#         td4.innerHTML = positions[employees[i].fields.position - 1].fields.position_name
#
#         document.getElementById('paged').appendChild(tr);
#     }
