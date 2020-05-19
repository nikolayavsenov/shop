from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from app import views
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('api/v1/', include('api.urls')),
    path('accounts/', include('allauth.urls')),
    path('', views.index),
    path('debug/', include(debug_toolbar.urls)),
    #path('', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

