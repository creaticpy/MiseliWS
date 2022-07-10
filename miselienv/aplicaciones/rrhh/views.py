import datetime
import json
import uuid

from django.conf.locale.en import formats as en_formats
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory, modelform_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView

from .forms import EmpleadosForm, PersonasForm, EmpleadosBeneficiosForm
from .models import EmpleadosModel, PersonasModel, EmpleadosBeneficiosModel

en_formats.DATE_FORMAT = ['%d/%m/%Y', '%d-%m-%Y']
from django.shortcuts import render


# Create your views here.
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%m/%d/%Y")


class EmpleadosView(LoginRequiredMixin, ListView):
    redirect = ""

    def consultas(request):
        template_name = 'empleados_ld.html'
        tabla_creada = ""
        url_agregar_registro = "rrhh/agregar_empleados"
        tab_texto = "Cargar Empleado"

        def get_queryset(filtro, order_by):
            qs = EmpleadosModel.objects.all()
            # qs = FacturasModel.objects.extra(select={"fecha_documento": "DATE_FORMAT(fecha_documento, '%%Y-%%m-%%d')"})
            qs = qs.filter(Q(estado=True),
                           Q(id__nombre__icontains=filtro) |
                           Q(id__apellido__icontains=filtro) |
                           Q(id__nro_documento__icontains=filtro) |
                           Q(id__razon_social__icontains=filtro)
                           ).values("id", "id__nombre", "id__apellido", "fecha_ingreso",
                                    "fecha_egreso", "id__nro_documento", "id__direccion", "id__email",
                                    "id__nro_celular",
                                    ).order_by("{order_by}".format(order_by=order_by))
            return qs

        try:  # entra 2 veces cuando es creada la tabla, la primera vez el parametro "tablacreada" existe y no hay problemas, la segunda vez ya no existe y da error.
            tabla_creada = request.GET['tablacreada']
        except:
            pass

        if tabla_creada == "yes":
            cols = [
                {"data": "id"},
                {"data": "id__nombre"},
                {"data": "id__apellido"},
                {"data": "fecha_ingreso"},
                {"data": "fecha_egreso"},
                {"data": "id__email"},
                {"data": "id__direccion"},
                {"data": "id__nro_documento"},
                {
                    "defaultContent": "<button type='button' class='editar btn btn-primary'><i charger_function='fm' abrir_en='tab-principal' href='#' url='rrhh/modificar_empleados' tab_text='Mod Empleado' class='fa bi-pencil-square'></i></button>"},
                {
                    "defaultContent": "<button type='button' class='eliminar btn btn-danger' href='#' url='rrhh/borrar_empleados' tab_text='Elim Empleado' data-toggle='modal' data-target='#modalEliminar'><i class='fa bi-trash'></i></button>"},
            #     "defaultContent": "<button type='button' class='editar btn btn-primary' href='#' url='rrhh/modificar_empleados' tab_text='Mod Empleado'><i class='fa bi-pencil-square'></i></button>"},
            # {
            #     "defaultContent": "<button type='button' class='eliminar btn btn-danger' href='#' url='rrhh/borrar_empleados' tab_text='Elim Empleado' data-toggle='modal' data-target='#modalEliminar'><i class='fa bi-trash'></i></button>"},

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
            valor["fecha_ingreso"] = valor["fecha_ingreso"].strftime("%d/%m/%Y")
            list_data.append(valor)

        context = {
            'count': data.count(),
            'objects': list_data
        }
        # todo default es llamado cuando un parametro no es convertido a json entonces se lo convierte a str y luego se reprocesa
        return HttpResponse(json.dumps(context, default=myconverter), 'application/json')

    def agregar(request):
        template_name = 'empleados_crearmod.html'
        empleadosformset = inlineformset_factory(PersonasModel, EmpleadosModel, form=EmpleadosForm, fk_name='id',
                                                 fields=('estado', 'fecha_ingreso', 'fecha_egreso', 'email',
                                                         'contacto_emergencia',), extra=1, max_num=1)
        emplbeneficiosformset = inlineformset_factory(EmpleadosModel, EmpleadosBeneficiosModel, form=EmpleadosBeneficiosForm, fk_name='empleado',
                                                 fields=('estado', 'beneficio',), extra=15, max_num=15)
        if request.method == 'GET':
            formcab = PersonasForm()
            formdet = empleadosformset()
            formdetben = emplbeneficiosformset()

            ctx = {
                'form': formcab,
                'formset': formdet,
                'formsetbeneficios': formdetben,
                'uuid': uuid.uuid4(),
                'form_uuid': uuid.uuid4(),
                'section_uuid': uuid.uuid4(),
                'nav_uuid': uuid.uuid4(),
                'url_guardar': 'rrhh/agregar_empleados',

            }
            return render(request, template_name, ctx)

        if request.method == 'POST':
            formcab = PersonasForm(request.POST)
            if formcab.is_valid():
                formcab = formcab.save(commit=False)
                formdet = empleadosformset(request.POST, instance=formcab)
                if formdet.is_valid():
                    formcab.save()
                    formdet.save()
                    print("FORMULARIO tiene error?.....!!!!", formdet.errors)
                    print("FORMULARIO debe tener error.....!!!!", formdet.non_form_errors())
                    print("FORMULARIO data.....!!!!", formdet.data)
                    print("FORMULARIO asecas.....!!!!", formdet)
                    return JsonResponse({'text': 'Registro Guardado...', 'type': 'primary', 'timelapse': '3000'})
                else:
                    return JsonResponse({'text': 'Registro no guardado', 'type': 'primary', 'timelapse': '3000'})

            else:
                print("FORMULARIO INVALIDO", formcab.errors)
                return JsonResponse({'text': 'Registro no guardado', 'type': 'primary', 'timelapse': '3000'})

    def modificar(request):  # update method
        template_name = 'empleados_crearmod.html'
        empleadosformset = inlineformset_factory(PersonasModel, EmpleadosModel, form=EmpleadosForm, fk_name='id',
                                                 fields=('estado', 'fecha_ingreso', 'fecha_egreso', 'email',
                                                         'contacto_emergencia',), extra=1, max_num=1)
        emplbeneficiosformset = inlineformset_factory(EmpleadosModel, EmpleadosBeneficiosModel, form=EmpleadosBeneficiosForm, fk_name='empleado',
                                                 fields=('estado', 'beneficio',), extra=15, max_num=15)

        ctx = {}
        formcab = PersonasForm()
        formdet = empleadosformset()
        formdetben = emplbeneficiosformset()

        if request.method == 'GET':
            parametros = request.GET
            objeto = PersonasModel.objects.get(pk=parametros['pk'])
            objemp = EmpleadosModel.objects.get(pk=parametros['pk'])
            if objeto is not None:
                formcab = PersonasForm(instance=objeto)
                formdet = empleadosformset(instance=objeto)
                formdetben = emplbeneficiosformset(instance=objemp)
                ctx = {
                    'form': formcab,
                    'formset': formdet,
                    'formsetbeneficios': formdetben,
                    'uuid': uuid.uuid4(),
                    'form_uuid': uuid.uuid4(),
                    'section_uuid': uuid.uuid4(),
                    'nav_uuid': uuid.uuid4(),
                    'url_guardar': 'rrhh/modificar_empleados',
                }
                return render(request, template_name, ctx)

        elif request.method == 'POST':
            empleadosformset = inlineformset_factory(PersonasModel, EmpleadosModel, form=EmpleadosForm, fk_name='id',
                                                     fields=('estado', 'fecha_ingreso', 'fecha_egreso', 'email',
                                                             'contacto_emergencia',), extra=1, max_num=1)
            emplbeneficiosformset = inlineformset_factory(EmpleadosModel, EmpleadosBeneficiosModel,
                                                          form=EmpleadosBeneficiosForm, fk_name='empleado',
                                                          fields=('estado', 'beneficio',), extra=15, max_num=15)
            # forms.py linea 33, revisar con Anthony, no es la manera de hacerlo.
            # facturas_crearmod.html linea 12, no debe ser la manera de hacerlo.....
            obj = PersonasModel.objects.get(pk=request.POST['id'])
            formcab = PersonasForm(request.POST, instance=obj)
            formdetben = EmpleadosModel.objects.get(pk=request.POST['id'])

            if formcab.is_valid():
                formcab = formcab.save(commit=False)
                formdet = empleadosformset(request.POST, instance=formcab)
                formdetben = emplbeneficiosformset(request.POST, instance=formdetben)
                if formdet.is_valid() and formdetben.is_valid():
                    formcab.save()
                    formdet.save()
                    formdetben.save()
                    return JsonResponse({'text': 'Guardado correctamente', 'type': 'primary', 'timelapse': '3000'})
                else:
                    return JsonResponse({'text': "Formulario no Guardado", 'type': 'danger', 'timelapse': '3000'})

            else:
                return JsonResponse({'text': "Formulario no Guardado", 'type': 'danger', 'timelapse': '3000'})

        # return render(request, template_name, ctx)

    def borrar(request):

        if request.method == 'POST':
            print("esta pio aqui?")
            objE = EmpleadosModel.objects.get(pk=request.POST['id'])
            objP = PersonasModel.objects.get(pk=request.POST['id'])
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
