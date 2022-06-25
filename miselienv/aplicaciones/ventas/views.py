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
                                                          'desc_larga',), extra=3, absolute_max=1500)
        data = {}
        ctx  = {}
        formcab = FacturasForm()
        formdet = facturadetformset()

        if request.method == 'POST':
            csrf = request.POST
            for key, value in csrf.items():
                data = key
            data = json.loads(data)
            formcab = FacturasForm(data=data)
            # print(formcab, "----------------------------------------> esto es formcab")
            if formcab.is_valid():
                formcab = formcab.save(commit=False)
                formdet = facturadetformset(data=data, instance=formcab)
                print(formdet, "fooooooooooooooooooooooooooooormdet")
                if formdet.is_valid():
                    formcab.save()
                    formdet.save()
                else:
                    print(formdet.non_form_errors())
                    print("NO ES VALIDO---------------------------------------")

            else:
                print("FORMULARIO INVALIDO")
                ctx['mensaje'] = 'No se que mensaje poner'
                # return JsonResponse(ctx)

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


    # def agregar(request):
    #     template_name = 'facturas_crearmod.html'
    #     reverse = " url 'core:index'"
    #     # https://github.com/rayed/django-crud-parent-child/blob/master/apps/books_pc_formset2/templates/books_pc_formset2/book_form.html
    #     data = {
    #         'form': FacturasForm,
    #         'uuid': uuid.uuid4(),
    #         'form_uuid': uuid.uuid4(),
    #         'section_uuid': uuid.uuid4(),
    #         'nav_uuid': uuid.uuid4(),
    #         'url_guardar': 'ventas/guardar_facturas',
    #         'reverse': reverse,
    #     }
    #
    #     return render(request, template_name, data)

    def guardar(request):
        template_name = 'facturas_crearmod.html'
        data = {}

        if request.method == 'POST':
            try:
                csrf = request.POST
                for key, value in csrf.items():
                    data = key
                data = json.loads(data)

                form = FacturasForm(data=data)
                if form.is_valid():
                    form.save()
                    data['mensaje'] = "Guardado Correctamente"
                else:
                    data['mensaje'] = 'No se que mensaje poner'
            except Exception as e:
                print(e)

        return render(request, template_name, data)

    # def nuevo_modificar(request):
    #     template_name = 'facturas_crearmod.html'
    #     reverse = " url 'core:index'"
    #
    #     params = request.GET
    #
    #     fact = FacturasModel()
    #     adsf = FacturasModel()
    #     print(adsf._meta.__class__)
    #
    #     for x in adsf._meta.__dict__:
    #         print(x)
    #         print(x)
    #     # for x in adsf._meta.local_fields:
    #     #     aaaa.append(x.name)
    #     #     print(x.name)
    #     #     print(x)
    #
    #
    #
    #
    #     # print(list(adsf.__dict__.keys()), "esto es dict keys()")
    #     # print(list(adsf.__dict__), "esto es dict")
    #     if params['pk'] != 'false':
    #
    #         fact = FacturasModel.objects.get(pk=params['pk'])
    #
    #
    #     context = {
    #         'datos': fact,
    #         'uuid': uuid.uuid4(),
    #         'form_uuid': uuid.uuid4(),
    #         'section_uuid': uuid.uuid4(),
    #         'nav_uuid': uuid.uuid4(),
    #         'reverse': reverse,
    #     }
    #
    #     return render(request, template_name, context)

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














  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  # def agregar(request):
  #       template_name = 'facturas_crearmod.html'
  #       facturadetformset = inlineformset_factory(FacturasModel, FacturasDetModel, fk_name='factura',
  #                                             fields=('articulo', 'nro_item', 'cantidad', 'precio_unitario'), extra=3)
  #       data = {}
  #       ctx  = {}
  #       formcab = FacturasForm(data=data or None)
  #       formdet = facturadetformset(data=data or None)
  #       # formdet = facturadetformset(data=data or None, instance=FacturasModel())
  #
  #       if request.method == 'POST':
  #           csrf = request.POST
  #           for key, value in csrf.items():
  #               data = key
  #           data = json.loads(data)
  #           formcab = FacturasForm(data=data or None)
  #           formdet = facturadetformset(data=data or None)
  #           for a in data:
  #               print(a, "que es esto:-++++++++++++++++++++++++++++++++++++++++++")
  #
  #           if formcab.is_valid() and formdet.is_valid():
  #               print("is valid formdet???????????????????????????????????????????????????????????????")
  #               factura = formcab.save()
  #               formdet.save()
  #
  #
  #           else:
  #               print("no es valid")
  #               ctx['mensaje'] = 'No se que mensaje poner'
  #               # return JsonResponse(ctx)
  #
  #       ctx = {
  #           'form': formcab,
  #           'formset': formdet,
  #           'uuid': uuid.uuid4(),
  #           'form_uuid': uuid.uuid4(),
  #           'section_uuid': uuid.uuid4(),
  #           'nav_uuid': uuid.uuid4(),
  #           'url_guardar': 'ventas/agregar_facturas',
  #           # 'url_guardar': 'ventas/guardar_facturas',
  #
  #       }
  #
  #       return render(request, template_name, ctx)
  #
  #
  #   # def agregar(request):
  #   #     template_name = 'facturas_crearmod.html'
  #   #     reverse = " url 'core:index'"
  #   #     # https://github.com/rayed/django-crud-parent-child/blob/master/apps/books_pc_formset2/templates/books_pc_formset2/book_form.html
  #   #     data = {
  #   #         'form': FacturasForm,
  #   #         'uuid': uuid.uuid4(),
  #   #         'form_uuid': uuid.uuid4(),
  #   #         'section_uuid': uuid.uuid4(),
  #   #         'nav_uuid': uuid.uuid4(),
  #   #         'url_guardar': 'ventas/guardar_facturas',
  #   #         'reverse': reverse,
  #   #     }
  #   #
  #   #     return render(request, template_name, data)