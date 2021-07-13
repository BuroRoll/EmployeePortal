from rest_framework import serializers

from .models import Device


class DevicesSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='device_type', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'type', 'owner']


class DeviceDetailsSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', default=None)
    owner_id = serializers.CharField(source='owner.pk', default=None)
    owner_telegram = serializers.CharField(source='owner.telegram_login', default=None)
    owner_slack = serializers.CharField(source='owner.slack_login', default=None)
    owner_phone = serializers.CharField(source='owner.phone', default=None)
    time_of_taked = serializers.DateTimeField(source='time_of_taking', format="%Y-%m-%d %H:%M")

    class Meta:
        model = Device
        fields = ['id', 'name', 'owner_name', 'owner_id', 'time_of_taked', 'owner_telegram', 'owner_slack',
                  'owner_phone']
