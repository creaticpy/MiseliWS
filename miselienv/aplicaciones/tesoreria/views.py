import datetime
import json
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from django.template import loader
from django.views.generic import ListView
from aplicaciones.rrhh.forms import PersonasForm
from aplicaciones.rrhh.models import PersonasModel
from aplicaciones.rrhh.views import myconverter

from .forms import EntidadesFinancierasForm, EntFinancierasPersonasForm
from aplicaciones.tesoreria.models import EntidadesFinancierasModel

from django.http import HttpResponse, JsonResponse


class EntidadesFinancierasView(LoginRequiredMixin, ListView):
    redirect = ""

    def consultas(request):
        template_name = 'entidadesfinancieras_ld.html'
        tabla_creada = ""
        url_agregar_registro = "tesoreria/agregar_entidadesfinancieras"
        tab_texto = "Cargar Ent. Financiera"

        def get_queryset(filtro, order_by):
            qs = EntidadesFinancierasModel.objects.all()
            qs = qs.filter(Q(estado=True),
                           Q(persona__nombre__icontains=filtro) |
                           Q(persona__apellido__icontains=filtro) |
                           Q(persona__nro_documento__icontains=filtro) |
                           Q(persona__razon_social__icontains=filtro)
                           ).values("id", "persona__nombre", "persona__apellido",
                                    "persona__nro_documento", "persona__direccion", "persona__email",
                                    "persona__ruc",
                                    ).order_by("{order_by}".format(order_by=order_by))
            return qs

        try:  # entra 2 veces cuando es creada la tabla, la primera vez el parametro "tablacreada" existe y no hay problemas, la segunda vez ya no existe y da error.
            tabla_creada = request.GET['tablacreada']
        except:
            pass

        if tabla_creada == "yes":
            cols = [
                {"data": "id"},
                {"data": "persona__nombre"},
                {"data": "persona__apellido"},
                {"data": "persona__email"},
                {"data": "persona__direccion"},
                {"data": "persona__ruc"},

                {
                    "defaultContent": "<button type='button' class='editar btn btn-primary'><i charger_function='fm' abrir_en='tab-principal' href='#' url='tesoreria/modificar_entidadesfinancieras' tab_text='Mod Ent. Financieras' class='fa bi-pencil-square'></i></button>"},
                {
                    "defaultContent": "<button type='button' class='eliminar btn btn-danger' href='#' url='rrhh/borrar_empleados' tab_text='Elim Empleado' data-toggle='modal' data-target='#modalEliminar'><i class='fa bi-trash'></i></button>"},

            ]
            context = {
                "cols": cols,
                "plantilla": loader.render_to_string(template_name),
                "url_agregar_registro": url_agregar_registro,
                "tab_texto": tab_texto,
            }

            return JsonResponse(context)

        inicio = int(request.GET.get('inicio'))
        fin = int(request.GET.get('limite'))
        filtro = request.GET.get('filtro')
        order_by = request.GET.get('order_by')
        data = get_queryset(filtro, order_by)
        list_data = []

        for indice, valor in enumerate(data[inicio:inicio + fin], inicio):
            list_data.append(valor)

        context = {
            'count': data.count(),
            'objects': list_data
        }
        # todo default es llamado cuando un parametro no es convertido a json entonces se lo convierte a str y luego se reprocesa
        return HttpResponse(json.dumps(context, default=myconverter), 'application/json')

    @transaction.atomic
    def agregar(request):
        template_name = 'entidadesfinancieras_crearmod.html'
        entidades_financieras = EntidadesFinancierasModel()

        if request.method == 'GET':
            formcab = PersonasForm()
            formdet = EntidadesFinancierasForm()
            # formdet = entidades_financieras

            ctx = {
                'form': formcab,
                'formset': formdet,
                'uuid': uuid.uuid4(),
                'form_uuid': uuid.uuid4(),
                'section_uuid': uuid.uuid4(),
                'nav_uuid': uuid.uuid4(),
                'url_guardar': 'tesoreria/agregar_entidadesfinancieras',

            }
            return render(request, template_name, ctx)

        if request.method == 'POST':
            formcab = EntFinancierasPersonasForm(request.POST, instance=PersonasModel())
            formdet = EntidadesFinancierasForm(request.POST, instance=EntidadesFinancierasModel())

            if formcab.is_valid() and formdet.is_valid():
                # formcab = formcab.save(commit=False) # I need this....
                formcab = formcab.save()  # I don´t need this. because it's all or nothing
                obj = formdet.save(commit=False)
                obj.persona = formcab
                formcab.save()
                obj.save()
                return JsonResponse({'text': 'Registro Guardado...', 'type': 'primary', 'timelapse': '3000'})
            else:
                print('formdet.errors', formdet.errors)
                return JsonResponse({'text': 'Registro no guardado...', 'type': 'danger', 'timelapse': '3000'})
                # return render(request, template_name, ctx)
        # if formcab.is_valid() and formdet.is_valid(): esto si funciona
        #     formcab = formcab.save() // esto esta equivocado es toodo o nada....
        #     #formdet.id = formcab.id
        #     #formcab.save()
        #     obj = formdet.save(commit=False)
        #     obj.id = formcab
        #     obj.save()
        #     return JsonResponse({'text': 'Registro Guardado...', 'type': 'primary', 'timelapse': '3000'})
        # else:
        #     return JsonResponse({'text': 'Registro no guardado (Detalle)', 'type': 'primary', 'timelapse': '3000'})

        return JsonResponse({'´status': '´done'})

    def modificar(request):  # update method
        template_name = 'entidadesfinancieras_crearmod.html'

        ctx = {}
        formcab = EntFinancierasPersonasForm()
        formdet = EntidadesFinancierasModel()

        if request.method == 'GET':
            parametros = request.GET
            v_id = EntidadesFinancierasModel.objects.filter(pk=parametros['pk']).values('persona')[:1].get()['persona']
            objeto = PersonasModel.objects.get(pk=v_id)
            objentfin = EntidadesFinancierasModel.objects.get(persona=v_id)
            if objeto is not None:
                formcab = EntFinancierasPersonasForm(instance=objeto)
                formdet = EntidadesFinancierasForm(instance=objentfin)

                ctx = {
                    'form': formcab,
                    'formset': formdet,
                    'uuid': uuid.uuid4(),
                    'form_uuid': uuid.uuid4(),
                    'section_uuid': uuid.uuid4(),
                    'nav_uuid': uuid.uuid4(),
                    'url_guardar': 'tesoreria/modificar_entidadesfinancieras',
                }
                return render(request, template_name, ctx)

        elif request.method == 'POST':
            print("a", request.POST)
            obj = PersonasModel.objects.get(pk=request.POST['id'])
            obj2 = EntidadesFinancierasModel.objects.get(persona=request.POST['id'])
            formcab = EntFinancierasPersonasForm(request.POST, instance=obj)

            if formcab.is_valid():
                formcab = formcab.save(commit=False)
                formdet = EntidadesFinancierasForm(request.POST, instance=obj2)

                if formdet.is_valid():
                    formcab.save()
                    formdet.save()
                    return JsonResponse({'text': 'Guardado correctamente', 'type': 'primary', 'timelapse': '3000'})
                else:
                    print(formdet.errors, "error 2")
                    return JsonResponse({'text': "Formulario no Guardado", 'type': 'danger', 'timelapse': '3000'})

            else:
                print("error de cabecera")
                return JsonResponse({'text': "Formulario no Guardado", 'type': 'danger', 'timelapse': '3000'})

        # return render(request, template_name, ctx)

    def borrar(request):
        if request.method == 'POST':
            print("esta pio aqui?")
            objP = PersonasModel.objects.get(pk=request.POST['id'])
            objE = EntidadesFinancierasModel.objects.get(pk=request.POST['id'])
            if objE is None:
                return JsonResponse({'error': 'No existe el registro de empleado, consulte con el administrador'})
            elif objP is None:
                return JsonResponse({'error': 'No existe el registro de persona, consulte con el administrador'})
            objE = objE.delete()
            objP = objP.delete()
            return JsonResponse({'text': "Registros Borrados", 'type': 'danger', 'timelapse': '3000'})

        context = {
            "cols": "cols",
            "plantilla": "loader.render_to_string(template_name)",
        }
        return JsonResponse(context)
