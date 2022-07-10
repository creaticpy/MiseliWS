from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models

# Create your models here.
from django.views.generic import ListView
from aplicaciones.rrhh.models import PersonasModel
from django.core.serializers import serialize

import json

class ServiciosView(LoginRequiredMixin, ListView):

    def consultar_tablero(request):

        if request.method == 'GET':
            empleado = PersonasModel.objects.all()
            empleado = serialize('json', empleado)

            # return JsonResponse(empleado, safe=False)
            return HttpResponse(empleado, content_type="application/json")
