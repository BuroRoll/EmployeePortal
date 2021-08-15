from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_menu, name='mainmenu'),
    path('account/', views.account, name='account'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.logout_then_login, name='logout_then_login'),
    path('password-change/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
    path('get_all_employees/', views.get_all_employees_page, name='get_all_employees'),
    path('delete_candidate/', views.delete_candidate, name='delete_candidate'),
    path('get_all_candidates/', views.get_all_candidates, name='get_all_candidates'),
    path('vacations/', views.vacations_table, name='vacations'),
    path('set_vacations/', views.set_vacations_days, name='set_vacations_days'),
    path('get_vacations/<int:pk>/', views.GetUserVacation.as_view()),
    path('download_vacations/', views.download_vacations_page, name='download_vacations_page'),
    path('download_vacations_list/', views.download_vacations, name='download_vacations'),
    path('users_logins/', views.get_users_logins, name='login_serializer'),
]
