from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from services.telegramBot import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webhooks/telegram/', csrf_exempt(TelegramBot.as_view())),
    path('', include('accounts.urls')),
    path('', include('services.urls')),
    path('', include('devices.urls')),
    path('', include('events.urls')),
    path('', include('map.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
