from rest_framework import serializers

from .models import Event


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'picture', 'title', 'event_date', 'event_time', 'event_place', 'description', 'show_members',
                  'show_members_count', 'members_count', 'members', 'creator']


class EventMembersSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_members_name')

    def get_members_name(self, obj):
        return obj.members.values_list('name', flat=True)

    class Meta:
        model = Event
        fields = ['data']


class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'picture', 'title', 'event_date', 'event_time', 'event_place', 'description', 'show_members',
                  'show_members_count', 'members_count', 'members']
