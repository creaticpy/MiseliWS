from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('base/', include('aplicaciones.base.urls')),
    path('', include('aplicaciones.ventas.urls')),
    ]

