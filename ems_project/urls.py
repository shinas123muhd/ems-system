from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Template-based views (HTML pages)
    path('', include('accounts.urls')),
    path('employees/', include('employees.urls')),

    # REST API endpoints
    path('api/', include('accounts.api_urls')),
    path('api/', include('employees.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
