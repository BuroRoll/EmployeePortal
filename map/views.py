from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Marker
from .serializers import MarkersSerializer


@login_required
def get_map_page(request):
    return render(request, 'map/map.html')


@login_required
@api_view(['POST'])
def create_marker(request):
    marker = Marker()
    data = request.data
    print(data)
    marker.place = data['place']
    marker.href = data['href']
    marker.date = data['date']
    marker.description = data['description']
    marker.owner = request.user
    marker.x_coordinate = data['x_coordinate']
    marker.y_coordinate = data['y_coordinate']
    marker.save()
    return Response({'success': 'ok', 'index_db': marker.pk})


@login_required
@api_view(['GET'])
def delete_marker(request):
    marker_id = request.GET.get('marker_id')
    Marker.objects.filter(pk=marker_id).delete()
    return Response({'success': 'ok'})


@permission_classes([IsAuthenticated])
class MarkersList(generics.ListAPIView):
    queryset = Marker.objects.all()
    serializer_class = MarkersSerializer
