from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Device
from .serializers import DevicesSerializer, DeviceDetailsSerializer


@api_view(['GET'])
def set_owner(request):
    device_id = request.GET.get('device_id')
    device = Device.objects.get(pk=device_id)
    if device.owner is not None:
        return Response({'success': 'false'})
    owner = request.user
    device.set_owner(owner)
    return Response({'success': 'ok'})


@api_view(['GET'])
def unset_owner(request):
    device_id = request.GET.get('device_id')
    device = Device.objects.get(pk=device_id)
    if device.owner is None or request.user.pk != device.owner.id:
        return Response({'success': 'false'})
    device.unset_owner()
    return Response({'success': 'ok'})


@permission_classes([IsAuthenticated])
class DevicesList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DevicesSerializer


@permission_classes([IsAuthenticated])
class DevicesDetails(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceDetailsSerializer


@login_required
def devices(request):
    return render(request, 'devices/devices.html')
