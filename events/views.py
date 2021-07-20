from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Event
from .serializers import EventsSerializer, EventMembersSerializer


@permission_classes([IsAuthenticated])
class EventsList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer


@login_required
def events(request):
    return render(request, 'events/events.html')


@api_view(['GET'])
@login_required
def join_in_event(request):
    event_id = request.GET.get('event_id')
    event = Event.objects.get(pk=event_id)
    event.members.add(request.user)
    return Response({'success': 'ok'})


@api_view(['GET'])
@login_required
def unjoin_in_event(request):
    event_id = request.GET.get('event_id')
    event = Event.objects.get(pk=event_id)
    event.members.remove(request.user)
    return Response({'success': 'ok'})


@api_view(['GET'])
@login_required
def delete_event(request):
    event_id = request.GET.get('event_id')
    try:
        event = Event.objects.filter(pk=event_id)
        event.delete()
        if event.delete():
            return Response({'success': 'ok'})
        return Response({'success': 'fail, something wrong'})
    except ObjectDoesNotExist:
        return Response({'success': 'fail, Object does not exist'})


@api_view(['POST'])
@login_required
def update_event(request):
    data = request.data
    Event.objects.filter(pk=data['event_id']).update(
        title=data['title'],
        event_date=data['event_date'],
        event_place=data['event_place'],
        description=data['description'],
        show_members=data['show_members'],
        show_members_count=data['show_members_count'],
        members_count=data['members_count'],
    )
    return Response({'success': 'ok'})


@api_view(['POST'])
@login_required
def create_event(request):
    data = request.data
    event = Event()
    event.title = data['title']
    event.event_date = data['event_date']
    event.event_time = data['event_time']
    event.event_place = data['event_place']
    event.description = data['description']
    event.show_members = data['show_members']
    event.show_members_count = data['show_members_count']
    event.members_count = data['members_count']
    event.creator = request.user
    event.save()
    return Response({'success': 'ok'})

@login_required
def event_manager(request):
    return render(request, 'events/event-manager.html')


class EventsMembers(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventMembersSerializer
