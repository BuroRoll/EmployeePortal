from rest_framework import serializers

from .models import Account


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'vacation_days', 'vacation']
