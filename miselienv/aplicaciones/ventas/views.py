import datetime
import json
import uuid

from django.conf.locale.en import formats as en_formats
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView

from .models import FacturasModel

en_formats.DATE_FORMAT = ['%d/%m/%Y', '%d-%m-%Y']


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%m/%d/%Y")


class FacturasView(LoginRequiredMixin, ListView):
    redirect = ""

    def consultas(request):
        template_name = 'facturas_ld.html'
        tabla_creada = ""

        def get_queryset(filtro, order_by):
            qs = FacturasModel.objects.all()
            # qs = FacturasModel.objects.extra(select={"fecha_documento": "DATE_FORMAT(fecha_documento, '%%Y-%%m-%%d')"})
            qs = qs.filter(Q(estado=True),
                           Q(cliente__id__nombre__icontains=filtro) |
                           Q(cliente__id__apellido__icontains=filtro) |
                           Q(cliente__id__ruc__icontains=filtro) |
                           Q(cliente__id__nro_documento__icontains=filtro) |
                           Q(fecha_documento__icontains=filtro) |
                           Q(periodo__icontains=filtro) |
                           Q(cotizacion__icontains=filtro) |
                           Q(nro_documento__icontains=filtro)
                           ).values("id", "cliente__id__nombre", "tip_documento__desc_corta", "fecha_documento",
                                    "nro_documento", "cotizacion"
                                    ).order_by("{order_by}".format(order_by=order_by))
            return qs

        try:  # entra 2 veces cuando es creada la tabla, la primera vez el parametro "tablacreada" existe y no hay problemas, la segunda vez ya no existe y da error.
            tabla_creada = request.GET['tablacreada']
        except:
            pass

        if tabla_creada == "yes":
            cols = [
                {"data": "id"},
                {"data": "cliente__id__nombre"},
                {"data": "tip_documento__desc_corta"},
                {"data": "fecha_documento"},
                {"data": "nro_documento"},
                {"data": "cotizacion"},
                {"defaultContent": "<button type='button' class='editar btn btn-primary' href='#' url='ventas/crear_modificar_facturas' tab_text='Mod Facturas'><i class='fa bi-pencil-square'></i></button>"},
                {"defaultContent": "<button type='button' class='eliminar btn btn-danger' href='#' url='ventas/borrar_facturas' tab_text='Elim Facturas' data-toggle='modal' data-target='#modalEliminar'><i class='fa bi-trash'></i></button>"},
            ]
            context = {
                "cols": cols,
                "plantilla": loader.render_to_string(template_name),
            }
            print("a")
            return JsonResponse(context)

        inicio = int(request.GET.get('inicio'))
        fin = int(request.GET.get('limite'))
        filtro = request.GET.get('filtro')
        order_by = request.GET.get('order_by')
        data = get_queryset(filtro, order_by)
        list_data = []

        for indice, valor in enumerate(data[inicio:inicio + fin], inicio):
            valor["fecha_documento"] = datetime.datetime.strptime(str(valor["fecha_documento"]), "%Y-%m-%d").strftime(
                "%d-%m-%Y")
            list_data.append(valor)

        context = {
            'count': data.count(),
            'objects': list_data
        }
        # todo default es llamado cuando un parametro no es convertido a json entonces se lo convierte a str y luego se reprocesa
        return HttpResponse(json.dumps(context, default=myconverter), 'application/json')

    def nuevo_modificar(request):
        template_name = 'facturas_crearmod.html'
        reverse = " url 'core:index'"

        params = request.GET

        fact = FacturasModel()

        if params['pk'] != 'false':

            fact = FacturasModel.objects.get(pk=params['pk'])

        context = {
            'datos': fact,
            'uuid': uuid.uuid4(),
            'form_uuid': uuid.uuid4(),
            'section_uuid': uuid.uuid4(),
            'nav_uuid': uuid.uuid4(),
            'reverse': reverse,
        }
        print("f")
        return render(request, template_name, context)

    def modificar(request):
        context = {
            "cols": "cols",
            "plantilla": "loader.render_to_string(template_name)",
        }
        return JsonResponse(context)

    def borrar(request):
        context = {
            "cols": "cols",
            "plantilla": "loader.render_to_string(template_name)",
        }
        return JsonResponse(context)
