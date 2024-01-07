from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('api/v1/',include('api.urls')),
    path('set_language/', set_language, name='set_language'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
