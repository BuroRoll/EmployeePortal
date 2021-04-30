from django.urls import path
from . import views

urlpatterns = [
    path('get_access/', views.get_system_access, name='systems_access')
]