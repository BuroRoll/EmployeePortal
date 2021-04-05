from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from services.views import TGBotView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('webhooks/telegram/', csrf_exempt(TGBotView.as_view())),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
