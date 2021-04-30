from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.logout_then_login, name='logout_then_login'),
    path('password-change/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
    path('', views.account, name='account'),
    path('get_all_employees/', views.get_all_employees, name='get_all_employees'),
    path('get_all_candidates/', views.get_all_candidates, name='get_all_candidates'),
]
