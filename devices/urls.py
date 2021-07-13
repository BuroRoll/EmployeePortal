from django.urls import path

from . import views

urlpatterns = [
    path('devices/', views.devices, name='devices'),
    path('set_owner/', views.set_owner, name='set_owner'),
    path('unset_owner/', views.unset_owner, name='unset_owner'),
    path('devices_list/', views.DevicesList.as_view()),
    path('devices_details/<int:pk>/', views.DevicesDetails.as_view()),
]
