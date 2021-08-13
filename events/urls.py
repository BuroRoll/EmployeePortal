from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.events),
    path('event_members_page', views.event_members_page),
    path('event_manager/', views.event_manager),
    path('events_list/', views.EventsList.as_view()),
    path('join_event/', views.join_in_event),
    path('unjoin_event/', views.unjoin_in_event),
    path('create_event/', views.create_event),
    path('delete_event/', views.delete_event),
    path('update_event/', views.update_event),
    path('event_details/<int:pk>/', views.EventDetails.as_view()),

]
