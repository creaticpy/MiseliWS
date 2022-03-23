from aplicaciones.ventas.forms import PedidosForm, FacturasForm, RemisionesForm
from aplicaciones.ventas.models import ConfVentasModel, ClientesSucursalesModel, ClientesModel, \
    VentasCuotasDetModel, FacturasDetModel, FacturasModel, PedidosModel, PedidosDetModel, RemisionesModel, \
    RemisionesDetModel, PedidosRemisionesModel
from django.contrib import admin
from django.core.exceptions import ValidationError
# Register your models here.


admin.site.register(ConfVentasModel)


class ClientesSucursalesAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'desc_corta']


admin.site.register(ClientesSucursalesModel, ClientesSucursalesAdmin)


class InLineClientesSucursalesAdmin(admin.TabularInline):
    model = ClientesSucursalesModel
    extra = 1


class ClientesAdmin(admin.ModelAdmin):
    inlines = [InLineClientesSucursalesAdmin]


admin.site.register(ClientesModel, ClientesAdmin)


# todo ejemplo de como agregar opcion de actions en el admin
@admin.action(description="Generar Recibos")
def Generar_recibos(modeladmin, request, queryset):
    print(modeladmin, "<--------------------------------------------------------------Este es el modeladmin")
    print(request, "<-----------------------------------------------------------------Este es el request")
    print(queryset, "<----------------------------------------------------------------Este es el queryset")


@admin.action(description="Generar Remision")
def Generar_remision(modeladmin, request, queryset):
    print(modeladmin, "<--------------------------------------------------------------Este es el modeladmin")
    print(request, "<--------------------------------------------------------------Este es el request")
    print(queryset, "<--------------------------------------------------------------Este es el queryset")


class InLinePedidosDetAdmin(admin.TabularInline):
    model = PedidosDetModel
    extra = 1
    readonly_fields = ('nro_item', 'monto_mon_local')
    autocomplete_fields = ['articulo']  # todo importantisimo
    fields = (
        'impuesto',
        'articulo',
        'cantidad',
        'precio_unitario',
        'monto_mon_local',
        'nro_item',
    )


class PedidosAdmin(admin.ModelAdmin):
    form = PedidosForm
    inlines = [InLinePedidosDetAdmin]
    raw_id_fields = ['cliente',]
    search_fields = ('cliente', 'tip_documento')
    list_filter = ('cliente', 'mes', 'periodo',)
    list_display = ('cliente', 'tip_documento', 'nro_documento', 'fecha_documento', 'monto_mon_local', )
    readonly_fields = ('monto_mon_local', 'mes', 'periodo', 'fecha_transaccion',)  # campos de solo lectura
    list_per_page = 20
    # prepopulated_fields = ??????????????
    fields = [('tip_documento', 'nro_documento',),
              ('fecha_documento', 'fecha_transaccion', 'mes', 'periodo',),
              ('cliente', 'dep_origen'),
              ('moneda', 'cotizacion',),
              ('monto_mon_local',),
              ]

    actions = [Generar_remision]


admin.site.register(PedidosModel, PedidosAdmin)


class InLinePedidosRemisionesAdmin(admin.TabularInline):
    model = PedidosRemisionesModel


class InLineRemisionesDetAdmin(admin.TabularInline):
    model = RemisionesDetModel
    extra = 1
    readonly_fields = ('nro_item', 'monto_mon_local')
    autocomplete_fields = ['articulo']  # todo importantísimo
    fields = (
        'impuesto',
        'articulo',
        'cantidad',
        'precio_unitario',
        'monto_mon_local',
        'nro_item',
    )


class RemisionesAdmin(admin.ModelAdmin):
    form = RemisionesForm
    inlines = [InLineRemisionesDetAdmin]
    raw_id_fields = ['cliente', ]
    search_fields = ('cliente', 'tip_documento', 'nro_documento')
    list_filter = ('cliente', 'mes', 'periodo',)
    list_display = ('cliente', 'tip_documento', 'nro_documento', 'fecha_documento', 'monto_mon_local', )
    readonly_fields = ('monto_mon_local', 'mes', 'periodo', 'fecha_transaccion',)  # campos de solo lectura
    list_per_page = 20
    # prepopulated_fields = ??????????????
    fields = [('tip_documento', 'nro_documento',),
              ('fecha_documento', 'fecha_transaccion', 'mes', 'periodo',),
              ('cliente', 'dep_origen'),
              ('moneda', 'cotizacion',),
              ('monto_mon_local',),
              ]

    # actions = [Generar_remision]


admin.site.register(RemisionesModel, RemisionesAdmin)


class InLineVentasCuotasDetAdmin(admin.TabularInline):
    model = VentasCuotasDetModel
    extra = 1
    classes = ['collapse']


class InLineFacturasDetAdmin(admin.TabularInline):
    model = FacturasDetModel
    extra = 1
    readonly_fields = ('nro_item', 'monto_mon_local')
    autocomplete_fields = ['articulo']  # todo importantísimo
    fields = (
        'impuesto',
        'articulo',
        'cantidad',
        'precio_unitario',
        'monto_mon_local',
        'nro_item',
    )


class FacturasAdmin(admin.ModelAdmin):
    inlines = [InLineFacturasDetAdmin, InLineVentasCuotasDetAdmin]
    raw_id_fields = ['cliente', ]
    search_fields = ('nro_documento', 'tip_documento__desc_corta', 'cliente__id__nombre', 'cliente__id__apellido', )
    list_filter = ('mes', 'periodo',)
    list_display = ('cliente', 'tip_documento', 'nro_documento', 'fecha_documento', 'monto_mon_local', 'saldo_mon_local',)
    readonly_fields = ('monto_mon_local', 'saldo_mon_local', 'mes', 'periodo', 'fecha_transaccion',)  # campos de solo lectura
    list_per_page = 20
    # prepopulated_fields = ??????????????
    fields = [('tip_documento', 'nro_documento',),
              ('contado_credito', 'conf_cuotas',),
              ('fecha_documento', 'fecha_transaccion', 'mes', 'periodo',),
              ('cliente', 'dep_origen'),
              ('moneda', 'cotizacion',),
              ('monto_mon_local', 'saldo_mon_local'),
              ]

    actions = [Generar_recibos]


admin.site.register(FacturasModel, FacturasAdmin)

