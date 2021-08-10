from rest_framework import serializers

from .models import Marker


class MarkersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='owner.name')
    coordinates = serializers.SerializerMethodField('get_coordinates')
    myMarker = serializers.SerializerMethodField('is_my_marker')

    def get_coordinates(self, obj):
        return [obj.x_coordinate, obj.y_coordinate]

    def is_my_marker(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.pk == obj.owner.pk:
                return True
        return False

    class Meta:
        model = Marker
        fields = ['id', 'place', 'href', 'date', 'description', 'name', 'coordinates', 'myMarker']
