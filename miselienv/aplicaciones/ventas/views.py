import datetime
import json
import uuid

from django.conf.locale.en import formats as en_formats
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView

from .forms import FacturasForm, FacturasDetForm
from .models import FacturasModel, FacturasDetModel

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
        url_agregar_registro = "ventas/agregar_facturas"

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
                {
                    "defaultContent": "<button type='button' class='editar btn btn-primary' href='#' url='ventas/modificar_facturas' tab_text='Mod Facturas'><i class='fa bi-pencil-square'></i></button>"},
                {
                    "defaultContent": "<button type='button' class='eliminar btn btn-danger' href='#' url='ventas/borrar_facturas' tab_text='Elim Facturas' data-toggle='modal' data-target='#modalEliminar'><i class='fa bi-trash'></i></button>"},
            ]
            context = {
                "cols": cols,
                "plantilla": loader.render_to_string(template_name),
                "url_agregar_registro": url_agregar_registro,
            }

            return JsonResponse(context)

        inicio = int(request.GET.get('inicio'))
        fin = int(request.GET.get('limite'))
        filtro = request.GET.get('filtro')
        order_by = request.GET.get('order_by')
        data = get_queryset(filtro, order_by)
        list_data = []

        for indice, valor in enumerate(data[inicio:inicio + fin], inicio):
            valor["fecha_documento"] = valor["fecha_documento"].strftime("%d/%m/%Y")
            list_data.append(valor)

        context = {
            'count': data.count(),
            'objects': list_data
        }
        # todo default es llamado cuando un parametro no es convertido a json entonces se lo convierte a str y luego se reprocesa
        return HttpResponse(json.dumps(context, default=myconverter), 'application/json')

    def agregar(request):
        template_name = 'facturas_crearmod.html'
        facturadetformset = inlineformset_factory(FacturasModel, FacturasDetModel, fk_name='factura',
                                                  fields=('articulo', 'nro_item', 'cantidad', 'precio_unitario', 'impuesto',
                                                          'desc_larga',), max_num=15, absolute_max=1500)
        data = {}
        ctx  = {}

        if request.method == 'GET':
            formcab = FacturasForm()
            formdet = facturadetformset()
            ctx = {
                'form': formcab,
                'formset': formdet,
                'uuid': uuid.uuid4(),
                'form_uuid': uuid.uuid4(),
                'section_uuid': uuid.uuid4(),
                'nav_uuid': uuid.uuid4(),
                'url_guardar': 'ventas/agregar_facturas',
                # 'url_guardar': 'ventas/guardar_facturas',

            }
            return render(request, template_name, ctx)

        if request.method == 'POST':
            formcab = FacturasForm(request.POST)

            if formcab.is_valid():
                formcab = formcab.save(commit=False)
                formdet = facturadetformset(request.POST, instance=formcab)
                if formdet.is_valid():
                    formcab.save()
                    formdet.save()
                else:
                    print(formdet.non_form_errors())
                    print("NO ES VALIDO---------------------------------------")
                    return render(request, template_name, {'error': 'Error en el formulario'})

            else:
                print("FORMULARIO INVALIDO")
            return render(request, template_name, {'error': 'Error en el formulario'})

    def modificar(request):  # update method
        template_name = 'facturas_crearmod.html'
        facturadetformset = inlineformset_factory(FacturasModel, FacturasDetModel, form=FacturasDetForm, fk_name='factura',
                                                  fields=('articulo', 'nro_item', 'cantidad', 'precio_unitario', 'impuesto',
                                                          'desc_larga',), extra=15, max_num=15)
        ctx = {}
        formcab = FacturasForm()
        formdet = facturadetformset()

        if request.method == 'GET':
            parametros = request.GET
            objeto = FacturasModel.objects.get(pk=parametros['pk'])
            if objeto is not None:
                formcab = FacturasForm(instance=objeto)
                formdet = facturadetformset(instance=objeto)

                ctx = {
                    'form': formcab,
                    'formset': formdet,
                    'uuid': uuid.uuid4(),
                    'form_uuid': uuid.uuid4(),
                    'section_uuid': uuid.uuid4(),
                    'nav_uuid': uuid.uuid4(),
                    'url_guardar': 'ventas/modificar_facturas',
                    # 'url_guardar': 'ventas/guardar_facturas',
                }
                return render(request, template_name, ctx)

        elif request.method == 'POST':
            facturadetformset = inlineformset_factory(FacturasModel, FacturasDetModel, form=FacturasDetForm, fk_name='factura', fields=('articulo', 'nro_item', 'cantidad', 'precio_unitario', 'impuesto', 'desc_larga',), extra=15, max_num=15)

            # forms.py linea 33, revisar con Anthony, no es la manera de hacerlo.
            # facturas_crearmod.html linea 12, no debe ser la manera de hacerlo.....
            obj = FacturasModel.objects.get(pk=request.POST['id'])
            formcab = FacturasForm(request.POST, instance=obj)

            if formcab.is_valid():
                formcab = formcab.save(commit=False)
                formdet = facturadetformset(request.POST, instance=formcab)
                if formdet.is_valid():
                    formcab.save()
                    formdet.save()
                    return JsonResponse({'text': 'Guardado correctamente', 'type': 'primary', 'timelapse': '3000'})
                else:
                    return JsonResponse({'text': "Formulario no Guardado", 'type': 'danger', 'timelapse': '3000'})

            else:
                return JsonResponse({'text': "Formulario no Guardado", 'type': 'danger', 'timelapse': '3000'})

        # return render(request, template_name, ctx)

    def borrar(request):
        context = {
            "cols": "cols",
            "plantilla": "loader.render_to_string(template_name)",
        }
        return JsonResponse(context)









