from django.contrib import admin
from django.urls import path, include
from aplicaciones.base import views

app_name = 'maquetaweb'


urlpatterns = [
    path('hello-view/', views.HelloApi.as_view()),
]


