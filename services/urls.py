from django.urls import path

from . import views

urlpatterns = [
    path('get_access/', views.get_system_access, name='systems_access'),
    path('systems_list/', views.SystemsList.as_view()),
    path('conversations_list/', views.ConversationsList.as_view()),
    path('send_request_for_access/', views.send_request_for_access),
]
