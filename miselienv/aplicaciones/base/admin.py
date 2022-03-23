from django.contrib import admin

from aplicaciones.base.models import UserProfile, SucursalesModel, EmpresasModel, BocasExpedicionModel, \
    BocasEmpleadosModel, NumerosSiguientesModel
from aplicaciones.base.models import ConfBaseModel
from aplicaciones.rrhh.models import EmpleadosBocasProxy

admin.site.site_header = 'SAAS SRL'
admin.site.index_title = 'Menu SAAS'
admin.site.site_title  = 'El mejor sistema'

admin.site.register(UserProfile)

admin.site.register(EmpresasModel)
admin.site.register(SucursalesModel)
admin.site.register(ConfBaseModel)


class BocasEmpleadosAdmin(admin.TabularInline):
    model = BocasEmpleadosModel
    extra = 1
    autocomplete_fields = ['empleado']


@admin.register(BocasExpedicionModel)
class BocasExpedicionAdmin(admin.ModelAdmin):
    inlines = [BocasEmpleadosAdmin, ]

    list_display = ['nombresucursal', 'nro_boca', ]
    list_filter = ['sucursal', ]


@admin.register(EmpleadosBocasProxy)
class EmpleadosBocasAdmin(admin.ModelAdmin):
    inlines = [BocasEmpleadosAdmin]
    fields = ['id']
    readonly_fields = ['id']

    def get_queryset(self, request):
        return EmpleadosBocasProxy.objects.all()


@admin.register(NumerosSiguientesModel)
class NumerosSiguientesAdmin(admin.ModelAdmin):
    list_display = ['tip_documento', 'sucursal', 'boca', 'nro_documento', ]
    ordering = ['tip_documento', 'boca_expedicion', ]
    fields = [('tip_documento', 'boca_expedicion', ),
              'nro_documento',]

    def sucursal(self, obj):
        return obj.boca_expedicion.sucursal.desc_larga

    def boca(self, obj):
        return obj.boca_expedicion.nro_boca
