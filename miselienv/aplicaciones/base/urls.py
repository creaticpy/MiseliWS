from django.contrib import admin
from django.urls import path, include
from aplicaciones.base import views

app_name = 'base'


urlpatterns = [
    path('', views.IndexView.as_view()),

]


