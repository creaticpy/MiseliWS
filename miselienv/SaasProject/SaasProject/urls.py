"""SaasProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import IndexView
from aplicaciones.base import views


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('base/', include('aplicaciones.base.urls')),
    path('', include('aplicaciones.ventas.urls')),
    path('', include('aplicaciones.rrhh.urls')),
    path('', include('aplicaciones.servicios.urls')),

]

# Add Django site authentication urls (for login, logout, password management)
# https://developer.mozilla.org/es/docs/Learn/Server-side/Django/Authentication
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]


# faulthandler ???? # todo no se que es
# handler404 = 'aplicaciones.ventas.views.NOMBRE-DEVISTA-AQUI'
# handler403 = 'aplicaciones.ventas.views.NOMBRE-DEVISTA-AQUI'
# handler500 = 'aplicaciones.ventas.views.NOMBRE-DEVISTA-AQUI'
# Y AGREGAR A LA VISTA:
# CLASS NOMBREVISTA(RETURN, exception):