from django.urls import path

from . import views

urlpatterns = [
    path('map/', views.get_map_page, name='map'),
    path('get_markers/', views.MarkersList.as_view(), name='map'),
    path('create_marker/', views.create_marker),
    path('delete_marker/', views.delete_marker),
]
