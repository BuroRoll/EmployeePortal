from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import *
from .forms import RegistrationForm
from services import slackBot
from services.views import TGBotView
from .models import Account
from services.models import Conversation


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            form.errors['Неверный логин или пароль'] = form.error_class(['Ошибка'])
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print('logined')
                    return redirect('/')

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'accounts/account1.html', {'section': 'dashboard'})


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
            print(request.POST)
            if user_form.cleaned_data['is_new_employee']:
                slackBot.post_message_to_slack(user_form)
                TGBotView.send_to_all(user_form)
            for conversations_for_accesses in Conversation.objects.filter(conversation_for_accesses=True):
                if conversations_for_accesses.messenger.messenger_name == 'Telegram':
                    TGBotView.send_to_access(user_form.cleaned_data['name'], user_form.cleaned_data['telegram_login'],
                                             selected_conversations, conversations_for_accesses)
                if conversations_for_accesses.messenger.messenger_name == 'Slack':
                    slackBot.send_msg_to_access(user_form.cleaned_data['name'], user_form.cleaned_data['slack_login'],
                                                selected_conversations, conversations_for_accesses)
            return redirect('/')
    else:
        user_form = RegistrationForm()
        conversations = Conversation.objects.all()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'conv': conversations})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
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
    return render(request, 'accounts/all_employees.html', {'employees': employee})
