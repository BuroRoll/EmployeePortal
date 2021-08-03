from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Event
from .serializers import EventsSerializer, EventMembersSerializer, EventDetailsSerializer


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
    print(event.members.count())
    print(event.members_count)
    if event.members.count() >= event.members_count:
        print('много людей')
        return Response({'success': 'error'})
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
        # title=data['title'],
        event_date=data['event_date'],
        event_time=data['event_time'],
        event_place=data['event_place'],
        description=data['description'],
        # show_members=data['show_members'],
        # show_members_count=data['show_members_count'],
        members_count=data['members_count'],
    )
    return Response({'success': 'ok'})


@api_view(['POST'])
@login_required
def create_event(request):
    print(request.data)
    data = request.data
    files = request.FILES
    event = Event()
    event.title = data['name']
    event.event_date = data['date-event']
    event.event_time = data['time-event']
    event.event_place = data['location-event']
    event.description = data['description']
    if 'view-list' in data:
        event.show_members = data['view-list'] == 'on'
    if 'view-count' in data:
        event.show_members_count = data['view-count'] == 'on'
    event.members_count = data['event-count']
    if len(files) != 0:
        event.picture = files.get('photo')
    event.creator = request.user
    event.save()
    return Response({'success': 'ok', 'event_id': event.pk})


@login_required
def event_manager(request):
    user_events = Event.objects.filter(creator=request.user.id)
    for event in user_events:
        event.free_count = event.members_count - event.members.all().count()
    return render(request, 'events/event-manager.html', {'events': user_events})


@permission_classes([IsAuthenticated])
class EventsMembers(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventMembersSerializer


@permission_classes([IsAuthenticated])
class EventDetails(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailsSerializer
