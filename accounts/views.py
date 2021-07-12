import io

import xlsxwriter
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from services import slackBot
from services.models import Conversation, Messenger, System
from services.views import TGBotView
from .forms import *
from .forms import RegistrationForm
from .models import Account, Position, Candidate
from .serializer import VacationSerializer


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
def account(request):
    if request.method == 'POST':
        position = Position.objects.get(id=request.user.position.id)
        if position.access_to_candidates or position.access_to_vacation_list:
            user_form = SpecialAccessEmployeeForm(instance=request.user, data=request.POST, files=request.FILES)
        else:
            user_form = UserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
        return redirect('/')
    else:
        print(request.user.position.id)
        position = Position.objects.get(id=request.user.position.id)
        if position.access_to_candidates or position.access_to_vacation_list:
            user_form = SpecialAccessEmployeeForm(instance=request.user)
        else:
            user_form = UserChangeForm(instance=request.user)
        return render(request,
                      'accounts/account1.html',
                      {'user_form': user_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
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
            selected_conversations = request.POST.getlist('system')
            if user_form.cleaned_data['is_new_employee']:
                slackBot.post_message_to_slack(user_form)
                TGBotView.send_to_all(user_form)
            if len(selected_conversations) > 0:
                telegram_messenger_id = Messenger.objects.filter(messenger_name='Telegram')[0].id
                slack_messenger_id = Messenger.objects.filter(messenger_name='Slack')[0].id
                for conversations_for_accesses in Conversation.objects.filter(conversation_for_accesses=True):
                    if conversations_for_accesses.messenger_id == telegram_messenger_id:
                        TGBotView.send_to_access(user_form.cleaned_data['name'],
                                                 user_form.cleaned_data['telegram_login'],
                                                 selected_conversations, conversations_for_accesses)
                    elif conversations_for_accesses.messenger_id == slack_messenger_id:
                        slackBot.send_msg_to_access(user_form.cleaned_data['name'],
                                                    user_form.cleaned_data['slack_login'],
                                                    selected_conversations, conversations_for_accesses)
            return redirect('/')
        else:
            return render(request, 'accounts/register1.html', {'invalid': True, 'form': user_form})
    user_form = RegistrationForm()
    conversations = Conversation.objects.all()
    systems = System.objects.all()
    return render(request, 'accounts/register1.html',
                  {'user_form': user_form, 'conversations': conversations, 'systems': systems})


# Метод для получения списка сотрудников
@login_required
def get_all_employees(request):
    employee = Account.objects.filter(is_superuser=False)
    positions = Position.objects.all()
    employee = serialize('json', employee, fields=['name', 'position'])
    positions = serialize('json', positions, fields=['position_name'])
    return render(request, 'accounts/employees_table.html',
                  {'employees': employee, 'positions': positions})


@login_required
def get_all_candidates(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            new_candidate = form.save()
            return JsonResponse(
                {"name": new_candidate.name, "position": new_candidate.position_id, "id": new_candidate.id})
        else:
            return JsonResponse({"msg": "Invalid data"})
    candidates = Candidate.objects.all()
    positions = Position.objects.all()
    candidates = serialize('json', candidates, fields=['name', 'position'])
    positions = serialize('json', positions, fields=['position_name'])
    candidate_form = CandidateForm()
    return render(request, 'accounts/candidates_table.html',
                  {'candidates': candidates, 'positions': positions, 'candidate_form': candidate_form})


@login_required
def candidate_form(request):
    form = CandidateForm()
    return render(request, 'accounts/candidates_table.html', {"form": form})


@login_required
def delete_candidate(request):
    id = request.GET.get("id", )
    candidate = Candidate.objects.get(id=id)
    candidate.delete()
    return HttpResponse('Deleted')


@login_required
def vacations_table(request):
    return render(request, 'accounts/vacations.html')


@login_required
def download_vacations_page(request):
    return render(request, 'accounts/download_vacations.html')


@login_required
def download_vacations(request):
    users = Account.objects.filter(~Q(vacation=''))
    print_in_xlsx(users)
    file_location = 'media/Vacations.xlsx'
    with open(file_location, 'rb') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Vacations.xlsx"'
    return response


def print_in_xlsx(data):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook('media/Vacations.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.set_column('B:B', 24)
    worksheet.write(0, 0, 'Сотрудник', bold)
    worksheet.write(0, 1, 'Даты отпуска', bold)
    i = 1
    for user in data:
        worksheet.write(i, 0, user.name)
        worksheet.set_column('A:A', len(user.name))
        vac = user.vacation.split(';')
        for v in vac[:len(vac) - 1]:
            worksheet.write(i, 1, v)
            i += 1
    workbook.close()


@api_view(['POST'])
@login_required
def set_vacations_days(request):
    data = request.data
    user = Account.objects.filter(pk=request.user.pk)[0]
    user.set_vacation(data['day_counts'], data['vacations_days'])
    return HttpResponse('ok')


@permission_classes([IsAuthenticated])
class GetUserVacation(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = VacationSerializer
